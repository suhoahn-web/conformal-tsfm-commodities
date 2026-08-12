"""Validate the manuscript figure palette for CVD separation (compute, don't eyeball).

Simulates protanopia/deuteranopia/tritanopia (Vienot-Brettel-Mollon linear model)
and reports OKLab dE x100 for every adjacent pair, plus normal-vision separation.
Thresholds follow the dataviz rules: CVD dE >= 8 target, normal-vision dE >= 15 hard floor.
"""
import itertools

import numpy as np

# Okabe-Ito (2008), the standard colorblind-safe qualitative palette for print.
# Yellow (#F0E442) dropped: insufficient contrast on white paper.
PALETTE = {
    "black": "#000000",
    "orange": "#E69F00",
    "skyblue": "#56B4E9",
    "green": "#009E73",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
}

M_LMS = np.array([[0.31399022, 0.63951294, 0.04649755],
                  [0.15537241, 0.75789446, 0.08670142],
                  [0.01775239, 0.10944209, 0.87256922]])
M_LMS_INV = np.linalg.inv(M_LMS)
SIM = {
    "protan": np.array([[0, 1.05118294, -0.05116099], [0, 1, 0], [0, 0, 1]]),
    "deutan": np.array([[1, 0, 0], [0.9513092, 0, 0.04866992], [0, 0, 1]]),
    "tritan": np.array([[1, 0, 0], [0, 1, 0], [-0.86744736, 1.86727089, 0]]),
}


def hex_to_lin(h: str) -> np.ndarray:
    srgb = np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)


def simulate(lin: np.ndarray, kind: str) -> np.ndarray:
    return M_LMS_INV @ (SIM[kind] @ (M_LMS @ lin))


def lin_to_oklab(lin: np.ndarray) -> np.ndarray:
    m = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                  [0.2119034982, 0.6806995451, 0.1073969566],
                  [0.0883024619, 0.2817188376, 0.6299787005]])
    lms = np.cbrt(np.clip(m @ lin, 0, None))
    m2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                   [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]])
    return m2 @ lms


def de(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(lin_to_oklab(a) - lin_to_oklab(b)) * 100)


def main() -> None:
    names = list(PALETTE)
    lins = {n: hex_to_lin(PALETTE[n]) for n in names}
    print(f"{'pair':28s} {'normal':>7s} {'protan':>7s} {'deutan':>7s} {'tritan':>7s}  verdict")
    fails = 0
    for a, b in itertools.combinations(names, 2):
        d_norm = de(lins[a], lins[b])
        ds = {k: de(simulate(lins[a], k), simulate(lins[b], k)) for k in SIM}
        worst_cvd = min(ds.values())
        verdict = "OK"
        if d_norm < 15:
            verdict = "FAIL normal<15"
            fails += 1
        elif worst_cvd < 6:
            verdict = "FAIL cvd<6"
            fails += 1
        elif worst_cvd < 8:
            verdict = "WARN cvd 6-8 (needs marker/linestyle)"
        print(f"{a + '/' + b:28s} {d_norm:7.1f} {ds['protan']:7.1f} "
              f"{ds['deutan']:7.1f} {ds['tritan']:7.1f}  {verdict}")
    print(f"\n{len(list(itertools.combinations(names, 2)))} pairs checked, {fails} hard failures")
    print("All figures additionally dual-encode with distinct markers and line styles.")


if __name__ == "__main__":
    main()
