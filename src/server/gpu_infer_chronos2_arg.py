"""Chronos-2 zero-shot GPU inference on the GPU server (tsfm env, concurrent-use approved).

Mirrors the local phase-1 runner: same origins, context, quantiles, output
schema, immutable cache. Chronos-2 supports arbitrary quantile levels, so
q05/q95 are REAL here (unlike Bolt).

Run on server (argv: model_key weights_dirname):
  ~/miniconda3/envs/tsfm/bin/python ~/commodity/scripts/gpu_infer_chronos2_arg.py \
      chronos_2_lora chronos2_ft_lora
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from chronos import BaseChronosPipeline

HOME = Path.home()
DATA = HOME / "commodity" / "data"
PRED = HOME / "commodity" / "outputs" / "predictions"
MODEL_KEY = sys.argv[1]
WEIGHTS = HOME / "commodity" / "weights" / sys.argv[2]
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
EVAL_START = "2015-01-01"
CONTEXT = 512
QUANTILES = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
BATCH = 256
torch.manual_seed(20260811)


def load(name: str) -> pd.Series:
    df = pd.read_csv(DATA / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def main() -> None:
    PRED.mkdir(parents=True, exist_ok=True)
    pipe = BaseChronosPipeline.from_pretrained(
        str(WEIGHTS), device_map="cuda", torch_dtype=torch.bfloat16,
    )
    for series in SERIES:
        prices = load(series)
        values = prices.values.astype(np.float32)
        idx = prices.index
        for h in HORIZONS:
            out = PRED / f"{MODEL_KEY}__{series}__h{h}.csv"
            if out.exists():
                print(f"skip cached {out.name}", flush=True)
                continue
            positions = np.arange(len(idx))
            tps = positions[(idx >= EVAL_START) & (positions >= CONTEXT + h)]
            rows = []
            t0 = time.time()
            for start in range(0, len(tps), BATCH):
                chunk = tps[start: start + BATCH]
                contexts = [torch.tensor(values[tp - h - CONTEXT + 1: tp - h + 1]) for tp in chunk]
                with torch.no_grad():
                    q_out, _ = pipe.predict_quantiles(
                        contexts, prediction_length=h, quantile_levels=QUANTILES,
                    )
                # Chronos-2 returns a list of per-item tensors; Bolt returns (B, h, Q)
                if isinstance(q_out, list):
                    q_h = np.stack([
                        np.asarray(q.float().cpu()).reshape(h, len(QUANTILES))[h - 1]
                        for q in q_out
                    ])
                else:
                    q_h = q_out[:, h - 1, :].float().cpu().numpy()
                for i, tp in enumerate(chunk):
                    rows.append({
                        "target_date": idx[tp], "origin_date": idx[tp - h],
                        "actual": values[tp],
                        "point": float(q_h[i, QUANTILES.index(0.50)]),
                        **{f"q{int(q*100):02d}": float(q_h[i, k]) for k, q in enumerate(QUANTILES)},
                    })
            df = pd.DataFrame(rows).set_index("target_date")
            if out.exists():
                raise FileExistsError(out)
            df.to_csv(out)
            print(f"{MODEL_KEY} {series} h={h}: {len(df)} targets in {time.time()-t0:.0f}s", flush=True)
    print("chronos-2 inference complete", flush=True)


if __name__ == "__main__":
    main()
