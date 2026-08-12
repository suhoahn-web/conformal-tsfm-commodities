"""Recompute CRPS on the grid EVERY model can express: {0.10, 0.50, 0.90}.

Chronos-Bolt clamps to [0.1, 0.9] and emits {q10,q25,q50,q75,q90}; TimesFM 2.5
emits deciles and therefore has no q25/q75. Their intersection is the only grid
on which a quantile-based CRPS approximation compares like with like — a wider
grid silently drops whichever model cannot express it (TimesFM was excluded
entirely by the previous {q10,q25,q50,q75,q90} choice).

This rewrites crps_phase1.csv only; nothing else in the evaluation depends on it.
Run:  python recompute_crps.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

PRED = ROOT / "outputs" / "predictions"
OUT = Path(__file__).resolve().parent
EMBARGO_END = pd.Timestamp("2026-02-27")
EVAL_START = pd.Timestamp("2015-01-01")
COMMON_Q = ["q10", "q50", "q90"]
LEVELS = [0.10, 0.50, 0.90]
REGIMES = {"covid": ("2020-02-20", "2020-08-31"), "ukraine": ("2022-02-24", "2022-08-31")}
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
MODELS = ["garch_t", "qr_ar", "chronos_bolt_small", "chronos_bolt_base", "chronos_2",
          "chronos_2_lora", "chronos_2_full", "timesfm_25", "moirai2_small"]


def regime_label(idx: pd.DatetimeIndex) -> pd.Series:
    lab = pd.Series("calm", index=idx)
    for name, (a, b) in REGIMES.items():
        lab.loc[(idx >= a) & (idx <= b)] = name
    return lab


def main() -> None:
    rows, skipped = [], []
    for model in MODELS:
        for series in SERIES:
            for h in HORIZONS:
                path = PRED / f"{model}__{series}__h{h}.csv"
                if not path.exists():
                    continue
                df = pd.read_csv(path, parse_dates=["target_date"]).set_index("target_date")
                df = df.loc[(df.index >= EVAL_START) & (df.index <= EMBARGO_END)]
                if not set(COMMON_Q).issubset(df.columns):
                    skipped.append(f"{model}__{series}__h{h}")
                    continue
                y = df["actual"].values
                pin = np.zeros(len(df))
                for c, q in zip(COMMON_Q, LEVELS):
                    diff = y - df[c].values
                    pin += np.maximum(q * diff, (q - 1) * diff)
                crps = pd.Series(2 * pin / len(COMMON_Q), index=df.index)
                lab = regime_label(df.index)
                row = {"model": model, "series": series, "h": h,
                       "crps_ALL": round(crps.mean(), 4), "n_valid_quantiles": len(COMMON_Q)}
                for reg in ["calm", "covid", "ukraine"]:
                    sub = crps[lab == reg]
                    if len(sub) >= 30:
                        row[f"crps_{reg}"] = round(sub.mean(), 4)
                rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "crps_phase1.csv", index=False)
    print(f"crps rows: {len(out)} | skipped (missing common grid): {len(skipped)}")
    print(out[out.h == 1].groupby("model")["crps_ALL"].mean().sort_values().round(3).to_string())


if __name__ == "__main__":
    main()
