"""Leakage tests for the conformal wrappers.

The paper criticises other studies for look-ahead, so this must be enforced in
code rather than asserted in prose. The test constructs a series whose future
becomes wildly more volatile at a known date and checks that intervals issued
for targets whose ORIGIN precedes that date are unaffected by it.

Run:  python test_no_leakage.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_core import conformal  # noqa: E402

CAL = 250
N = 900
BREAK = 700  # position where volatility explodes


def build(seed: int = 0) -> tuple[pd.Series, pd.Series]:
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2020-01-01", periods=N, freq="B")
    y = pd.Series(np.cumsum(rng.normal(0, 1, N)), index=idx)
    f = y + rng.normal(0, 0.5, N)
    return f, y


def counterfactual(f: pd.Series, y: pd.Series, scale: float, seed: int = 1):
    """Same data, but everything from BREAK onward is perturbed."""
    rng = np.random.default_rng(seed)
    y2 = y.copy()
    y2.iloc[BREAK:] = y2.iloc[BREAK:] + rng.normal(0, scale, N - BREAK)
    return f, y2


def check(name: str, fn, horizon: int) -> bool:
    f, y = build()
    a = fn(f, y, horizon)
    f2, y2 = counterfactual(f, y, scale=50.0)
    b = fn(f2, y2, horizon)
    common = a.index.intersection(b.index)
    # Targets whose ORIGIN is strictly before the break cannot legitimately be
    # influenced by post-break outcomes.
    origin_pos = pd.Series(range(len(y)), index=y.index).reindex(common) - horizon
    safe = common[origin_pos.values < BREAK]
    if len(safe) == 0:
        print(f"  {name} h={horizon}: no comparable targets"); return True
    d_lo = (a.loc[safe, "lo"] - b.loc[safe, "lo"]).abs().max()
    d_hi = (a.loc[safe, "hi"] - b.loc[safe, "hi"]).abs().max()
    ok = max(d_lo, d_hi) < 1e-9
    print(f"  {name} h={horizon}: {'PASS' if ok else 'FAIL'} "
          f"(max drift lo={d_lo:.3g}, hi={d_hi:.3g}, n={len(safe)})")
    return ok


def main() -> int:
    fns = {
        "split_conformal": lambda f, y, h: conformal.split_conformal(f, y, 0.2, CAL, horizon=h),
        "aci": lambda f, y, h: conformal.aci(f, y, 0.2, CAL, horizon=h),
        "cqr": lambda f, y, h: conformal.cqr(f - 1.0, f + 1.0, y, 0.2, CAL, horizon=h),
    }
    all_ok = True
    print("no-leakage tests (post-break outcomes must not affect pre-break-origin intervals)")
    for name, fn in fns.items():
        for h in (1, 5, 22):
            all_ok &= check(name, fn, h)
    print("ALL PASS" if all_ok else "FAILURES PRESENT")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
