"""Smoke test A (local, CPU): end-to-end validation of the evaluation pipeline.

3 series (WTI/gold/copper futures), h=1 and h=5, test year 2023 (calm regime —
deliberately NOT a crisis window and far from the sacred Hormuz holdout).
Models: no-change benchmark, recursive AR(5); intervals: split conformal + ACI
on both models' forecasts. Purpose: validate code, alignment, and metric
plumbing — NOT to produce paper results.

Run:  python run_smoke_a.py
Outputs: analysis/smoke_a/results_smoke_a.md + forecasts CSV (immutable).
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from eval_core import baselines, conformal, metrics  # noqa: E402

PRICES = ROOT / "data" / "raw" / "prices"
OUT = Path(__file__).resolve().parent
SERIES = ["wti_fut", "gold_fut", "copper_fut"]
HORIZONS = [1, 5]
TEST_START, TEST_END = "2023-01-01", "2023-12-31"
CAL_SIZE = 250
ALPHAS = [0.20, 0.05]
np.random.seed(20260811)


def load(name: str) -> pd.Series:
    df = pd.read_csv(PRICES / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def evaluate(name: str, h: int) -> list[dict]:
    prices = load(name)
    origins = prices.loc["2010-01-01":TEST_END].index
    nc = baselines.no_change(prices, h)
    ar = baselines.recursive_ar_forecast(prices, h, origins, p=5)

    frame = pd.concat({"nc": nc, "ar": ar, "y": prices}, axis=1).dropna()
    test = frame.loc[TEST_START:TEST_END]
    if len(test) < 200:
        raise ValueError(f"{name} h={h}: only {len(test)} test points — alignment bug?")

    rows = []
    y, ncf, arf = test["y"].values, test["nc"].values, test["ar"].values
    m = metrics.mspe_ratio(arf, ncf, y)
    prev = prices.reindex(test.index.map(lambda d: prices.index[prices.index.get_loc(d) - h]))
    d_actual = y - prev.values
    d_pred = arf - prev.values
    sr = metrics.success_ratio(d_pred, d_actual)
    pt = metrics.pesaran_timmermann(d_pred, d_actual)
    dm = metrics.diebold_mariano(arf - y, ncf - y, h=h)
    rows.append({
        "series": name, "h": h, "model": "AR(5) vs no-change",
        "mspe_ratio": round(m["mspe_ratio"], 4),
        "rmae": round(metrics.rmae(arf, ncf, y), 4),
        "success_ratio": round(sr, 3),
        "pt_pvalue": None if np.isnan(pt["pvalue"]) else round(pt["pvalue"], 3),
        "dm_p_onesided": None if np.isnan(dm["p_onesided"]) else round(dm["p_onesided"], 3),
    })

    for model_name, fc_full in [("no-change", pd.concat([nc], axis=1).iloc[:, 0]),
                                ("AR(5)", pd.concat([ar], axis=1).iloc[:, 0])]:
        actual_full = prices.reindex(fc_full.index)
        for alpha in ALPHAS:
            for wrap_name, wrap in [("splitCP", conformal.split_conformal), ("ACI", conformal.aci)]:
                iv = wrap(fc_full, actual_full, alpha, CAL_SIZE)
                iv_test = iv.loc[TEST_START:TEST_END]
                ym = prices.reindex(iv_test.index).values
                im = metrics.interval_metrics(iv_test["lo"].values, iv_test["hi"].values, ym, alpha)
                rows.append({
                    "series": name, "h": h, "model": f"{model_name}+{wrap_name}",
                    "nominal_cov": im["nominal"], "picp": round(im["picp"], 3),
                    "mean_width": round(im["mean_width"], 2),
                    "winkler": round(im["winkler"], 2),
                })
    # immutable forecast cache
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cache = OUT / f"forecasts_{name}_h{h}_{stamp}.csv"
    test.to_csv(cache)
    return rows


def main() -> None:
    all_rows = []
    for name in SERIES:
        for h in HORIZONS:
            all_rows.extend(evaluate(name, h))
            print(f"done {name} h={h}")
    df = pd.DataFrame(all_rows)
    md = [
        "# Smoke Test A — Evaluation Pipeline Validation",
        f"\nGenerated {datetime.now(timezone.utc).isoformat()}  |  test window {TEST_START}..{TEST_END} "
        f"(calm regime, NOT the holdout)  |  cal_size={CAL_SIZE}",
        "\n## Point forecasts (AR(5) vs no-change benchmark)\n",
        df[df["model"].str.contains("vs")].dropna(axis=1, how="all").to_markdown(index=False),
        "\n## Conformal intervals\n",
        df[~df["model"].str.contains("vs")].dropna(axis=1, how="all").to_markdown(index=False),
        "\n## Pass criteria",
        "- [ ] MSPE ratios near 1.0 (daily prices ~ random walk — AR should NOT dominate; a ratio far below 1 signals leakage)",
        "- [ ] split-CP and ACI PICP within ~3pp of nominal in this calm window",
        "- [ ] no exceptions, no silent NaN drops (enforced in metrics module)",
    ]
    (OUT / "results_smoke_a.md").write_text("\n".join(md), encoding="utf-8")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
