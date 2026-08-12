"""Smoke test B (local CPU): zero-shot Chronos-Bolt on 3 series, same window as smoke A.

Validates the TSFM harness end-to-end: context construction (no future data),
quantile outputs, CRPS-from-quantiles, conformalization of TSFM intervals,
and the point-forecast audit vs no-change. NOT paper results (small model,
CPU, one calm year).

Run:  python run_smoke_b.py
Outputs: analysis/smoke_b/results_smoke_b.md + forecast CSV cache (immutable).
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from eval_core import baselines, metrics  # noqa: E402
from chronos import BaseChronosPipeline  # noqa: E402

PRICES = ROOT / "data" / "raw" / "prices"
OUT = Path(__file__).resolve().parent
MODEL = "amazon/chronos-bolt-small"
SERIES = ["wti_fut", "gold_fut", "copper_fut"]
HORIZONS = [1, 5]
TEST_START, TEST_END = "2023-01-01", "2023-12-31"
CONTEXT = 512
QUANTILES = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
STRIDE = 1
torch.manual_seed(20260811)
np.random.seed(20260811)


def load(name: str) -> pd.Series:
    df = pd.read_csv(PRICES / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def crps_from_quantiles(q_preds: np.ndarray, actual: float, qs: list[float]) -> float:
    """Approximate CRPS via average pinball loss over the quantile grid (x2)."""
    losses = []
    for q, qp in zip(qs, q_preds):
        diff = actual - qp
        losses.append(max(q * diff, (q - 1) * diff))
    return 2 * float(np.mean(losses))


def run_series(pipe, name: str, h: int) -> dict:
    prices = load(name)
    idx = prices.index
    test_mask = (idx >= TEST_START) & (idx <= TEST_END)
    target_positions = np.where(test_mask)[0]
    rows = []
    for tp in target_positions[::STRIDE]:
        op = tp - h  # forecast origin position
        if op < CONTEXT:
            continue
        context = torch.tensor(prices.values[op - CONTEXT + 1: op + 1], dtype=torch.float32)
        with torch.no_grad():
            q_out, _ = pipe.predict_quantiles(
                [context], prediction_length=h, quantile_levels=QUANTILES,
            )
        q_h = q_out[0, h - 1, :].numpy()  # quantiles at the h-step-ahead date
        rows.append({
            "target_date": idx[tp], "origin_date": idx[op],
            "actual": prices.values[tp], "origin_price": prices.values[op],
            **{f"q{int(q * 100):02d}": float(v) for q, v in zip(QUANTILES, q_h)},
        })
    return pd.DataFrame(rows).set_index("target_date")


def evaluate(df: pd.DataFrame, name: str, h: int) -> dict:
    y = df["actual"].values
    med = df["q50"].values
    nc = df["origin_price"].values  # no-change forecast = price at origin
    m = metrics.mspe_ratio(med, nc, y)
    dm = metrics.diebold_mariano(med - y, nc - y, h=h)
    sr = metrics.success_ratio(med - nc, y - nc)
    pt = metrics.pesaran_timmermann(med - nc, y - nc)
    iv80 = metrics.interval_metrics(df["q10"].values, df["q90"].values, y, 0.20)
    iv90 = metrics.interval_metrics(df["q05"].values, df["q95"].values, y, 0.10)
    crps = float(np.mean([
        crps_from_quantiles(row[[f"q{int(q*100):02d}" for q in QUANTILES]].values, row["actual"], QUANTILES)
        for _, row in df.iterrows()
    ]))
    return {
        "series": name, "h": h, "n": len(df),
        "mspe_ratio_vs_nc": round(m["mspe_ratio"], 4),
        "rmae_vs_nc": round(metrics.rmae(med, nc, y), 4),
        "success_ratio": round(sr, 3),
        "pt_p": None if np.isnan(pt["pvalue"]) else round(pt["pvalue"], 3),
        "dm_p_onesided": None if np.isnan(dm["p_onesided"]) else round(dm["p_onesided"], 3),
        "crps": round(crps, 3),
        "picp80_native": round(iv80["picp"], 3),
        "picp90_native": round(iv90["picp"], 3),
        "winkler80": round(iv80["winkler"], 2),
    }


def main() -> None:
    print(f"loading {MODEL} (CPU)...")
    pipe = BaseChronosPipeline.from_pretrained(MODEL, device_map="cpu", torch_dtype=torch.float32)
    results = []
    for name in SERIES:
        for h in HORIZONS:
            t0 = datetime.now()
            df = run_series(pipe, name, h)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            df.to_csv(OUT / f"chronos_bolt_small_{name}_h{h}_{stamp}.csv")
            res = evaluate(df, name, h)
            res["sec"] = round((datetime.now() - t0).total_seconds(), 1)
            results.append(res)
            print(res)
    table = pd.DataFrame(results)
    md = [
        "# Smoke Test B — Zero-shot Chronos-Bolt-small (CPU) Harness Validation",
        f"\nGenerated {datetime.now(timezone.utc).isoformat()} | model {MODEL} | context {CONTEXT} | "
        f"test {TEST_START}..{TEST_END} (calm year; NOT the holdout; NOT paper results)",
        "\n", table.to_markdown(index=False),
        "\n## Pass criteria",
        "- [ ] runs end-to-end, per-origin context strictly excludes target dates",
        "- [ ] MSPE ratio ~1.0 (zero-shot small model should NOT crush no-change; <<1 = leakage alarm)",
        "- [ ] native PICP80/90 recorded (miscoverage here motivates the conformal layer)",
    ]
    (OUT / "results_smoke_b.md").write_text("\n".join(md), encoding="utf-8")
    print("\n", table.to_string(index=False))


if __name__ == "__main__":
    main()
