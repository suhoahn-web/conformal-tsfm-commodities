"""Fine-tune Chronos-2 on the pre-2015 commodity panel (the GPU server, tsfm env).

Pre-registration compliance (RESEARCH_PLAN_v1 §3.3):
  - Training inputs: the 10 futures series STRICTLY before 2015-01-01.
  - Validation (model selection): the 2013-2014 tail of the training window —
    still pre-2015, so no OOS contamination.
  - Hyperparameters: library defaults (lr=1e-6, num_steps=1000, batch=256);
    LoRA uses chronos' default LoraConfig. Nothing tuned on post-2015 data.
  - Two variants: finetune_mode="lora" and "full" (full FT replaces the TTM
    full-FT slot; deviation logged in the plan).

Run on server:
  ~/miniconda3/envs/tsfm/bin/python ~/commodity/scripts/finetune_chronos2.py lora
  ~/miniconda3/envs/tsfm/bin/python ~/commodity/scripts/finetune_chronos2.py full
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
WEIGHTS = HOME / "commodity" / "weights" / "amazon__chronos-2"
OUT_BASE = HOME / "commodity" / "weights"
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
TRAIN_END = "2012-12-31"   # training series end
VAL_START, VAL_END = "2013-01-01", "2014-12-31"  # pre-2015 validation tail
PREDICTION_LENGTH = 22
torch.manual_seed(20260811)
np.random.seed(20260811)


def load(name: str) -> pd.Series:
    df = pd.read_csv(DATA / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "lora"
    assert mode in ("lora", "full")
    out_dir = OUT_BASE / f"chronos2_ft_{mode}"
    if (out_dir / "config.json").exists() or (out_dir / "model.safetensors").exists():
        print(f"already fine-tuned: {out_dir} — refusing to overwrite", flush=True)
        return

    train_inputs, val_inputs = [], []
    for s in SERIES:
        p = load(s)
        tr = p.loc[:TRAIN_END].values.astype(np.float32)
        va = p.loc[:VAL_END].values.astype(np.float32)  # context incl. train, targets in 2013-14
        assert p.loc[:TRAIN_END].index.max() < pd.Timestamp("2013-01-01")
        assert p.loc[:VAL_END].index.max() < pd.Timestamp("2015-01-01")
        train_inputs.append(torch.tensor(tr))
        val_inputs.append(torch.tensor(va))
        print(f"{s}: train n={len(tr)}, val-context n={len(va)}", flush=True)

    pipe = BaseChronosPipeline.from_pretrained(
        str(WEIGHTS), device_map="cuda", torch_dtype=torch.float32,
    )
    t0 = time.time()
    ft_pipe = pipe.fit(
        inputs=train_inputs,
        prediction_length=PREDICTION_LENGTH,
        validation_inputs=val_inputs,
        finetune_mode=mode,
        output_dir=str(out_dir / "trainer_out"),
    )
    ft_pipe.save_pretrained(str(out_dir))
    print(f"fine-tune [{mode}] done in {time.time()-t0:.0f}s -> {out_dir}", flush=True)


if __name__ == "__main__":
    main()
