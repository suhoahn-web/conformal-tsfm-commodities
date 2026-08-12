# Smoke Test A — Evaluation Pipeline Validation

Generated 2026-08-10T16:47:22.351844+00:00  |  test window 2023-01-01..2023-12-31 (calm regime, NOT the holdout)  |  cal_size=250

## Point forecasts (AR(5) vs no-change benchmark)

| series     |   h | model              |   mspe_ratio |   rmae |   success_ratio |   pt_pvalue |   dm_p_onesided |
|:-----------|----:|:-------------------|-------------:|-------:|----------------:|------------:|----------------:|
| wti_fut    |   1 | AR(5) vs no-change |       1.8227 | 1.3608 |           0.492 |       0.428 |           1     |
| wti_fut    |   5 | AR(5) vs no-change |       1.0677 | 1.0325 |           0.512 |       0.253 |           0.785 |
| gold_fut   |   1 | AR(5) vs no-change |       0.9986 | 0.999  |           0.484 |       0.729 |           0.307 |
| gold_fut   |   5 | AR(5) vs no-change |       0.9972 | 1.0007 |           0.516 |       0.586 |           0.294 |
| copper_fut |   1 | AR(5) vs no-change |       1.0076 | 0.9999 |           0.514 |       0.33  |           0.765 |
| copper_fut |   5 | AR(5) vs no-change |       0.9997 | 0.9966 |           0.582 |       0.003 |           0.479 |

## Conformal intervals

| series     |   h | model             |   nominal_cov |   picp |   mean_width |   winkler |
|:-----------|----:|:------------------|--------------:|-------:|-------------:|----------:|
| wti_fut    |   1 | no-change+splitCP |          0.8  |  0.888 |         5.23 |      6.21 |
| wti_fut    |   1 | no-change+ACI     |          0.8  |  0.776 |         3.91 |      5.8  |
| wti_fut    |   1 | no-change+splitCP |          0.95 |  0.98  |         9.3  |      9.89 |
| wti_fut    |   1 | no-change+ACI     |          0.95 |  0.944 |         6.13 |      8.3  |
| wti_fut    |   1 | AR(5)+splitCP     |          0.8  |  0.916 |         7.38 |      8.23 |
| wti_fut    |   1 | AR(5)+ACI         |          0.8  |  0.8   |         5.67 |      7.64 |
| wti_fut    |   1 | AR(5)+splitCP     |          0.95 |  0.984 |        11.53 |     11.96 |
| wti_fut    |   1 | AR(5)+ACI         |          0.95 |  0.936 |         8.66 |     10.56 |
| wti_fut    |   5 | no-change+splitCP |          0.8  |  0.924 |        11.99 |     13.3  |
| wti_fut    |   5 | no-change+ACI     |          0.8  |  0.804 |         9.48 |     12.5  |
| wti_fut    |   5 | no-change+splitCP |          0.95 |  0.984 |        19.18 |     19.99 |
| wti_fut    |   5 | no-change+ACI     |          0.95 |  0.944 |        13.44 |     17.24 |
| wti_fut    |   5 | AR(5)+splitCP     |          0.8  |  0.908 |        11.93 |     13.4  |
| wti_fut    |   5 | AR(5)+ACI         |          0.8  |  0.8   |         9.56 |     12.8  |
| wti_fut    |   5 | AR(5)+splitCP     |          0.95 |  0.992 |        18.75 |     18.79 |
| wti_fut    |   5 | AR(5)+ACI         |          0.95 |  0.944 |        14.31 |     16.79 |
| gold_fut   |   1 | no-change+splitCP |          0.8  |  0.836 |        41.98 |     60.6  |
| gold_fut   |   1 | no-change+ACI     |          0.8  |  0.796 |        38.03 |     60.31 |
| gold_fut   |   1 | no-change+splitCP |          0.95 |  0.956 |        72.8  |     91.56 |
| gold_fut   |   1 | no-change+ACI     |          0.95 |  0.952 |        68.18 |     87.57 |
| gold_fut   |   1 | AR(5)+splitCP     |          0.8  |  0.832 |        41.93 |     60.57 |
| gold_fut   |   1 | AR(5)+ACI         |          0.8  |  0.8   |        38.5  |     60.59 |
| gold_fut   |   1 | AR(5)+splitCP     |          0.95 |  0.964 |        73.18 |     91.56 |
| gold_fut   |   1 | AR(5)+ACI         |          0.95 |  0.948 |        67.49 |     87.88 |
| gold_fut   |   5 | no-change+splitCP |          0.8  |  0.796 |        89.92 |    128.57 |
| gold_fut   |   5 | no-change+ACI     |          0.8  |  0.788 |        87.25 |    127.28 |
| gold_fut   |   5 | no-change+splitCP |          0.95 |  0.956 |       148.04 |    180.01 |
| gold_fut   |   5 | no-change+ACI     |          0.95 |  0.956 |       145.41 |    178.93 |
| gold_fut   |   5 | AR(5)+splitCP     |          0.8  |  0.792 |        90.2  |    128.33 |
| gold_fut   |   5 | AR(5)+ACI         |          0.8  |  0.792 |        85.88 |    127.53 |
| gold_fut   |   5 | AR(5)+splitCP     |          0.95 |  0.956 |       147.9  |    179.29 |
| gold_fut   |   5 | AR(5)+ACI         |          0.95 |  0.952 |       141.63 |    179.8  |
| copper_fut |   1 | no-change+splitCP |          0.8  |  0.869 |         0.15 |      0.18 |
| copper_fut |   1 | no-change+ACI     |          0.8  |  0.805 |         0.13 |      0.18 |
| copper_fut |   1 | no-change+splitCP |          0.95 |  0.988 |         0.25 |      0.26 |
| copper_fut |   1 | no-change+ACI     |          0.95 |  0.956 |         0.21 |      0.23 |
| copper_fut |   1 | AR(5)+splitCP     |          0.8  |  0.869 |         0.15 |      0.18 |
| copper_fut |   1 | AR(5)+ACI         |          0.8  |  0.805 |         0.13 |      0.18 |
| copper_fut |   1 | AR(5)+splitCP     |          0.95 |  0.988 |         0.25 |      0.26 |
| copper_fut |   1 | AR(5)+ACI         |          0.95 |  0.956 |         0.2  |      0.23 |
| copper_fut |   5 | no-change+splitCP |          0.8  |  0.928 |         0.35 |      0.38 |
| copper_fut |   5 | no-change+ACI     |          0.8  |  0.833 |         0.28 |      0.35 |
| copper_fut |   5 | no-change+splitCP |          0.95 |  0.992 |         0.55 |      0.57 |
| copper_fut |   5 | no-change+ACI     |          0.95 |  0.972 |         0.44 |      0.48 |
| copper_fut |   5 | AR(5)+splitCP     |          0.8  |  0.928 |         0.35 |      0.39 |
| copper_fut |   5 | AR(5)+ACI         |          0.8  |  0.837 |         0.27 |      0.35 |
| copper_fut |   5 | AR(5)+splitCP     |          0.95 |  0.992 |         0.55 |      0.58 |
| copper_fut |   5 | AR(5)+ACI         |          0.95 |  0.972 |         0.44 |      0.48 |

## Pass criteria
- [ ] MSPE ratios near 1.0 (daily prices ~ random walk — AR should NOT dominate; a ratio far below 1 signals leakage)
- [ ] split-CP and ACI PICP within ~3pp of nominal in this calm window
- [ ] no exceptions, no silent NaN drops (enforced in metrics module)