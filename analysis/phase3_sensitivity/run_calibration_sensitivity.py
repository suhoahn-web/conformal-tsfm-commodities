"""E3/E4: is the crisis-calibration result an artefact of our two fixed choices?

The manuscript compares one rolling-window conformal baseline (250 observations,
fixed nominal level) against one ACI configuration (gamma = 0.02) and concludes
that the rolling baseline undercovers badly in crises. A referee will immediately
ask whether a *shorter* rolling window would adapt fast enough on its own — which
would reduce the finding to "our window was too slow" rather than a statement
about non-adaptive calibration.

This script answers that by sweeping both knobs on the cached predictions:

  E3  rolling-window length  {50, 100, 250, 500}   at the pre-registered alpha
  E4  ACI step size gamma    {0.005, 0.01, 0.02, 0.05} at window 250

Nothing is re-forecast; the wrappers are re-applied to the immutable cache, so
this is CPU-only and changes no existing result. The embargo is enforced exactly
as in phase 1 — the Hormuz window never enters.

This is a post-hoc robustness analysis, run after the pre-registered result. It
is reported as such and does not replace the pre-registered configuration.

Run:  python analysis/phase3_sensitivity/run_calibration_sensitivity.py
"""
import io
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from eval_core import conformal, metrics  # noqa: E402

PRED_DIR = ROOT / "outputs" / "predictions"
OUT = Path(__file__).resolve().parent
EMBARGO_END = pd.Timestamp("2026-02-27")
EVAL_START = pd.Timestamp("2015-01-01")
REGIMES = {"covid": ("2020-02-20", "2020-08-31"),
           "ukraine": ("2022-02-24", "2022-08-31")}
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
INTERVAL_MODELS = ["garch_t", "qr_ar", "chronos_bolt_small", "chronos_bolt_base",
                   "chronos_2", "chronos_2_lora", "chronos_2_full",
                   "timesfm_25", "moirai2_small"]

ALPHA = 0.20                       # the 80% band the manuscript headlines
WINDOWS = [50, 100, 250, 500]      # E3
GAMMAS = [0.005, 0.01, 0.02, 0.05]  # E4
PREREGISTERED = (250, 0.02)


def load_cache(model: str, series: str, h: int) -> pd.DataFrame | None:
    path = PRED_DIR / f"{model}__{series}__h{h}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=["target_date"]).set_index("target_date")
    df = df.loc[(df.index >= EVAL_START) & (df.index <= EMBARGO_END)]
    if df.empty:
        return None
    assert df.index.max() <= EMBARGO_END, "EMBARGO VIOLATION"
    return df


def regime_label(idx: pd.DatetimeIndex) -> pd.Series:
    lab = pd.Series("calm", index=idx)
    for name, (a, b) in REGIMES.items():
        lab.loc[(idx >= a) & (idx <= b)] = name
    return lab


def score(lo, hi, y, idx) -> list[dict]:
    j = pd.concat({"lo": lo, "hi": hi, "y": y}, axis=1).dropna()
    lab = regime_label(j.index)
    out = []
    for reg in ["ALL", "calm", "covid", "ukraine"]:
        sub = j if reg == "ALL" else j[lab == reg]
        if len(sub) < 30:
            continue
        im = metrics.interval_metrics(sub["lo"].values, sub["hi"].values,
                                      sub["y"].values, ALPHA)
        out.append({"regime": reg, "n": len(sub), "picp": round(im["picp"], 4),
                    "width": round(im["mean_width"], 4),
                    "winkler": round(im["winkler"], 4)})
    return out


def main() -> int:
    rows, done, skipped = [], 0, 0
    for model in INTERVAL_MODELS:
        for series in SERIES:
            for h in HORIZONS:
                df = load_cache(model, series, h)
                if df is None:
                    skipped += 1
                    continue
                fc, ac = df["point"], df["actual"]
                configs = [("Rolling-SC", w, np.nan) for w in WINDOWS]
                configs += [("ACI", 250, g) for g in GAMMAS]
                for method, win, gam in configs:
                    if method == "Rolling-SC":
                        iv = conformal.split_conformal(fc, ac, alpha=ALPHA,
                                                       cal_size=win, horizon=h)
                    else:
                        iv = conformal.aci(fc, ac, alpha=ALPHA, cal_size=win,
                                           gamma=gam, horizon=h)
                    for r in score(iv["lo"], iv["hi"], ac, df.index):
                        rows.append({"model": model, "series": series, "h": h,
                                     "method": method, "window": win,
                                     "gamma": gam, **r})
                done += 1
                print(f"  {done:3d} cells | {model}/{series}/h{h}", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "calibration_sensitivity.csv", index=False)

    # Headline question: pooled median coverage by config, regime and horizon.
    piv = (df.groupby(["method", "window", "gamma", "h", "regime"], dropna=False)
             ["picp"].median().reset_index())
    piv.to_csv(OUT / "calibration_sensitivity_medians.csv", index=False)

    lines = [
        "# E3/E4 — rolling-window and ACI step-size sensitivity",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat()} | nominal 0.80 | "
        f"eval {EVAL_START.date()}..{EMBARGO_END.date()} (Hormuz window excluded)",
        "",
        f"Cells evaluated: {done} (model x series x horizon); missing: {skipped}.",
        "Post-hoc robustness analysis. The pre-registered configuration is "
        f"window {PREREGISTERED[0]}, gamma {PREREGISTERED[1]}.",
        "",
        "## Median PICP across models and series (nominal 0.80)",
        "",
    ]
    for h in HORIZONS:
        lines += [f"### h = {h}", "",
                  "| method | window | gamma | calm | covid | ukraine |",
                  "|---|---|---|---|---|---|"]
        sub = piv[piv["h"] == h]
        for (m, w, g), grp in sub.groupby(["method", "window", "gamma"], dropna=False):
            got = {r.regime: r.picp for r in grp.itertuples()}
            star = " **(pre-registered)**" if (w, g) == PREREGISTERED or \
                   (m == "Rolling-SC" and w == 250) else ""
            gs = "—" if pd.isna(g) else f"{g}"
            lines.append(f"| {m}{star} | {w} | {gs} | "
                         f"{got.get('calm', float('nan')):.3f} | "
                         f"{got.get('covid', float('nan')):.3f} | "
                         f"{got.get('ukraine', float('nan')):.3f} |")
        lines.append("")

    # The decisive comparison, stated explicitly so it cannot be read selectively.
    lines += ["## Decisive comparison", ""]
    for h in HORIZONS:
        sub = piv[(piv["h"] == h) & (piv["regime"].isin(["covid", "ukraine"]))]
        sc = sub[sub["method"] == "Rolling-SC"]
        aci_pre = sub[(sub["method"] == "ACI") & (sub["gamma"] == 0.02)]
        best_sc = sc.loc[sc["picp"].idxmax()] if len(sc) else None
        if best_sc is None or not len(aci_pre):
            continue
        lines.append(
            f"- **h = {h}**: best rolling window is {int(best_sc.window)} at "
            f"PICP {best_sc.picp:.3f} ({best_sc.regime}); pre-registered ACI "
            f"(gamma 0.02) reaches {aci_pre['picp'].max():.3f} at its best crisis "
            f"regime and {aci_pre['picp'].min():.3f} at its worst.")
    (OUT / "results_sensitivity.md").write_text("\n".join(lines) + "\n",
                                                encoding="utf-8")
    print(f"\nwritten: {OUT / 'results_sensitivity.md'} ({len(df)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
