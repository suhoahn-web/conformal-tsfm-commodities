"""FINAL Hormuz-window evaluation — SINGLE-USE, pre-registered.

This script evaluates the sealed holdout (2026-02-28 .. 2026-07-31) exactly
once, after all model predictions are cached and all specifications frozen.

SAFEGUARDS
1. Refuses to run unless the file `HORMUZ_UNSEAL_APPROVED.txt` exists in this
   directory, containing the user's approval sentence and a date.
2. Refuses to run twice: writes `HORMUZ_EVALUATED.marker` on completion and
   aborts if it already exists.
3. Metric set below is frozen per RESEARCH_PLAN_v1 §3.2; do not extend after
   unsealing.

Run:  python run_hormuz_final.py
Output: results_hormuz_final.md + hormuz_{points,intervals,var}.csv
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from eval_core import conformal, metrics  # noqa: E402

PRED = ROOT / "outputs" / "predictions"
OUT = Path(__file__).resolve().parent
HORMUZ_START, HORMUZ_END = pd.Timestamp("2026-02-28"), pd.Timestamp("2026-07-31")
CAL_SIZE = 250
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
POINT_MODELS = ["ar5_returns", "lear_lite", "garch_t", "qr_ar",
                "chronos_bolt_small", "chronos_bolt_base", "chronos_2",
                "chronos_2_lora", "chronos_2_full", "timesfm_25", "moirai2_small"]
INTERVAL_MODELS = ["garch_t", "qr_ar", "chronos_bolt_small", "chronos_bolt_base",
                   "chronos_2", "chronos_2_lora", "chronos_2_full",
                   "timesfm_25", "moirai2_small"]
VAR_MODELS = ["garch_t", "qr_ar", "chronos_2", "chronos_2_lora", "chronos_2_full",
              "moirai2_small"]


def guard() -> None:
    approval = OUT / "HORMUZ_UNSEAL_APPROVED.txt"
    marker = OUT / "HORMUZ_EVALUATED.marker"
    if marker.exists():
        sys.exit("ABORT: Hormuz window already evaluated once. No second pass.")
    if not approval.exists():
        sys.exit("ABORT: HORMUZ_UNSEAL_APPROVED.txt not found — user approval required.")
    print("Approval found:", approval.read_text(encoding="utf-8").strip()[:120])


def load_full(model: str, series: str, h: int) -> pd.DataFrame | None:
    p = PRED / f"{model}__{series}__h{h}.csv"
    if not p.exists():
        return None
    return pd.read_csv(p, parse_dates=["target_date"]).set_index("target_date")


def main() -> None:
    guard()
    pt_rows, iv_rows, var_rows, missing = [], [], [], []
    for series in SERIES:
        for h in HORIZONS:
            nc = load_full("no_change", series, h)
            if nc is None:
                missing.append(f"no_change__{series}__h{h}")
                continue
            nc_w = nc.loc[HORMUZ_START:HORMUZ_END]
            for m in POINT_MODELS:
                df = load_full(m, series, h)
                if df is None:
                    missing.append(f"{m}__{series}__h{h}")
                    continue
                j = df[["point", "actual"]].join(nc["point"].rename("nc"), how="inner")
                w = j.loc[HORMUZ_START:HORMUZ_END].dropna()
                if len(w) < 30:
                    continue
                y, f, b = w["actual"].values, w["point"].values, w["nc"].values
                r = metrics.mspe_ratio(f, b, y)
                dm = metrics.diebold_mariano(f - y, b - y, h=h)
                pt_rows.append({
                    "model": m, "series": series, "h": h, "n": len(w),
                    "mspe_ratio": round(r["mspe_ratio"], 4),
                    "rmae": round(metrics.rmae(f, b, y), 4),
                    "dm_p": None if np.isnan(dm["p_onesided"]) else round(dm["p_onesided"], 3),
                })
            for m in INTERVAL_MODELS:
                df = load_full(m, series, h)
                if df is None:
                    continue
                fc, ac = df["point"], df["actual"]
                variants = {}
                if {"q10", "q90"}.issubset(df.columns):
                    variants["native80"] = (df["q10"], df["q90"], 0.20)
                for alpha, tag in [(0.20, "80"), (0.10, "90")]:
                    for wn, wrap in [("splitCP", conformal.split_conformal),
                                     ("ACI", conformal.aci), ("SPCI", conformal.spci_lite)]:
                        iv = wrap(fc, ac, alpha=alpha, cal_size=CAL_SIZE, horizon=h)
                        variants[f"{wn}{tag}"] = (iv["lo"], iv["hi"], alpha)
                if {"q10", "q90"}.issubset(df.columns):
                    iv = conformal.cqr(df["q10"], df["q90"], ac, alpha=0.20, cal_size=CAL_SIZE, horizon=h)
                    variants["CQR80"] = (iv["lo"], iv["hi"], 0.20)
                for vname, (lo, hi, alpha) in variants.items():
                    j = pd.concat({"lo": lo, "hi": hi, "y": ac}, axis=1)
                    w = j.loc[HORMUZ_START:HORMUZ_END].dropna()
                    if len(w) < 30:
                        continue
                    im = metrics.interval_metrics(w["lo"].values, w["hi"].values,
                                                  w["y"].values, alpha)
                    iv_rows.append({"model": m, "series": series, "h": h, "band": vname,
                                    "nominal": round(1 - alpha, 2),
                                    "picp": round(im["picp"], 3),
                                    "winkler": round(im["winkler"], 3), "n": len(w)})
            for m in VAR_MODELS:
                df = load_full(m, series, h)
                if df is None or "q05" not in df.columns:
                    continue
                if "q10" in df.columns and (df["q05"] == df["q10"]).all():
                    continue
                w = df[["q05", "actual"]].loc[HORMUZ_START:HORMUZ_END].dropna()
                if len(w) >= 60:
                    var_rows.append({"model": m, "series": series, "h": h,
                                     **metrics.var_backtest(w["q05"].values,
                                                            w["actual"].values, 0.95)})
    pts, ivs, vars_ = map(pd.DataFrame, (pt_rows, iv_rows, var_rows))
    md = [
        "# FINAL Hormuz Window Results (2026-02-28 .. 2026-07-31) — single pass",
        f"\nGenerated {datetime.now(timezone.utc).isoformat()} | missing: {len(missing)}",
        "\n## Point: median MSPE ratio vs no-change\n",
        pts.groupby(["model", "h"])["mspe_ratio"].median().unstack().round(4).to_markdown()
        if len(pts) else "(none)",
        "\n## Intervals: median PICP by band (nominal 0.80/0.90)\n",
        ivs.groupby(["model", "band", "h"])["picp"].median().unstack().round(3).to_markdown()
        if len(ivs) else "(none)",
        "\n## 95% VaR: Kupiec pass share by model\n",
        vars_.assign(ok=vars_["kupiec_p"] > 0.05).groupby(["model", "h"])["ok"].mean()
        .round(3).unstack().to_markdown() if len(vars_) else "(none)",
    ]
    (OUT / "results_hormuz_final.md").write_text("\n".join(md), encoding="utf-8")
    pts.to_csv(OUT / "hormuz_points.csv", index=False)
    ivs.to_csv(OUT / "hormuz_intervals.csv", index=False)
    vars_.to_csv(OUT / "hormuz_var.csv", index=False)
    (OUT / "HORMUZ_EVALUATED.marker").write_text(
        datetime.now(timezone.utc).isoformat(), encoding="utf-8")
    print(f"FINAL: points {len(pts)} | intervals {len(ivs)} | var {len(vars_)} | missing {len(missing)}")


if __name__ == "__main__":
    main()
