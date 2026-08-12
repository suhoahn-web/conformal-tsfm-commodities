"""Generate manuscript figures from the evaluation CSVs.

Design rules (validated by src/visualization/palette_check.py):
  - Okabe-Ito colorblind-safe palette, ALWAYS dual-encoded with markers/linestyles
  - single y-axis per panel, recessive grid, thin marks, no chartjunk
  - reference lines carry the meaning (MSPE ratio = 1, nominal coverage)
  - vector PDF for submission + PNG for inspection

Figures:
  fig2_point_accuracy   — MSPE ratio vs no-change by model x horizon (all regimes)
  fig3_calibration      — PICP by conformal band x regime (the core result)
  fig4_finetune_tradeoff— accuracy gain vs calibration loss for FT variants
  fig5_mcs_survival     — Model Confidence Set survival frequency

Run:  python make_figures.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
P1 = ROOT / "analysis" / "phase1_local"
P2 = ROOT / "analysis" / "phase2_local"
FIG = ROOT / "outputs" / "figures"

OKABE = {
    "black": "#000000", "orange": "#E69F00", "skyblue": "#56B4E9",
    "green": "#009E73", "blue": "#0072B2", "vermillion": "#D55E00",
    "purple": "#CC79A7",
}
MARKERS = ["o", "s", "^", "D", "v", "P", "X"]
LINESTYLES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)), (0, (5, 1)), (0, (1, 1))]

MODEL_LABELS = {
    "no_change": "No-change", "ar5_returns": "AR(5)", "lear_lite": "LEAR-lite",
    "garch_t": "GARCH-t", "qr_ar": "QR-AR",
    "chronos_bolt_small": "Chronos-Bolt (S)", "chronos_bolt_base": "Chronos-Bolt (B)",
    "chronos_2": "Chronos-2", "chronos_2_lora": "Chronos-2 +LoRA",
    "chronos_2_full": "Chronos-2 +full FT", "timesfm_25": "TimesFM 2.5",
    "moirai2_small": "Moirai-2 (S)",
}
REGIME_LABELS = {"calm": "Calm", "covid": "COVID-19", "ukraine": "Ukraine war",
                 "ALL": "All periods"}

mpl.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 300, "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
    "axes.axisbelow": True, "legend.frameon": False, "lines.linewidth": 1.6,
    "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "figure.constrained_layout.use": True,
})


def save(fig, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)
    print(f"saved {name}.pdf/.png")


def fig2_point_accuracy(points: pd.DataFrame) -> None:
    d = points[points.regime == "ALL"]
    order = (d.groupby("model")["mspe_ratio"].median().sort_values().index.tolist())
    horizons = sorted(d.h.unique())
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    colors = [OKABE["blue"], OKABE["orange"], OKABE["green"]]
    for i, h in enumerate(horizons):
        sub = d[d.h == h].groupby("model")["mspe_ratio"].median().reindex(order)
        ax.plot(range(len(order)), sub.values, marker=MARKERS[i], color=colors[i],
                linestyle="none", markersize=6, markeredgecolor="white",
                markeredgewidth=0.6, label=f"h = {h}")
    ax.axhline(1.0, color=OKABE["black"], linewidth=1.0, linestyle="--", zorder=1)
    ax.annotate("no-change benchmark (ratio = 1)", xy=(0.99, 1.0),
                xycoords=("axes fraction", "data"), xytext=(0, 4),
                textcoords="offset points", ha="right", va="bottom",
                fontsize=7.5, color="0.35")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([MODEL_LABELS.get(m, m) for m in order], rotation=40,
                       ha="right")
    ax.set_ylabel("MSPE ratio vs no-change\n(median over 10 commodities)")
    ax.set_xlabel("")
    ax.legend(loc="upper left", ncols=3, fontsize=8)
    ax.set_ylim(0.95, max(1.25, d.mspe_ratio.median() * 1.2))
    save(fig, "fig2_point_accuracy")


def fig3_calibration(ivs: pd.DataFrame) -> None:
    d = ivs[(ivs.nominal == 0.80) & (ivs.regime != "ALL")]
    bands = [b for b in ["native80", "splitCP80", "SPCI80", "CQR80", "ACI80"]
             if b in set(d.band)]
    band_labels = {"native80": "Model native", "splitCP80": "Split conformal",
                   "SPCI80": "SPCI (adaptive width)", "CQR80": "CQR",
                   "ACI80": "ACI (adaptive $\\alpha$)"}
    regimes = ["calm", "covid", "ukraine"]
    colors = [OKABE["vermillion"], OKABE["orange"], OKABE["purple"],
              OKABE["skyblue"], OKABE["blue"]]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.4), sharey=True)
    handles = []
    for ax, h in zip(axes, [1, 5, 22]):
        for i, band in enumerate(bands):
            vals = [d[(d.band == band) & (d.regime == r) & (d.h == h)]["picp"].median()
                    for r in regimes]
            ln, = ax.plot(range(len(regimes)), vals, marker=MARKERS[i], color=colors[i],
                          linestyle=LINESTYLES[i], markersize=5.5, markeredgecolor="white",
                          markeredgewidth=0.5, label=band_labels.get(band, band))
            if ax is axes[0]:
                handles.append(ln)
        ax.axhline(0.80, color=OKABE["black"], linewidth=1.0, linestyle="--", zorder=1)
        ax.set_xticks(range(len(regimes)))
        ax.set_xticklabels([REGIME_LABELS[r] for r in regimes], rotation=25, ha="right")
        ax.set_title(f"h = {h}", fontsize=9)
        ax.margins(x=0.12)
    axes[0].set_ylabel("Empirical coverage (PICP)\nnominal 80%")
    # legend below the panels: never overlaps data, scales to 5 bands
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.02),
               ncols=min(len(handles), 3), fontsize=7.5)
    save(fig, "fig3_calibration")


def fig4_finetune_tradeoff(points: pd.DataFrame, ivs: pd.DataFrame) -> None:
    variants = ["chronos_2", "chronos_2_lora", "chronos_2_full"]
    colors = [OKABE["blue"], OKABE["green"], OKABE["vermillion"]]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
    horizons = [1, 5, 22]
    for i, v in enumerate(variants):
        acc = [points[(points.model == v) & (points.regime == "ALL") & (points.h == h)]
               ["mspe_ratio"].median() for h in horizons]
        ax1.plot(range(len(horizons)), acc, marker=MARKERS[i], color=colors[i],
                 linestyle=LINESTYLES[i], markersize=6, markeredgecolor="white",
                 markeredgewidth=0.6, label=MODEL_LABELS[v])
        cov = [ivs[(ivs.model == v) & (ivs.band == "native80") & (ivs.regime == r)
                   & (ivs.h == 5)]["picp"].median() for r in ["calm", "covid", "ukraine"]]
        ax2.plot(range(3), cov, marker=MARKERS[i], color=colors[i],
                 linestyle=LINESTYLES[i], markersize=6, markeredgecolor="white",
                 markeredgewidth=0.6, label=MODEL_LABELS[v])
    ax1.axhline(1.0, color=OKABE["black"], linewidth=1.0, linestyle="--")
    ax1.set_xticks(range(len(horizons)))
    ax1.set_xticklabels([f"h = {h}" for h in horizons])
    ax1.set_ylabel("MSPE ratio vs no-change")
    ax1.set_title("(a) Point accuracy improves", fontsize=9, loc="left")
    ax2.axhline(0.80, color=OKABE["black"], linewidth=1.0, linestyle="--")
    ax2.set_xticks(range(3))
    ax2.set_xticklabels([REGIME_LABELS[r] for r in ["calm", "covid", "ukraine"]],
                        rotation=25, ha="right")
    ax2.set_ylabel("Native interval coverage (h = 5)")
    ax2.set_title("(b) Calibration degrades", fontsize=9, loc="left")
    for ax in (ax1, ax2):
        ax.margins(x=0.10, y=0.18)  # keep extreme markers off the frame
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.04), ncols=3, fontsize=7.5)
    save(fig, "fig4_finetune_tradeoff")


def fig5_mcs(mcs_path: Path) -> None:
    mcs = pd.read_csv(mcs_path)
    freq = (mcs["survivors"].str.split(";").explode().value_counts() / len(mcs))
    freq = freq.sort_values()
    is_tsfm = [m in {"chronos_bolt_small", "chronos_bolt_base", "chronos_2",
                     "chronos_2_lora", "chronos_2_full", "timesfm_25",
                     "moirai2_small"} for m in freq.index]
    colors = [OKABE["vermillion"] if t else OKABE["blue"] for t in is_tsfm]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    bars = ax.barh([MODEL_LABELS.get(m, m) for m in freq.index], freq.values,
                   color=colors, height=0.65)
    for b, v in zip(bars, freq.values):
        ax.annotate(f"{v:.2f}", xy=(v, b.get_y() + b.get_height() / 2),
                    xytext=(3, 0), textcoords="offset points", va="center", fontsize=7.5)
    ax.set_xlabel("Share of 30 series x horizon combinations in the MCS (10% level)")
    ax.set_xlim(0, 1.08)
    handles = [plt.Line2D([], [], marker="s", linestyle="none", color=OKABE["blue"],
                          label="Statistical baselines"),
               plt.Line2D([], [], marker="s", linestyle="none", color=OKABE["vermillion"],
                          label="Foundation models")]
    ax.legend(handles=handles, fontsize=7.5, loc="lower right")
    save(fig, "fig5_mcs_survival")


def main() -> None:
    points = pd.read_csv(P1 / "points_phase1.csv")
    ivs = pd.read_csv(P1 / "intervals_phase1.csv")
    fig2_point_accuracy(points)
    fig3_calibration(ivs)
    fig4_finetune_tradeoff(points, ivs)
    mcs_path = P2 / "mcs_phase2.csv"
    if mcs_path.exists():
        fig5_mcs(mcs_path)
    print("figures complete ->", FIG)


if __name__ == "__main__":
    main()
