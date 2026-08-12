"""Figure 1 — the calibration layer as a deployable, model-agnostic module.

Minimal diagram: few boxes, few words per box, straight arrows, no arrow crossing
a box or a label. Detail lives in the caption, not the figure.

Run:  python make_fig1_architecture.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "outputs" / "figures"

INK = "#1a1a1a"
MUTED = "#6b6b6b"
ACCENT = "#0072B2"      # Okabe-Ito blue: the contributed module
NEUTRAL = "#f2f2f2"

mpl.rcParams.update({"figure.dpi": 150, "savefig.dpi": 300,
                     "font.size": 9, "font.family": "sans-serif"})


def box(ax, x, y, w, h, label, sub=None, accent=False):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
        linewidth=1.4, edgecolor=ACCENT if accent else MUTED,
        facecolor="white" if accent else NEUTRAL, zorder=2))
    ax.text(x + w / 2, y + h / 2 + (0.035 if sub else 0), label,
            ha="center", va="center", fontsize=9.5, zorder=3,
            color=ACCENT if accent else INK,
            fontweight="bold" if accent else "normal")
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.05, sub, ha="center", va="center",
                fontsize=7.8, color=MUTED, zorder=3)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrow(x1, y1, x2 - x1, y2 - y1, width=0.004,
                            head_width=0.024, head_length=0.020,
                            length_includes_head=True, color=MUTED, zorder=1))


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 2.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    y, h = 0.46, 0.30
    xs = [0.005, 0.27, 0.535, 0.815]
    ws = [0.20, 0.20, 0.225, 0.18]
    box(ax, xs[0], y, ws[0], h, "Price history", "univariate, daily")
    box(ax, xs[1], y, ws[1], h, "Any forecaster", "TSFM or classical")
    box(ax, xs[2], y, ws[2], h, "Calibration layer", "online, no retraining", accent=True)
    box(ax, xs[3], y, ws[3], h, "Calibrated\ninterval", "coverage held")

    for i in range(3):
        arrow(ax, xs[i] + ws[i] + 0.012, y + h / 2, xs[i + 1] - 0.012, y + h / 2)

    # feedback: realised outcome returns to the calibration layer only after the horizon
    x_mid = xs[2] + ws[2] / 2
    x_out = xs[3] + ws[3] / 2
    y_fb = y - 0.16
    ax.plot([x_out, x_out, x_mid], [y, y_fb, y_fb], color=MUTED, lw=1.2, zorder=1)
    arrow(ax, x_mid, y_fb, x_mid, y - 0.008)
    ax.text(x_mid + (x_out - x_mid) / 2, y_fb - 0.10,
            "realised outcome, delayed by the horizon",
            ha="center", va="center", fontsize=7.8, color=MUTED)

    ax.text(x_mid, y + h + 0.06, "contributed module", ha="center", fontsize=8,
            color=ACCENT, style="italic")

    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"fig1_architecture.{ext}", bbox_inches="tight")
    plt.close(fig)
    print("saved fig1_architecture.pdf/.png")


if __name__ == "__main__":
    main()
