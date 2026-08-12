"""Phase 1 evaluation: regime-segmented metrics from the prediction cache.

EMBARGO ENFORCEMENT: evaluation hard-stops at 2026-02-27. The Hormuz window
(2026-02-28..2026-07-31) is excluded at load time and an assertion guards every
metric input. The final Hormuz pass will be a separate, single-use script run
once after all specifications are frozen (they now are) and all models are in.

Run:  python evaluate_phase1.py
Output: analysis/phase1_local/results_phase1.md
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from eval_core import conformal, metrics  # noqa: E402

PRED_DIR = ROOT / "outputs" / "predictions"
OUT = Path(__file__).resolve().parent
EMBARGO_END = pd.Timestamp("2026-02-27")  # inclusive last evaluable date
EVAL_START = pd.Timestamp("2015-01-01")
REGIMES = {
    "covid": ("2020-02-20", "2020-08-31"),
    "ukraine": ("2022-02-24", "2022-08-31"),
}
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
CAL_SIZE = 250
POINT_MODELS = ["ar5_returns", "lear_lite", "garch_t", "qr_ar",
                "chronos_bolt_small", "chronos_bolt_base",
                "chronos_2", "chronos_2_lora", "chronos_2_full",
                "timesfm_25", "moirai2_small"]
INTERVAL_MODELS = ["garch_t", "qr_ar", "chronos_bolt_small", "chronos_bolt_base",
                   "chronos_2", "chronos_2_lora", "chronos_2_full",
                   "timesfm_25", "moirai2_small"]


def load_cache(model: str, series: str, h: int) -> pd.DataFrame | None:
    path = PRED_DIR / f"{model}__{series}__h{h}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=["target_date"]).set_index("target_date")
    df = df.loc[(df.index >= EVAL_START) & (df.index <= EMBARGO_END)]
    assert df.index.max() <= EMBARGO_END, "EMBARGO VIOLATION"
    return df


def regime_label(idx: pd.DatetimeIndex) -> pd.Series:
    lab = pd.Series("calm", index=idx)
    for name, (a, b) in REGIMES.items():
        lab.loc[(idx >= a) & (idx <= b)] = name
    return lab


def eval_point(model: str, series: str, h: int, missing: list) -> list[dict]:
    m_df, nc_df = load_cache(model, series, h), load_cache("no_change", series, h)
    if m_df is None or nc_df is None:
        missing.append(f"{model}__{series}__h{h}")
        return []
    j = m_df[["point", "actual"]].join(nc_df["point"].rename("nc"), how="inner").dropna()
    labels = regime_label(j.index)
    rows = []
    for reg in ["ALL", "calm", "covid", "ukraine"]:
        sub = j if reg == "ALL" else j[labels == reg]
        if len(sub) < 30:
            continue
        y, f, nc = sub["actual"].values, sub["point"].values, sub["nc"].values
        r = metrics.mspe_ratio(f, nc, y)
        dm = metrics.diebold_mariano(f - y, nc - y, h=h)
        sr = metrics.success_ratio(f - nc, y - nc)
        pt = metrics.pesaran_timmermann(f - nc, y - nc)
        rows.append({
            "model": model, "series": series, "h": h, "regime": reg, "n": len(sub),
            "mspe_ratio": round(r["mspe_ratio"], 4),
            "rmae": round(metrics.rmae(f, nc, y), 4),
            "sr": round(sr, 3),
            "pt_p": None if np.isnan(pt["pvalue"]) else round(pt["pvalue"], 3),
            "dm_p": None if np.isnan(dm["p_onesided"]) else round(dm["p_onesided"], 3),
        })
    return rows


# Quantile levels every model in the panel can express. Chronos-Bolt clamps to
# [0.1, 0.9] and TimesFM emits deciles only, so this intersection is the only
# grid on which a CRPS approximation is comparable ACROSS models. Using each
# model's own grid makes the score a function of grid size rather than of
# distributional quality — the defect this constant exists to prevent.
COMMON_Q = ["q10", "q25", "q50", "q75", "q90"]


def crps_by_regime(df: pd.DataFrame) -> dict:
    """Quantile-grid CRPS approximation (2x mean pinball) on a COMMON grid.

    Restricted to COMMON_Q so that scores are comparable across models with
    different native quantile heads. Models missing a level are skipped
    entirely rather than scored on a different grid.
    """
    valid = [c for c in COMMON_Q if c in df.columns]
    if len(valid) < len(COMMON_Q):
        return {}
    levels = [int(c[1:]) / 100 for c in valid]
    y = df["actual"].values
    pin = np.zeros(len(df))
    for c, q in zip(valid, levels):
        diff = y - df[c].values
        pin += np.maximum(q * diff, (q - 1) * diff)
    crps = pd.Series(2 * pin / len(valid), index=df.index)
    lab = regime_label(df.index)
    out = {"crps_ALL": crps.mean()}
    for reg in ["calm", "covid", "ukraine"]:
        sub = crps[lab == reg]
        if len(sub) >= 30:
            out[f"crps_{reg}"] = sub.mean()
    return {k: round(v, 4) for k, v in out.items()} | {"n_valid_quantiles": len(valid)}


def eval_intervals(model: str, series: str, h: int, missing: list) -> list[dict]:
    df = load_cache(model, series, h)
    if df is None:
        missing.append(f"{model}__{series}__h{h}")
        return []
    labels = regime_label(df.index)
    rows = []
    variants = {}
    if {"q10", "q90"}.issubset(df.columns):
        variants["native80"] = (df["q10"], df["q90"], 0.20)
    if {"q05", "q95"}.issubset(df.columns) and not (df["q05"] == df["q10"]).all():
        # real 90% band (only models without quantile clamping, e.g. Chronos-2)
        variants["native90"] = (df["q05"], df["q95"], 0.10)
    fc, ac = df["point"], df["actual"]
    for alpha, tag in [(0.20, "80"), (0.10, "90")]:
        for wrap_name, wrap in [("splitCP", conformal.split_conformal), ("ACI", conformal.aci),
                                ("SPCI", conformal.spci_lite)]:
            iv = wrap(fc, ac, alpha=alpha, cal_size=CAL_SIZE, horizon=h)
            variants[f"{wrap_name}{tag}"] = (iv["lo"], iv["hi"], alpha)
    # CQR conformalizes the model's own quantile band (only where band is real)
    if "native80" in variants:
        iv = conformal.cqr(df["q10"], df["q90"], ac, alpha=0.20, cal_size=CAL_SIZE, horizon=h)
        variants["CQR80"] = (iv["lo"], iv["hi"], 0.20)
    if "native90" in variants:
        iv = conformal.cqr(df["q05"], df["q95"], ac, alpha=0.10, cal_size=CAL_SIZE, horizon=h)
        variants["CQR90"] = (iv["lo"], iv["hi"], 0.10)
    for vname, (lo, hi, alpha) in variants.items():
        j = pd.concat({"lo": lo, "hi": hi, "y": ac}, axis=1).dropna()
        lab = regime_label(j.index)
        for reg in ["ALL", "calm", "covid", "ukraine"]:
            sub = j if reg == "ALL" else j[lab == reg]
            if len(sub) < 30:
                continue
            im = metrics.interval_metrics(sub["lo"].values, sub["hi"].values, sub["y"].values, alpha)
            rows.append({
                "model": model, "series": series, "h": h, "band": vname,
                "nominal": round(1 - alpha, 2), "regime": reg,
                "n": len(sub), "picp": round(im["picp"], 3),
                "winkler": round(im["winkler"], 3),
                "width": round(im["mean_width"], 3),
            })
    return rows


def main() -> None:
    missing: list[str] = []
    point_rows, iv_rows, crps_rows = [], [], []
    for model in INTERVAL_MODELS:
        for series in SERIES:
            for h in HORIZONS:
                df = load_cache(model, series, h)
                if df is not None and any(c.startswith("q") for c in df.columns):
                    stats = crps_by_regime(df)
                    if stats:
                        crps_rows.append({"model": model, "series": series, "h": h, **stats})
    for model in POINT_MODELS:
        for series in SERIES:
            for h in HORIZONS:
                point_rows.extend(eval_point(model, series, h, missing))
    for model in INTERVAL_MODELS:
        for series in SERIES:
            for h in HORIZONS:
                iv_rows.extend(eval_intervals(model, series, h, missing))
    points = pd.DataFrame(point_rows)
    ivs = pd.DataFrame(iv_rows)

    md = [
        "# Phase 1 Results — Local Models (EMBARGOED: no Hormuz window)",
        f"\nGenerated {datetime.now(timezone.utc).isoformat()} | eval {EVAL_START.date()}..{EMBARGO_END.date()} "
        f"| regimes: calm / covid / ukraine | cal_size={CAL_SIZE}",
        f"\nMissing caches ({len(missing)}): {', '.join(missing) if missing else 'none'}",
    ]
    if len(points):
        md += ["\n## Point forecasts vs no-change — median MSPE ratio by model x regime x h\n",
               points.groupby(["model", "regime", "h"])["mspe_ratio"].median().unstack("h")
                     .round(4).to_markdown(),
               "\n### Per-series detail (h=1, ALL)\n",
               points[(points.h == 1) & (points.regime == "ALL")]
                   .drop(columns=["h", "regime"]).to_markdown(index=False)]
    if len(ivs):
        md += ["\n## Interval calibration — median PICP (nominal 0.80) by band x regime x h\n",
               ivs.groupby(["model", "band", "regime", "h"])["picp"].median().unstack("h")
                  .round(3).to_markdown()]
    crps_df = pd.DataFrame(crps_rows)
    if len(crps_df):
        md += ["\n## CRPS by model (mean over series, per regime; lower = better)\n",
               crps_df.groupby(["model", "h"])[
                   [c for c in crps_df.columns if c.startswith("crps_")]
               ].mean().round(3).to_markdown()]
        crps_df.to_csv(OUT / "crps_phase1.csv", index=False)
    (OUT / "results_phase1.md").write_text("\n".join(md), encoding="utf-8")
    points.to_csv(OUT / "points_phase1.csv", index=False)
    ivs.to_csv(OUT / "intervals_phase1.csv", index=False)
    print(f"point rows: {len(points)}, interval rows: {len(ivs)}, crps rows: {len(crps_df)}, missing: {len(missing)}")
    print("written: results_phase1.md")


if __name__ == "__main__":
    main()
