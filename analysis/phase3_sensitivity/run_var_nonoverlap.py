"""E2: value-at-risk backtests on NON-OVERLAPPING origins.

At h = 5 and h = 22 the manuscript issues a forecast every day, so the realised
horizons overlap and the exceedance sequence is mechanically dependent even
under a correctly specified model. Kupiec's test assumes i.i.d. Bernoulli hits
and Christoffersen's independence test assumes an independent hit sequence;
neither holds on the overlapping sample.

This script re-runs the unconditional-coverage backtest on a thinned sample —
every h-th origin, so consecutive retained forecasts do not share any target
period — and reports the empirical exceedance rate first and the test second,
because a pass rate is not evidence of validity.

The overlapping results in the manuscript are not deleted; they are relabelled
as descriptive and this is the inferential version.

Run:  python analysis/phase3_sensitivity/run_var_nonoverlap.py
"""
import io
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from eval_core import metrics  # noqa: E402

PRED_DIR = ROOT / "outputs" / "predictions"
OUT = Path(__file__).resolve().parent
EMBARGO_END = pd.Timestamp("2026-02-27")
EVAL_START = pd.Timestamp("2015-01-01")
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
VAR_MODELS = ["garch_t", "qr_ar", "chronos_2", "chronos_2_lora", "chronos_2_full",
              "moirai2_small"]
COVERAGE = 0.95


def load(model: str, series: str, h: int) -> pd.DataFrame | None:
    p = PRED_DIR / f"{model}__{series}__h{h}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=["target_date"]).set_index("target_date")
    df = df.loc[(df.index >= EVAL_START) & (df.index <= EMBARGO_END)]
    assert df.empty or df.index.max() <= EMBARGO_END, "EMBARGO VIOLATION"
    return None if df.empty else df


def main() -> int:
    rows = []
    for model in VAR_MODELS:
        for series in SERIES:
            for h in HORIZONS:
                df = load(model, series, h)
                if df is None or "q05" not in df.columns:
                    continue
                if "q10" in df.columns and (df["q05"] == df["q10"]).all():
                    continue  # clamped tail, not a real 5% quantile
                j = df[["q05", "actual"]].dropna()
                if len(j) < 60:
                    continue
                # every h-th origin: retained forecasts share no target period
                thin = j.iloc[::h]
                for tag, sub in [("overlapping", j), ("non_overlapping", thin)]:
                    if len(sub) < 30:
                        continue
                    r = metrics.var_backtest(sub["q05"].values, sub["actual"].values,
                                             COVERAGE)
                    hits = int(round(r["hit_rate"] * r["n"]))
                    # Wilson interval on the exceedance rate — reported instead of
                    # leaning on a non-rejection.
                    n, p = r["n"], r["hit_rate"]
                    z = 1.959964
                    den = 1 + z * z / n
                    centre = (p + z * z / (2 * n)) / den
                    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
                    rows.append({
                        "model": model, "series": series, "h": h, "sample": tag,
                        "n": n, "exceedances": hits,
                        "exceedance_rate": round(p, 4), "expected": 0.05,
                        "ci_lo": round(max(centre - half, 0), 4),
                        "ci_hi": round(centre + half, 4),
                        "kupiec_p": r["kupiec_p"],
                    })
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "var_nonoverlap.csv", index=False)

    lines = ["# E2 — value-at-risk backtests on non-overlapping origins", "",
             f"Generated {datetime.now(timezone.utc).isoformat()} | 95% VaR from the 5% "
             "predictive quantile | embargoed sample only", "",
             "The non-overlapping sample keeps every h-th origin, so retained forecasts "
             "share no target period. Exceedance rates are reported first; the Kupiec "
             "p-value is secondary because failing to reject is not evidence of validity.",
             ""]
    for h in HORIZONS:
        lines += [f"## h = {h}", "",
                  "| model | sample | median n | median exceedance rate | median Kupiec p | "
                  "share rejecting at 5% |", "|---|---|---|---|---|---|"]
        for model in VAR_MODELS:
            for tag in ["overlapping", "non_overlapping"]:
                s = df[(df.model == model) & (df.h == h) & (df["sample"] == tag)]
                if s.empty:
                    continue
                rej = (s["kupiec_p"] < 0.05).mean()
                lines.append(f"| {model} | {tag} | {s['n'].median():.0f} | "
                             f"{s['exceedance_rate'].median():.4f} | "
                             f"{s['kupiec_p'].median():.3f} | {rej:.1f} |")
        lines.append("")
    (OUT / "results_var_nonoverlap.md").write_text("\n".join(lines) + "\n",
                                                   encoding="utf-8")
    print(f"written: {OUT / 'results_var_nonoverlap.md'} ({len(df)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
