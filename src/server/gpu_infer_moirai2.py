"""Moirai-2 (small) zero-shot GPU inference on the GPU server (moirai env, uni2ts 2.0).

GluonTS-based: each rolling-origin context becomes one ListDataset entry;
forecasts are read via Forecast.quantile(level). Same output schema and
immutable-cache rules as the other runners.

Run on server:
  ~/miniconda3/envs/moirai/bin/python ~/commodity/scripts/gpu_infer_moirai2.py
"""
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from gluonts.dataset.common import ListDataset
from uni2ts.model.moirai2 import Moirai2Forecast, Moirai2Module

HOME = Path.home()
DATA = HOME / "commodity" / "data"
PRED = HOME / "commodity" / "outputs" / "predictions"
WEIGHTS = HOME / "commodity" / "weights" / "Salesforce__moirai-2.0-R-small"
MODEL_KEY = "moirai2_small"
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
EVAL_START = "2015-01-01"
CONTEXT = 512
QUANTILES = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
BATCH = 512
torch.manual_seed(20260811)


def load(name: str) -> pd.Series:
    df = pd.read_csv(DATA / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def main() -> None:
    PRED.mkdir(parents=True, exist_ok=True)
    module = Moirai2Module.from_pretrained(str(WEIGHTS))
    for series in SERIES:
        prices = load(series)
        values = prices.values.astype(np.float32)
        idx = prices.index
        for h in HORIZONS:
            out = PRED / f"{MODEL_KEY}__{series}__h{h}.csv"
            if out.exists():
                print(f"skip cached {out.name}", flush=True)
                continue
            model = Moirai2Forecast(
                module=module, prediction_length=h, context_length=CONTEXT,
                target_dim=1, feat_dynamic_real_dim=0, past_feat_dynamic_real_dim=0,
            )
            predictor = model.create_predictor(batch_size=BATCH)
            positions = np.arange(len(idx))
            tps = positions[(idx >= EVAL_START) & (positions >= CONTEXT + h)]
            entries = [
                {
                    "target": values[tp - h - CONTEXT + 1: tp - h + 1],
                    "start": pd.Period(idx[tp - h - CONTEXT + 1], freq="D"),
                    "item_id": int(tp),
                }
                for tp in tps
            ]
            ds = ListDataset(entries, freq="D")
            t0 = time.time()
            rows = []
            for fc in predictor.predict(ds):
                tp = int(fc.item_id)
                qvals = {f"q{int(q*100):02d}": float(np.asarray(fc.quantile(q))[h - 1])
                         for q in QUANTILES}
                rows.append({
                    "target_date": idx[tp], "origin_date": idx[tp - h],
                    "actual": values[tp], "point": qvals["q50"], **qvals,
                })
            df = pd.DataFrame(rows).set_index("target_date")
            if out.exists():
                raise FileExistsError(out)
            df.to_csv(out)
            print(f"{MODEL_KEY} {series} h={h}: {len(df)} targets in {time.time()-t0:.0f}s", flush=True)
    print("moirai-2 inference complete", flush=True)


if __name__ == "__main__":
    main()
