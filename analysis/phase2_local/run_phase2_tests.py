"""Phase 2 statistical tests: MCS over all point models, GW vs no-change,
and 95% VaR backtests from q05 forecasts. EMBARGO: hard stop 2026-02-27.

Run:  python run_phase2_tests.py
Output: analysis/phase2_local/results_phase2_tests.md (+ CSVs)
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from eval_core import metrics  # noqa: E402

PRED = ROOT / "outputs" / "predictions"
OUT = Path(__file__).resolve().parent
EMBARGO_END = pd.Timestamp("2026-02-27")
EVAL_START = pd.Timestamp("2015-01-01")
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
POINT_MODELS = ["no_change", "ar5_returns", "lear_lite", "garch_t", "qr_ar",
                "chronos_bolt_small", "chronos_bolt_base", "chronos_2",
                "chronos_2_lora", "chronos_2_full", "timesfm_25", "moirai2_small"]
VAR_MODELS = ["garch_t", "qr_ar", "chronos_2", "chronos_2_lora", "chronos_2_full",
              "moirai2_small"]  # models with a REAL q05
REGIMES = {"covid": ("2020-02-20", "2020-08-31"), "ukraine": ("2022-02-24", "2022-08-31")}


def load(model: str, series: str, h: int) -> pd.DataFrame | None:
    p = PRED / f"{model}__{series}__h{h}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=["target_date"]).set_index("target_date")
    df = df.loc[(df.index >= EVAL_START) & (df.index <= EMBARGO_END)]
    assert df.index.max() <= EMBARGO_END
    return df


def main() -> None:
    mcs_rows, gw_rows, var_rows, missing = [], [], [], []
    for series in SERIES:
        for h in HORIZONS:
            frames = {}
            for m in POINT_MODELS:
                df = load(m, series, h)
                if df is None:
                    missing.append(f"{m}__{series}__h{h}")
                    continue
                frames[m] = df["point"]
            if "no_change" not in frames or len(frames) < 3:
                continue
            actual = load("no_change", series, h)["actual"]
            joined = pd.DataFrame(frames).join(actual.rename("y"), how="inner").dropna()
            losses = np.column_stack([
                (joined[m] - joined["y"]).values ** 2 for m in frames
            ])
            mcs = metrics.model_confidence_set(losses, list(frames), alpha=0.10,
                                               n_boot=1000, block=max(22, h))
            mcs_rows.append({"series": series, "h": h,
                             "survivors": ";".join(mcs["survivors"]),
                             "n_survivors": len(mcs["survivors"]),
                             "eliminated_first3": ";".join(mcs["eliminated"][:3])})
            e_nc = (joined["no_change"] - joined["y"]).values
            for m in frames:
                if m == "no_change":
                    continue
                gw = metrics.giacomini_white((joined[m] - joined["y"]).values, e_nc, h=h)
                gw_rows.append({"series": series, "h": h, "model": m,
                                "gw_stat": None if np.isnan(gw["stat"]) else round(gw["stat"], 2),
                                "gw_p": None if gw.get("pvalue") is None or np.isnan(gw["pvalue"])
                                else round(gw["pvalue"], 4)})
            for m in VAR_MODELS:
                df = load(m, series, h)
                if df is None or "q05" not in df.columns:
                    continue
                if "q10" in df.columns and (df["q05"] == df["q10"]).all():
                    continue  # clamped tail — not a real q05
                j = df[["q05", "actual"]].dropna()
                res = metrics.var_backtest(j["q05"].values, j["actual"].values, 0.95)
                row = {"series": series, "h": h, "model": m, "regime": "ALL", **res}
                var_rows.append(row)
                for reg, (a, b) in REGIMES.items():
                    sub = j.loc[a:b]
                    if len(sub) >= 60:
                        var_rows.append({"series": series, "h": h, "model": m,
                                         "regime": reg,
                                         **metrics.var_backtest(sub["q05"].values,
                                                                sub["actual"].values, 0.95)})
    mcs_df, gw_df, var_df = map(pd.DataFrame, (mcs_rows, gw_rows, var_rows))
    md = [
        "# Phase 2 Tests — MCS / GW / VaR (EMBARGOED: no Hormuz)",
        f"\nGenerated {datetime.now(timezone.utc).isoformat()} | missing caches: {len(missing)}",
        "\n## MCS survivors per series x h (10% level, squared loss)\n",
        mcs_df.to_markdown(index=False) if len(mcs_df) else "(none)",
        "\n## MCS survivor frequency by model\n",
    ]
    if len(mcs_df):
        freq = (mcs_df["survivors"].str.split(";").explode().value_counts()
                / len(mcs_df)).round(3)
        md.append(freq.to_markdown())
    md += ["\n## GW conditional-ability rejections vs no-change (p<0.10 share by model)\n"]
    if len(gw_df):
        gw_share = gw_df.assign(rej=gw_df["gw_p"] < 0.10).groupby("model")["rej"].mean().round(3)
        md.append(gw_share.to_markdown())
    md += ["\n## 95% VaR backtest — share of series passing Kupiec (p>0.05) by model x regime\n"]
    if len(var_df):
        piv = (var_df.assign(ok=var_df["kupiec_p"] > 0.05)
               .groupby(["model", "regime", "h"])["ok"].mean().round(3).unstack("h"))
        md.append(piv.to_markdown())
    (OUT / "results_phase2_tests.md").write_text("\n".join(md), encoding="utf-8")
    for name, df in [("mcs", mcs_df), ("gw", gw_df), ("var", var_df)]:
        df.to_csv(OUT / f"{name}_phase2.csv", index=False)
    print(f"mcs {len(mcs_df)} | gw {len(gw_df)} | var {len(var_df)} | missing {len(missing)}")


if __name__ == "__main__":
    main()
