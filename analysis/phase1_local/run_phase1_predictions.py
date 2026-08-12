"""Phase 1 (local CPU): generate the full out-of-sample prediction cache.

Scope: 10 futures series x h in {1,5,22} x models {no-change, AR(5)-returns,
chronos-bolt-small, chronos-bolt-base}. Origins: every business day whose
target lands in 2015-01-01 .. data end.

IMPORTANT: predictions ARE generated for the sacred Hormuz window (models are
frozen/zero-shot; no tuning is possible), but the EVALUATION script must not
touch that window until the final, single, pre-registered pass.

Outputs: outputs/predictions/{model}__{series}__h{h}.csv (immutable — script
refuses to overwrite existing files).
Run:  python run_phase1_predictions.py
"""
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from eval_core import baselines  # noqa: E402
from chronos import BaseChronosPipeline  # noqa: E402

PRICES = ROOT / "data" / "raw" / "prices"
PRED_DIR = ROOT / "outputs" / "predictions"
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
EVAL_START = "2015-01-01"
CONTEXT = 512
QUANTILES = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
BATCH = 128
CHRONOS_MODELS = {
    "chronos_bolt_small": "amazon/chronos-bolt-small",
    "chronos_bolt_base": "amazon/chronos-bolt-base",
}
torch.manual_seed(20260811)
np.random.seed(20260811)


def load(name: str) -> pd.Series:
    df = pd.read_csv(PRICES / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def out_path(model: str, series: str, h: int) -> Path:
    return PRED_DIR / f"{model}__{series}__h{h}.csv"


def save_immutable(df: pd.DataFrame, model: str, series: str, h: int) -> None:
    path = out_path(model, series, h)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite immutable cache: {path}")
    df.to_csv(path)


def gen_targets(prices: pd.Series, h: int) -> np.ndarray:
    idx = prices.index
    positions = np.arange(len(idx))
    mask = (idx >= EVAL_START)
    return positions[mask & (positions >= CONTEXT + h)]


def run_baselines(series: str, prices: pd.Series) -> None:
    for h in HORIZONS:
        tps = gen_targets(prices, h)
        origins = prices.index[tps - h]
        if not out_path("no_change", series, h).exists():
            nc = prices.values[tps - h]
            df = pd.DataFrame({
                "target_date": prices.index[tps], "origin_date": origins,
                "actual": prices.values[tps], "point": nc,
            }).set_index("target_date")
            save_immutable(df, "no_change", series, h)
        if not out_path("ar5_returns", series, h).exists():
            ar = baselines.recursive_ar_returns_forecast(prices, h, origins, p=5)
            df = pd.DataFrame({
                "target_date": ar.index,
                "origin_date": prices.index[prices.index.get_indexer(ar.index) - h],
                "actual": prices.reindex(ar.index).values, "point": ar.values,
            }).set_index("target_date")
            save_immutable(df, "ar5_returns", series, h)
        print(f"  baselines {series} h={h} done ({len(tps)} targets)")


def run_chronos(model_key: str, hf_name: str, series: str, prices: pd.Series, pipe) -> None:
    values = prices.values.astype(np.float32)
    for h in HORIZONS:
        if out_path(model_key, series, h).exists():
            print(f"  {model_key} {series} h={h} cached — skip")
            continue
        tps = gen_targets(prices, h)
        rows = []
        t0 = time.time()
        for start in range(0, len(tps), BATCH):
            chunk = tps[start: start + BATCH]
            contexts = [torch.tensor(values[tp - h - CONTEXT + 1: tp - h + 1]) for tp in chunk]
            with torch.no_grad():
                q_out, _ = pipe.predict_quantiles(
                    contexts, prediction_length=h, quantile_levels=QUANTILES,
                )
            q_h = q_out[:, h - 1, :].numpy()
            for i, tp in enumerate(chunk):
                rows.append({
                    "target_date": prices.index[tp],
                    "origin_date": prices.index[tp - h],
                    "actual": values[tp],
                    "point": float(q_h[i, QUANTILES.index(0.50)]),
                    **{f"q{int(q*100):02d}": float(q_h[i, k]) for k, q in enumerate(QUANTILES)},
                })
        df = pd.DataFrame(rows).set_index("target_date")
        save_immutable(df, model_key, series, h)
        print(f"  {model_key} {series} h={h} done ({len(df)} targets, {time.time()-t0:.0f}s)")


def main() -> None:
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "eval_start": EVAL_START, "context": CONTEXT, "quantiles": QUANTILES,
        "note": "Hormuz window predictions present but embargoed for evaluation until final pass",
    }
    for series in SERIES:
        prices = load(series)
        print(f"[{series}] {len(prices)} obs {prices.index.min().date()}..{prices.index.max().date()}")
        run_baselines(series, prices)
    for model_key, hf_name in CHRONOS_MODELS.items():
        print(f"loading {hf_name} (CPU)...")
        pipe = BaseChronosPipeline.from_pretrained(hf_name, device_map="cpu", torch_dtype=torch.float32)
        for series in SERIES:
            run_chronos(model_key, hf_name, series, load(series), pipe)
        del pipe
    (PRED_DIR / "manifest.json").write_text(pd.Series(manifest).to_json(indent=2), encoding="utf-8")
    print("phase 1 prediction cache complete")


if __name__ == "__main__":
    main()
