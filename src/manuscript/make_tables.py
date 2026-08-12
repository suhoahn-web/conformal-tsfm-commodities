"""Build the manuscript tables from the evaluation CSVs.

Every table is generated here so that no number is ever transcribed by hand.
Output: outputs/tables/tableN_*.csv (machine-readable) and a single
outputs/tables/all_tables.md (for insertion into the manuscript).

Run:  python make_tables.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
P1 = ROOT / "analysis" / "phase1_local"
P2 = ROOT / "analysis" / "phase2_local"
HZ = ROOT / "analysis" / "final_hormuz"
OUT = ROOT / "outputs" / "tables"

LABEL = {
    "no_change": "No-change", "ar5_returns": "AR(5)", "lear_lite": "LEAR-lite",
    "garch_t": "GARCH-t", "qr_ar": "QR-AR",
    "chronos_bolt_small": "Chronos-Bolt (S)", "chronos_bolt_base": "Chronos-Bolt (B)",
    "chronos_2": "Chronos-2", "chronos_2_lora": "Chronos-2 + LoRA",
    "chronos_2_full": "Chronos-2 + full FT", "timesfm_25": "TimesFM 2.5",
    "moirai2_small": "Moirai-2 (S)",
}
ORDER = ["no_change", "ar5_returns", "lear_lite", "garch_t", "qr_ar", "timesfm_25",
         "moirai2_small", "chronos_2", "chronos_2_lora", "chronos_2_full",
         "chronos_bolt_small", "chronos_bolt_base"]
BAND = {"native80": "Native", "splitCP80": "Split conformal", "ACI80": "ACI",
        "CQR80": "CQR", "SPCI80": "SPCI-lite"}
SERIES_LABEL = {
    "wti_fut": "WTI crude", "brent_fut": "Brent crude", "natgas_fut": "Natural gas",
    "gold_fut": "Gold", "silver_fut": "Silver", "copper_fut": "Copper",
    "platinum_fut": "Platinum", "corn_fut": "Corn", "wheat_fut": "Wheat",
    "soybean_fut": "Soybeans",
}
tables: dict[str, tuple[str, pd.DataFrame]] = {}


def order_models(df: pd.DataFrame, col: str = "model") -> pd.DataFrame:
    present = [m for m in ORDER if m in set(df[col])]
    df = df.set_index(col).loc[present].reset_index()
    df[col] = df[col].map(LABEL)
    return df


def t1_data() -> None:
    import json
    meta = json.loads((ROOT / "data" / "raw" / "prices" / "retrieval_metadata.json")
                      .read_text(encoding="utf-8"))
    rows = []
    for r in meta["results"]:
        if not r["name"].endswith("_fut"):
            continue
        rows.append({"Commodity": SERIES_LABEL.get(r["name"], r["name"]),
                     "Symbol": r.get("symbol", ""), "First obs": r["first_date"],
                     "Last obs": r["last_date"], "N": r["rows"]})
    tables["table1_data"] = ("Table 1. Commodity futures panel.", pd.DataFrame(rows))


def t3_mspe() -> None:
    p = pd.read_csv(P1 / "points_phase1.csv")
    d = p[p.regime == "ALL"].groupby(["model", "h"])["mspe_ratio"].median().unstack()
    d.columns = [f"h = {c}" for c in d.columns]
    d = order_models(d.round(4).reset_index())
    tables["table3_mspe_ratio"] = (
        "Table 3. Median MSPE ratio against the no-change benchmark, 2015-01-01 to "
        "2026-02-27. Values below 1 indicate improvement over a random walk without "
        "drift. Medians are taken across the ten commodities.", d)


def t3_per_series() -> None:
    p = pd.read_csv(P1 / "points_phase1.csv")
    d = p[(p.h == 1) & (p.regime == "ALL")][
        ["model", "series", "mspe_ratio", "rmae", "sr", "pt_p", "dm_p"]]
    d = d.pivot(index="series", columns="model", values="mspe_ratio").round(3)
    d = d[[m for m in ORDER if m in d.columns]].rename(columns=LABEL)
    d.index = [SERIES_LABEL.get(s, s) for s in d.index]
    d.index.name = "Commodity"
    tables["table3_per_series"] = (
        "Table 3. Per-series MSPE ratio against the no-change benchmark at h = 1. The "
        "dispersion behind the medians of Table 2.", d.reset_index())


def t6_gw() -> None:
    gw = pd.read_csv(P2 / "gw_phase2.csv")
    d = (gw.assign(rej=gw["gw_p"] < 0.10).groupby(["model", "h"])["rej"].mean()
         .unstack().round(3))
    d.columns = [f"h = {c}" for c in d.columns]
    tables["table6_gw"] = (
        "Table 6. Giacomini-White tests of conditional predictive ability against the "
        "no-change benchmark: share of commodities rejecting equal predictive ability at "
        "the 10% level. In every rejection the loss differential favours the benchmark.",
        order_models(d.reset_index()))


def t11_var() -> None:
    v = pd.read_csv(P2 / "var_phase2.csv")
    d = (v[v.regime == "ALL"].assign(ok=v["kupiec_p"] > 0.05)
         .groupby(["model", "h"])["ok"].mean().unstack().round(2))
    d.columns = [f"h = {c}" for c in d.columns]
    tables["table11_var"] = (
        "Table 11. Share of commodities passing the Kupiec unconditional-coverage "
        "backtest of the 95% value-at-risk (p > 0.05), by model and horizon. Only models "
        "with an unclamped 5th percentile are shown.", order_models(d.reset_index()))


def t4_regime() -> None:
    p = pd.read_csv(P1 / "points_phase1.csv")
    d = (p[p.regime != "ALL"].groupby(["model", "regime", "h"])["mspe_ratio"]
         .median().unstack(["regime", "h"]).round(3))
    tables["table4_mspe_by_regime"] = (
        "Table 4. Median MSPE ratio by regime and horizon.", order_models(d.reset_index()))


def t5_mcs() -> None:
    mcs = pd.read_csv(P2 / "mcs_phase2.csv")
    freq = (mcs["survivors"].str.split(";").explode().value_counts() / len(mcs))
    first = mcs["eliminated_first3"].dropna().str.split(";").str[0].value_counts()
    d = pd.DataFrame({"MCS survival share": freq.round(3),
                      "First eliminated (cells)": first}).fillna(0)
    d.index.name = "model"
    d["First eliminated (cells)"] = d["First eliminated (cells)"].astype(int)
    tables["table5_mcs"] = (
        "Table 5. Model Confidence Set at the 10% level under squared loss, computed "
        "separately in each of the 30 series-horizon cells. Survival share is the "
        "fraction of cells in which the model cannot be distinguished from the best.",
        order_models(d.reset_index()))


def t6_intervals() -> None:
    iv = pd.read_csv(P1 / "intervals_phase1.csv")
    d = iv[(iv.nominal == 0.80) & (iv.regime != "ALL")]
    d = d.groupby(["band", "regime", "h"])["picp"].median().unstack(["regime", "h"]).round(3)
    d = d.reindex([b for b in BAND if b in d.index]).rename(index=BAND)
    d.index.name = "Interval construction"
    tables["table6_calibration"] = (
        "Table 6. Median empirical coverage of nominal 80% prediction intervals, by "
        "interval construction, regime and horizon, pooled across interval-producing "
        "models.", d.reset_index())


def t7_native_by_model() -> None:
    iv = pd.read_csv(P1 / "intervals_phase1.csv")
    d = iv[(iv.nominal == 0.80) & (iv.band == "native80") & (iv.regime != "ALL") & (iv.h == 5)]
    d = d.groupby(["model", "regime"])["picp"].median().unstack().round(3)
    d = d[["calm", "covid", "ukraine"]].rename(
        columns={"calm": "Calm", "covid": "COVID-19", "ukraine": "Ukraine war"})
    tables["table7_native_coverage"] = (
        "Table 7. Native 80% interval coverage at h = 5 by model and regime. QR-AR, a "
        "classical model, has the weakest crisis coverage in the panel; TimesFM 2.5 the "
        "strongest.", order_models(d.reset_index()))


def t8_width_crps() -> None:
    iv = pd.read_csv(P1 / "intervals_phase1.csv")
    w = (iv[(iv.nominal == 0.80) & (iv.regime == "calm") & (iv.h == 5)]
         .groupby("band")["width"].median().round(2))
    w = w.reindex([b for b in BAND if b in w.index]).rename(index=BAND)
    crps = pd.read_csv(P1 / "crps_phase1.csv")
    c = crps[crps.h == 1].groupby("model")["crps_ALL"].mean().round(3)
    tables["table8_width"] = (
        "Table 8. Median interval width in calm periods at h = 5 (price units).",
        w.reset_index().rename(columns={"band": "Construction", "width": "Median width"}))
    tables["table9_crps"] = (
        "Table 9. Mean CRPS at h = 1 across the ten commodities. Lower is better.",
        order_models(c.reset_index()))


def t10_finetune() -> None:
    p = pd.read_csv(P1 / "points_phase1.csv")
    iv = pd.read_csv(P1 / "intervals_phase1.csv")
    v = pd.read_csv(P2 / "var_phase2.csv")
    variants = ["chronos_2", "chronos_2_lora", "chronos_2_full"]
    rows = []
    for m in variants:
        acc = p[(p.model == m) & (p.regime == "ALL")].groupby("h")["mspe_ratio"].median()
        cov = iv[(iv.model == m) & (iv.band == "native80") & (iv.h == 5)]
        cov = cov.groupby("regime")["picp"].median()
        var1 = v[(v.model == m) & (v.h == 1) & (v.regime == "ALL")]
        rows.append({
            "model": m,
            "MSPE h=1": round(acc.get(1, float("nan")), 4),
            "MSPE h=5": round(acc.get(5, float("nan")), 4),
            "MSPE h=22": round(acc.get(22, float("nan")), 4),
            "PICP calm": round(cov.get("calm", float("nan")), 3),
            "PICP COVID": round(cov.get("covid", float("nan")), 3),
            "PICP Ukraine": round(cov.get("ukraine", float("nan")), 3),
            "VaR Kupiec pass (h=1)": round((var1["kupiec_p"] > 0.05).mean(), 2),
        })
    tables["table10_finetune"] = (
        "Table 10. The fine-tuning trade-off for Chronos-2: point accuracy, native 80% "
        "interval coverage at h = 5, and the share of commodities passing the Kupiec "
        "backtest of the 95% value-at-risk at h = 1.", order_models(pd.DataFrame(rows)))


def t11_hormuz() -> None:
    if not (HZ / "hormuz_points.csv").exists():
        return
    p = pd.read_csv(HZ / "hormuz_points.csv")
    d = p.groupby(["model", "h"])["mspe_ratio"].median().unstack().round(4)
    d.columns = [f"h = {c}" for c in d.columns]
    tables["table11_hormuz_points"] = (
        "Table 11. Sealed holdout: median MSPE ratio against the no-change benchmark in "
        "the Iran-Hormuz window, 2026-02-28 to 2026-07-31 (106 origins per cell). "
        "Evaluated once, after all specifications were frozen.",
        order_models(d.reset_index()))
    iv = pd.read_csv(HZ / "hormuz_intervals.csv")
    b = iv[iv.nominal == 0.80]
    b = b.groupby(["band", "h"])["picp"].median().unstack().round(3)
    b = b.reindex([x for x in BAND if x in b.index]).rename(index=BAND)
    b.columns = [f"h = {c}" for c in b.columns]
    b.index.name = "Interval construction"
    tables["table12_hormuz_intervals"] = (
        "Table 12. Sealed holdout: median coverage of nominal 80% prediction intervals in "
        "the Iran-Hormuz window, pooled across models.", b.reset_index())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (t1_data, t3_mspe, t3_per_series, t4_regime, t5_mcs, t6_gw, t6_intervals,
               t7_native_by_model, t8_width_crps, t11_var, t10_finetune, t11_hormuz):
        fn()
    md = ["# Manuscript tables (generated — do not edit by hand)\n"]
    for name, (caption, df) in tables.items():
        df.to_csv(OUT / f"{name}.csv", index=False)
        md += [f"\n## {caption}\n", df.to_markdown(index=False)]
    (OUT / "all_tables.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{len(tables)} tables written to {OUT}")
    for name, (_, df) in tables.items():
        print(f"  {name}: {df.shape[0]} rows x {df.shape[1]} cols")


if __name__ == "__main__":
    main()
