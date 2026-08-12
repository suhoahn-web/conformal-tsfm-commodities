"""TimesFM 2.5 zero-shot GPU inference on the GPU server (tsfm env).

API (probed 2026-08-11): from_pretrained -> compile(ForecastConfig) ->
forecast(horizon, inputs) -> (point (B,H), quantiles (B,H,10)).
Quantile tensor convention: col 0 = mean, cols 1..9 = deciles q10..q90
(asserted + spot-checked for monotonicity at runtime). Native 95% bands are
NOT available — recorded as a model capability finding.

Run on server:
  ~/miniconda3/envs/tsfm/bin/python ~/commodity/scripts/gpu_infer_timesfm25.py
"""
import time
from pathlib import Path

import numpy as np
import pandas as pd
import timesfm

HOME = Path.home()
DATA = HOME / "commodity" / "data"
PRED = HOME / "commodity" / "outputs" / "predictions"
WEIGHTS = HOME / "commodity" / "weights" / "google__timesfm-2.5-200m-pytorch"
MODEL_KEY = "timesfm_25"
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
EVAL_START = "2015-01-01"
CONTEXT = 512
BATCH = 256
DECILES = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]


def load(name: str) -> pd.Series:
    df = pd.read_csv(DATA / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def main() -> None:
    PRED.mkdir(parents=True, exist_ok=True)
    model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(str(WEIGHTS))
    model.compile(timesfm.ForecastConfig(
        max_context=CONTEXT, max_horizon=32, normalize_inputs=True,
        per_core_batch_size=32, use_continuous_quantile_head=True,
        fix_quantile_crossing=True,
    ))
    checked = False
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
                inputs = [values[tp - h - CONTEXT + 1: tp - h + 1] for tp in chunk]
                point, quantiles = model.forecast(horizon=h, inputs=inputs)
                q = np.asarray(quantiles)
                assert q.shape[-1] == 10, f"unexpected quantile dim: {q.shape}"
                if not checked:
                    row0 = q[0, h - 1, 1:]
                    assert np.all(np.diff(row0) >= -1e-6), f"deciles not monotone: {row0}"
                    print(f"quantile convention check OK: {row0}", flush=True)
                    checked = True
                for i, tp in enumerate(chunk):
                    rows.append({
                        "target_date": idx[tp], "origin_date": idx[tp - h],
                        "actual": values[tp],
                        "point": float(np.asarray(point)[i, h - 1]),
                        **{f"q{int(dq*100):02d}": float(q[i, h - 1, k + 1])
                           for k, dq in enumerate(DECILES)},
                    })
            df = pd.DataFrame(rows).set_index("target_date")
            if out.exists():
                raise FileExistsError(out)
            df.to_csv(out)
            print(f"{MODEL_KEY} {series} h={h}: {len(df)} targets in {time.time()-t0:.0f}s", flush=True)
    print("timesfm-2.5 inference complete", flush=True)


if __name__ == "__main__":
    main()
