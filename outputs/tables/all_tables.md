# Manuscript tables (generated — do not edit by hand)


## Table 1. Commodity futures panel.

| Commodity   | Symbol   | First obs   | Last obs   |    N |
|:------------|:---------|:------------|:-----------|-----:|
| WTI crude   | CL=F     | 2000-08-23  | 2026-08-10 | 6518 |
| Natural gas | NG=F     | 2000-08-30  | 2026-08-10 | 6515 |
| Gold        | GC=F     | 2000-08-30  | 2026-08-10 | 6509 |
| Silver      | SI=F     | 2000-08-30  | 2026-08-10 | 6511 |
| Copper      | HG=F     | 2000-08-30  | 2026-08-10 | 6514 |
| Platinum    | PL=F     | 2000-01-04  | 2026-08-10 | 5993 |
| Corn        | ZC=F     | 2000-07-17  | 2026-08-10 | 6521 |
| Wheat       | ZW=F     | 2000-07-17  | 2026-08-10 | 6533 |
| Soybeans    | ZS=F     | 2000-09-15  | 2026-08-10 | 6513 |
| Brent crude | BZ=F     | 2007-07-30  | 2026-08-10 | 4736 |

## Table 3. Median MSPE ratio against the no-change benchmark, 2015-01-01 to 2026-02-27. Values below 1 indicate improvement over a random walk without drift. Medians are taken across the ten commodities.

| model               |   h = 1 |   h = 5 |   h = 22 |
|:--------------------|--------:|--------:|---------:|
| AR(5)               |  1.0008 |  0.9956 |   1.0016 |
| LEAR-lite           |  1.0061 |  1.0078 |   1.0221 |
| GARCH-t             |  1.0006 |  1.0024 |   1.0099 |
| QR-AR               |  1.0041 |  0.9936 |   1.0125 |
| TimesFM 2.5         |  1.0286 |  1.0204 |   1.0358 |
| Moirai-2 (S)        |  1.0658 |  1.0326 |   1.0658 |
| Chronos-2           |  1.1028 |  1.0637 |   1.0956 |
| Chronos-2 + LoRA    |  1.0901 |  1.0686 |   1.0707 |
| Chronos-2 + full FT |  1.1128 |  1.0276 |   1.0309 |
| Chronos-Bolt (S)    |  1.1746 |  1.0798 |   1.1048 |
| Chronos-Bolt (B)    |  1.1415 |  1.1046 |   1.1635 |

## Table 3. Per-series MSPE ratio against the no-change benchmark at h = 1. The dispersion behind the medians of Table 2.

| Commodity   |   AR(5) |   LEAR-lite |   GARCH-t |   QR-AR |   TimesFM 2.5 |   Moirai-2 (S) |   Chronos-2 |   Chronos-2 + LoRA |   Chronos-2 + full FT |   Chronos-Bolt (S) |   Chronos-Bolt (B) |
|:------------|--------:|------------:|----------:|--------:|--------------:|---------------:|------------:|-------------------:|----------------------:|-------------------:|-------------------:|
| Brent crude |   1.006 |       1.027 |     1.005 |   1.012 |         1.036 |          1.14  |       1.137 |              1.14  |                 1.194 |              1.279 |              1.202 |
| Copper      |   0.996 |       1.004 |     1     |   1.006 |         1.01  |          1.062 |       1.07  |              1.073 |                 1.121 |              1.12  |              1.103 |
| Corn        |   1.001 |       1.005 |     1.001 |   1.012 |         1.03  |          1.134 |       1.118 |              1.105 |                 1.152 |              1.164 |              1.166 |
| Gold        |   0.996 |       0.999 |     0.992 |   0.994 |         1.031 |          1.086 |       1.088 |              1.072 |                 1.104 |              1.264 |              1.384 |
| Natural gas |   0.99  |       1.001 |     1.001 |   1.001 |         0.998 |          1.058 |       1.044 |              1.05  |                 1.054 |              1.173 |              1.146 |
| Platinum    |   0.988 |       1.024 |     1     |   0.995 |         1.032 |          1.062 |       1.193 |              1.166 |                 1.06  |              1.182 |              1.137 |
| Silver      |   1.003 |       1.025 |     0.999 |   1.009 |         1.028 |          1.027 |       1.219 |              1.186 |                 0.987 |              1.196 |              1.123 |
| Soybeans    |   1     |       1.007 |     1.001 |   1.004 |         1.018 |          1.107 |       1.067 |              1.075 |                 1.206 |              1.173 |              1.178 |
| Wheat       |   1.004 |       1.005 |     1     |   1.005 |         1.04  |          1.041 |       1.338 |              1.3   |                 1.129 |              1.176 |              1.095 |
| WTI crude   |   1.265 |       2.019 |     1.003 |   0.883 |         0.866 |          1.069 |       1.075 |              1.074 |                 1.022 |              1.063 |              1.125 |

## Table 4. Median MSPE ratio by regime and horizon.

| ('model', '')       |   ('calm', 1) |   ('calm', 5) |   ('calm', 22) |   ('covid', 1) |   ('covid', 5) |   ('covid', 22) |   ('ukraine', 1) |   ('ukraine', 5) |   ('ukraine', 22) |
|:--------------------|--------------:|--------------:|---------------:|---------------:|---------------:|----------------:|-----------------:|-----------------:|------------------:|
| AR(5)               |         1.002 |         0.999 |          1.004 |          1.002 |          0.997 |           0.996 |            1.005 |            1.009 |             1.016 |
| LEAR-lite           |         1.006 |         1.008 |          1.017 |          1.01  |          1.01  |           1.013 |            1.008 |            1.008 |             1.036 |
| GARCH-t             |         1.001 |         1.005 |          1.02  |          1     |          1     |           1.003 |            1.003 |            1.013 |             1.053 |
| QR-AR               |         1.004 |         1.003 |          1.019 |          1.007 |          1.004 |           1.032 |            1.007 |            1.01  |             1.009 |
| TimesFM 2.5         |         1.026 |         1.024 |          1.051 |          1.039 |          1.019 |           1.028 |            1.017 |            0.991 |             0.973 |
| Moirai-2 (S)        |         1.073 |         1.024 |          1.056 |          1.097 |          1.036 |           1.049 |            1.09  |            1.05  |             1.086 |
| Chronos-2           |         1.086 |         1.052 |          1.085 |          1.109 |          1.031 |           0.978 |            1.052 |            1.017 |             1.061 |
| Chronos-2 + LoRA    |         1.076 |         1.052 |          1.068 |          1.101 |          1.031 |           0.979 |            1.046 |            1.025 |             1.077 |
| Chronos-2 + full FT |         1.105 |         1.049 |          1.045 |          1.063 |          1.035 |           0.987 |            1.116 |            1.038 |             1.098 |
| Chronos-Bolt (S)    |         1.182 |         1.095 |          1.162 |          1.159 |          1.071 |           1.064 |            1.162 |            1.062 |             1.107 |
| Chronos-Bolt (B)    |         1.152 |         1.112 |          1.254 |          1.118 |          1.064 |           1.125 |            1.12  |            1.087 |             1.079 |

## Table 5. Model Confidence Set at the 10% level under squared loss, computed separately in each of the 30 series-horizon cells. Survival share is the fraction of cells in which the model cannot be distinguished from the best.

| model               |   MCS survival share |   First eliminated (cells) |
|:--------------------|---------------------:|---------------------------:|
| No-change           |                0.933 |                          1 |
| AR(5)               |                0.967 |                          0 |
| LEAR-lite           |                0.867 |                          1 |
| GARCH-t             |                0.967 |                          0 |
| QR-AR               |                0.967 |                          1 |
| TimesFM 2.5         |                0.833 |                          0 |
| Moirai-2 (S)        |                0.633 |                          1 |
| Chronos-2           |                0.767 |                          1 |
| Chronos-2 + LoRA    |                0.733 |                          0 |
| Chronos-2 + full FT |                0.633 |                          2 |
| Chronos-Bolt (S)    |                0.533 |                          5 |
| Chronos-Bolt (B)    |                0.4   |                         12 |

## Table 6. Giacomini-White tests of conditional predictive ability against the no-change benchmark: share of commodities rejecting equal predictive ability at the 10% level. In every rejection the loss differential favours the benchmark.

| model               |   h = 1 |   h = 5 |   h = 22 |
|:--------------------|--------:|--------:|---------:|
| AR(5)               |     0.1 |     0.6 |      0.6 |
| LEAR-lite           |     0.4 |     0.7 |      0.4 |
| GARCH-t             |     0.2 |     1   |      0.6 |
| QR-AR               |     0.1 |     0.5 |      0.5 |
| TimesFM 2.5         |     0.3 |     0.7 |      0.4 |
| Moirai-2 (S)        |     0.8 |     0.8 |      0.7 |
| Chronos-2           |     0.6 |     0.4 |      0.4 |
| Chronos-2 + LoRA    |     0.5 |     0.3 |      0.4 |
| Chronos-2 + full FT |     0.8 |     0.5 |      0.6 |
| Chronos-Bolt (S)    |     0.9 |     0.7 |      0.5 |
| Chronos-Bolt (B)    |     0.9 |     0.7 |      0.8 |

## Table 6. Median empirical coverage of nominal 80% prediction intervals, by interval construction, regime and horizon, pooled across interval-producing models.

| ('Interval construction', '')   |   ('calm', 1) |   ('calm', 5) |   ('calm', 22) |   ('covid', 1) |   ('covid', 5) |   ('covid', 22) |   ('ukraine', 1) |   ('ukraine', 5) |   ('ukraine', 22) |
|:--------------------------------|--------------:|--------------:|---------------:|---------------:|---------------:|----------------:|-----------------:|-----------------:|------------------:|
| Native                          |         0.814 |         0.786 |          0.781 |          0.785 |          0.726 |           0.678 |            0.771 |            0.74  |             0.676 |
| Split conformal                 |         0.802 |         0.799 |          0.793 |          0.733 |          0.704 |           0.637 |            0.656 |            0.698 |             0.599 |
| ACI                             |         0.799 |         0.798 |          0.8   |          0.77  |          0.774 |           0.756 |            0.809 |            0.794 |             0.763 |
| CQR                             |         0.804 |         0.804 |          0.794 |          0.77  |          0.756 |           0.741 |            0.794 |            0.767 |             0.695 |
| SPCI-lite                       |         0.766 |         0.714 |          0.627 |          0.689 |          0.659 |           0.593 |            0.695 |            0.649 |             0.557 |

## Table 7. Native 80% interval coverage at h = 5 by model and regime. QR-AR, a classical model, has the weakest crisis coverage in the panel; TimesFM 2.5 the strongest.

| model               |   Calm |   COVID-19 |   Ukraine war |
|:--------------------|-------:|-----------:|--------------:|
| GARCH-t             |  0.796 |      0.737 |         0.732 |
| QR-AR               |  0.796 |      0.608 |         0.622 |
| TimesFM 2.5         |  0.811 |      0.792 |         0.809 |
| Moirai-2 (S)        |  0.787 |      0.722 |         0.748 |
| Chronos-2           |  0.782 |      0.74  |         0.764 |
| Chronos-2 + LoRA    |  0.783 |      0.733 |         0.748 |
| Chronos-2 + full FT |  0.753 |      0.696 |         0.718 |
| Chronos-Bolt (S)    |  0.77  |      0.715 |         0.756 |
| Chronos-Bolt (B)    |  0.792 |      0.737 |         0.729 |

## Table 8. Median interval width in calm periods at h = 5 (price units).

| Construction    |   Median width |
|:----------------|---------------:|
| Native          |          20.03 |
| Split conformal |          22.13 |
| ACI             |          24.99 |
| CQR             |          21.93 |
| SPCI-lite       |          19.07 |

## Table 9. Mean CRPS at h = 1 across the ten commodities. Lower is better.

| model               |   crps_ALL |
|:--------------------|-----------:|
| GARCH-t             |      3.681 |
| QR-AR               |      3.745 |
| TimesFM 2.5         |      3.804 |
| Moirai-2 (S)        |      3.759 |
| Chronos-2           |      3.802 |
| Chronos-2 + LoRA    |      3.788 |
| Chronos-2 + full FT |      3.919 |
| Chronos-Bolt (S)    |      3.956 |
| Chronos-Bolt (B)    |      3.957 |

## Table 11. Share of commodities passing the Kupiec unconditional-coverage backtest of the 95% value-at-risk (p > 0.05), by model and horizon. Only models with an unclamped 5th percentile are shown.

| model               |   h = 1 |   h = 5 |   h = 22 |
|:--------------------|--------:|--------:|---------:|
| GARCH-t             |     0.7 |     0.6 |      0.2 |
| QR-AR               |     0.6 |     0.5 |      0.6 |
| Moirai-2 (S)        |     0.7 |     0.7 |      0.3 |
| Chronos-2           |     0.6 |     0.5 |      0.4 |
| Chronos-2 + LoRA    |     0.8 |     0.3 |      0.4 |
| Chronos-2 + full FT |     0.1 |     0   |      0.2 |

## Table 10. The fine-tuning trade-off for Chronos-2: point accuracy, native 80% interval coverage at h = 5, and the share of commodities passing the Kupiec backtest of the 95% value-at-risk at h = 1.

| model               |   MSPE h=1 |   MSPE h=5 |   MSPE h=22 |   PICP calm |   PICP COVID |   PICP Ukraine |   VaR Kupiec pass (h=1) |
|:--------------------|-----------:|-----------:|------------:|------------:|-------------:|---------------:|------------------------:|
| Chronos-2           |     1.1028 |     1.0637 |      1.0956 |       0.782 |        0.74  |          0.764 |                     0.6 |
| Chronos-2 + LoRA    |     1.0901 |     1.0686 |      1.0707 |       0.783 |        0.733 |          0.748 |                     0.8 |
| Chronos-2 + full FT |     1.1128 |     1.0276 |      1.0309 |       0.753 |        0.696 |          0.718 |                     0.1 |

## Table 11. Sealed holdout: median MSPE ratio against the no-change benchmark in the Iran-Hormuz window, 2026-02-28 to 2026-07-31 (106 origins per cell). Evaluated once, after all specifications were frozen.

| model               |   h = 1 |   h = 5 |   h = 22 |
|:--------------------|--------:|--------:|---------:|
| AR(5)               |  1.0054 |  1.0014 |   1.0004 |
| LEAR-lite           |  1.025  |  1.038  |   1.031  |
| GARCH-t             |  1.0022 |  1.0074 |   1.0448 |
| QR-AR               |  1.0141 |  1.0209 |   1.0332 |
| TimesFM 2.5         |  1.0268 |  1.0278 |   0.9542 |
| Moirai-2 (S)        |  1.094  |  1.0466 |   0.9777 |
| Chronos-2           |  1.1018 |  1.0638 |   1.0634 |
| Chronos-2 + LoRA    |  1.1019 |  1.0814 |   1.0812 |
| Chronos-2 + full FT |  1.1608 |  1.0515 |   1.0085 |
| Chronos-Bolt (S)    |  1.1716 |  1.1365 |   1.2189 |
| Chronos-Bolt (B)    |  1.1374 |  1.1299 |   1.1092 |

## Table 12. Sealed holdout: median coverage of nominal 80% prediction intervals in the Iran-Hormuz window, pooled across models.

| Interval construction   |   h = 1 |   h = 5 |   h = 22 |
|:------------------------|--------:|--------:|---------:|
| Native                  |   0.783 |   0.783 |    0.694 |
| Split conformal         |   0.731 |   0.708 |    0.679 |
| ACI                     |   0.802 |   0.783 |    0.84  |
| CQR                     |   0.783 |   0.788 |    0.755 |
| SPCI-lite               |   0.708 |   0.698 |    0.599 |