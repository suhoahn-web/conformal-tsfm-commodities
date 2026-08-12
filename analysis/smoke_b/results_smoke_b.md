# Smoke Test B — Zero-shot Chronos-Bolt-small (CPU) Harness Validation

Generated 2026-08-10T16:51:45.784314+00:00 | model amazon/chronos-bolt-small | context 512 | test 2023-01-01..2023-12-31 (calm year; NOT the holdout; NOT paper results)


| series     |   h |   n |   mspe_ratio_vs_nc |   rmae_vs_nc |   success_ratio |   pt_p |   dm_p_onesided |   crps |   picp80_native |   picp90_native |   winkler80 |   sec |
|:-----------|----:|----:|-------------------:|-------------:|----------------:|-------:|----------------:|-------:|----------------:|----------------:|------------:|------:|
| wti_fut    |   1 | 250 |             1.198  |       1.0882 |           0.512 |  0.204 |           0.999 |  0.813 |           0.828 |           0.828 |        6.21 |   5.8 |
| wti_fut    |   5 | 250 |             1.0679 |       1.0263 |           0.54  |  0.112 |           0.798 |  1.729 |           0.756 |           0.756 |       12.95 |   5.6 |
| gold_fut   |   1 | 250 |             1.1113 |       1.0702 |           0.508 |  0.446 |           0.994 |  7.9   |           0.816 |           0.816 |       63.82 |   5.7 |
| gold_fut   |   5 | 250 |             1.0408 |       1.0367 |           0.492 |  0.856 |           0.702 | 16.94  |           0.784 |           0.784 |      128.81 |   5.9 |
| copper_fut |   1 | 251 |             1.09   |       1.0331 |           0.506 |  0.328 |           0.99  |  0.024 |           0.797 |           0.797 |        0.19 |   5.8 |
| copper_fut |   5 | 251 |             1.0142 |       1.0211 |           0.506 |  0.413 |           0.612 |  0.047 |           0.857 |           0.857 |        0.36 |   5.6 |

## Pass criteria
- [ ] runs end-to-end, per-origin context strictly excludes target dates
- [ ] MSPE ratio ~1.0 (zero-shot small model should NOT crush no-change; <<1 = leakage alarm)
- [ ] native PICP80/90 recorded (miscoverage here motivates the conformal layer)
## Analyst notes (2026-08-11)

- All pass criteria met: end-to-end run, no leakage signal (all MSPE ratios >= 1), ~5.7s per series-horizon on CPU (250 origins).
- Zero-shot Chronos-Bolt-small LOSES to no-change on all 6 series-horizon combos (MSPE ratio 1.01-1.20) in the calm 2023 window — consistent with the TSFM-on-financial-series literature; the interesting question (crisis regimes, larger models, fine-tuning) remains open for the full experiment.
- **FINDING: picp90_native == picp80_native identically — Chronos-Bolt clamps requested quantiles to its trained range [0.1, 0.9]** (verified: q05==q10 and q95==q90 in every cached forecast). Native 95% intervals are IMPOSSIBLE for the Bolt family. This is a strong, concrete motivation for the conformal layer (and for including Chronos-2, which supports arbitrary quantile levels) — goes into the paper's motivation section.
- Native PICP80 ranges 0.756-0.857 vs nominal 0.80 even in a calm year — miscoverage exists before any crisis; regime windows should widen this gap (hypothesis for full run).
