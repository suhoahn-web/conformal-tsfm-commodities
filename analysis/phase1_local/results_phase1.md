# Phase 1 Results — Local Models (EMBARGOED: no Hormuz window)

Generated 2026-08-11T18:23:58.834285+00:00 | eval 2015-01-01..2026-02-27 | regimes: calm / covid / ukraine | cal_size=250

Missing caches (0): none

## Point forecasts vs no-change — median MSPE ratio by model x regime x h

|                                   |      1 |      5 |     22 |
|:----------------------------------|-------:|-------:|-------:|
| ('ar5_returns', 'ALL')            | 1.0008 | 0.9956 | 1.0016 |
| ('ar5_returns', 'calm')           | 1.0018 | 0.9989 | 1.0044 |
| ('ar5_returns', 'covid')          | 1.0021 | 0.997  | 0.9956 |
| ('ar5_returns', 'ukraine')        | 1.0048 | 1.009  | 1.0162 |
| ('chronos_2', 'ALL')              | 1.1028 | 1.0637 | 1.0956 |
| ('chronos_2', 'calm')             | 1.0865 | 1.052  | 1.0846 |
| ('chronos_2', 'covid')            | 1.1089 | 1.0312 | 0.9775 |
| ('chronos_2', 'ukraine')          | 1.0518 | 1.0171 | 1.0606 |
| ('chronos_2_full', 'ALL')         | 1.1128 | 1.0276 | 1.0309 |
| ('chronos_2_full', 'calm')        | 1.1048 | 1.0492 | 1.0448 |
| ('chronos_2_full', 'covid')       | 1.0627 | 1.0348 | 0.9866 |
| ('chronos_2_full', 'ukraine')     | 1.1161 | 1.038  | 1.0985 |
| ('chronos_2_lora', 'ALL')         | 1.0901 | 1.0686 | 1.0707 |
| ('chronos_2_lora', 'calm')        | 1.0764 | 1.0524 | 1.068  |
| ('chronos_2_lora', 'covid')       | 1.1006 | 1.0314 | 0.9794 |
| ('chronos_2_lora', 'ukraine')     | 1.0459 | 1.0246 | 1.0766 |
| ('chronos_bolt_base', 'ALL')      | 1.1415 | 1.1046 | 1.1635 |
| ('chronos_bolt_base', 'calm')     | 1.1522 | 1.1122 | 1.2541 |
| ('chronos_bolt_base', 'covid')    | 1.1182 | 1.0642 | 1.1252 |
| ('chronos_bolt_base', 'ukraine')  | 1.1201 | 1.0865 | 1.0788 |
| ('chronos_bolt_small', 'ALL')     | 1.1746 | 1.0798 | 1.1048 |
| ('chronos_bolt_small', 'calm')    | 1.1815 | 1.0947 | 1.1617 |
| ('chronos_bolt_small', 'covid')   | 1.1594 | 1.0708 | 1.0645 |
| ('chronos_bolt_small', 'ukraine') | 1.162  | 1.062  | 1.1073 |
| ('garch_t', 'ALL')                | 1.0006 | 1.0024 | 1.0099 |
| ('garch_t', 'calm')               | 1.001  | 1.0047 | 1.0203 |
| ('garch_t', 'covid')              | 1      | 1.0004 | 1.0027 |
| ('garch_t', 'ukraine')            | 1.0032 | 1.0134 | 1.0534 |
| ('lear_lite', 'ALL')              | 1.0061 | 1.0078 | 1.0221 |
| ('lear_lite', 'calm')             | 1.0059 | 1.0084 | 1.0166 |
| ('lear_lite', 'covid')            | 1.0098 | 1.0099 | 1.0129 |
| ('lear_lite', 'ukraine')          | 1.0078 | 1.0085 | 1.0358 |
| ('moirai2_small', 'ALL')          | 1.0658 | 1.0326 | 1.0658 |
| ('moirai2_small', 'calm')         | 1.0729 | 1.0244 | 1.056  |
| ('moirai2_small', 'covid')        | 1.0968 | 1.0358 | 1.0492 |
| ('moirai2_small', 'ukraine')      | 1.0896 | 1.0502 | 1.0856 |
| ('qr_ar', 'ALL')                  | 1.0041 | 0.9936 | 1.0125 |
| ('qr_ar', 'calm')                 | 1.0042 | 1.0031 | 1.0192 |
| ('qr_ar', 'covid')                | 1.007  | 1.0038 | 1.0316 |
| ('qr_ar', 'ukraine')              | 1.0068 | 1.0101 | 1.0092 |
| ('timesfm_25', 'ALL')             | 1.0286 | 1.0204 | 1.0358 |
| ('timesfm_25', 'calm')            | 1.0262 | 1.0244 | 1.051  |
| ('timesfm_25', 'covid')           | 1.0393 | 1.0194 | 1.0284 |
| ('timesfm_25', 'ukraine')         | 1.0174 | 0.9912 | 0.9729 |

### Per-series detail (h=1, ALL)

| model              | series       |    n |   mspe_ratio |   rmae |    sr |   pt_p |   dm_p |
|:-------------------|:-------------|-----:|-------------:|-------:|------:|-------:|-------:|
| ar5_returns        | wti_fut      | 2805 |       1.2649 | 1.2188 | 0.499 |  0.394 |  0.997 |
| ar5_returns        | brent_fut    | 2806 |       1.0058 | 1.0028 | 0.503 |  0.279 |  0.956 |
| ar5_returns        | natgas_fut   | 2806 |       0.9899 | 0.9971 | 0.525 |  0.003 |  0.095 |
| ar5_returns        | gold_fut     | 2804 |       0.9964 | 0.997  | 0.527 |  0.722 |  0.136 |
| ar5_returns        | silver_fut   | 2804 |       1.0026 | 1.0014 | 0.506 |  0.539 |  0.636 |
| ar5_returns        | copper_fut   | 2805 |       0.9956 | 0.9975 | 0.498 |  0.559 |  0.161 |
| ar5_returns        | platinum_fut | 2803 |       0.9884 | 0.9973 | 0.503 |  0.381 |  0.107 |
| ar5_returns        | corn_fut     | 2802 |       1.0014 | 1.0017 | 0.485 |  0.853 |  0.709 |
| ar5_returns        | wheat_fut    | 2804 |       1.004  | 1.002  | 0.476 |  0.872 |  0.894 |
| ar5_returns        | soybean_fut  | 2804 |       1.0002 | 1.0003 | 0.495 |  0.612 |  0.525 |
| lear_lite          | wti_fut      | 2805 |       2.0189 | 1.4146 | 0.502 |  0.165 |  1     |
| lear_lite          | brent_fut    | 2806 |       1.0273 | 1.0166 | 0.501 |  0.3   |  0.999 |
| lear_lite          | natgas_fut   | 2806 |       1.0013 | 1.0025 | 0.511 |  0.066 |  0.567 |
| lear_lite          | gold_fut     | 2804 |       0.9988 | 1.001  | 0.514 |  0.213 |  0.381 |
| lear_lite          | silver_fut   | 2804 |       1.0247 | 1.014  | 0.496 |  0.649 |  0.915 |
| lear_lite          | copper_fut   | 2805 |       1.0039 | 1.0018 | 0.489 |  0.769 |  0.918 |
| lear_lite          | platinum_fut | 2803 |       1.0239 | 1.0108 | 0.491 |  0.632 |  0.984 |
| lear_lite          | corn_fut     | 2802 |       1.0048 | 1.0028 | 0.49  |  0.567 |  0.978 |
| lear_lite          | wheat_fut    | 2804 |       1.0052 | 1.0046 | 0.468 |  0.996 |  0.997 |
| lear_lite          | soybean_fut  | 2804 |       1.0069 | 1.0036 | 0.5   |  0.221 |  0.98  |
| garch_t            | wti_fut      | 2805 |       1.0028 | 0.9991 | 0.512 |  0.927 |  0.929 |
| garch_t            | brent_fut    | 2806 |       1.0048 | 0.9991 | 0.509 |  0.458 |  0.922 |
| garch_t            | natgas_fut   | 2806 |       1.0006 | 1      | 0.506 |  0.203 |  0.808 |
| garch_t            | gold_fut     | 2804 |       0.9924 | 0.9951 | 0.52  |  0.436 |  0.073 |
| garch_t            | silver_fut   | 2804 |       0.9989 | 0.998  | 0.523 |  0.074 |  0.346 |
| garch_t            | copper_fut   | 2805 |       1.0001 | 1.0001 | 0.493 |  0.648 |  0.523 |
| garch_t            | platinum_fut | 2803 |       0.9996 | 1.0005 | 0.483 |  0.916 |  0.361 |
| garch_t            | corn_fut     | 2802 |       1.0012 | 1.0003 | 0.488 |  0.754 |  0.853 |
| garch_t            | wheat_fut    | 2804 |       1.0005 | 1      | 0.5   |  0.789 |  0.857 |
| garch_t            | soybean_fut  | 2804 |       1.0013 | 1.0005 | 0.5   |  0.688 |  0.921 |
| qr_ar              | wti_fut      | 2805 |       0.8826 | 0.9973 | 0.524 |  0.045 |  0.19  |
| qr_ar              | brent_fut    | 2806 |       1.0115 | 1.0018 | 0.518 |  0.151 |  0.973 |
| qr_ar              | natgas_fut   | 2806 |       1.0013 | 1.0004 | 0.51  |  0.114 |  0.569 |
| qr_ar              | gold_fut     | 2804 |       0.9937 | 0.9988 | 0.512 |  0.299 |  0.238 |
| qr_ar              | silver_fut   | 2804 |       1.009  | 1.0038 | 0.508 |  0.249 |  0.756 |
| qr_ar              | copper_fut   | 2805 |       1.0061 | 1.0034 | 0.5   |  0.357 |  0.854 |
| qr_ar              | platinum_fut | 2803 |       0.995  | 0.9992 | 0.502 |  0.514 |  0.389 |
| qr_ar              | corn_fut     | 2802 |       1.0122 | 1.0038 | 0.485 |  0.842 |  0.972 |
| qr_ar              | wheat_fut    | 2804 |       1.0046 | 1.0025 | 0.514 |  0.034 |  0.636 |
| qr_ar              | soybean_fut  | 2804 |       1.0036 | 1.0032 | 0.497 |  0.573 |  0.879 |
| chronos_bolt_small | wti_fut      | 2805 |       1.0633 | 1.1146 | 0.499 |  0.669 |  0.737 |
| chronos_bolt_small | brent_fut    | 2806 |       1.2787 | 1.1517 | 0.505 |  0.396 |  1     |
| chronos_bolt_small | natgas_fut   | 2806 |       1.1729 | 1.0939 | 0.51  |  0.139 |  0.999 |
| chronos_bolt_small | gold_fut     | 2804 |       1.2639 | 1.0913 | 0.525 |  0.052 |  0.99  |
| chronos_bolt_small | silver_fut   | 2804 |       1.1959 | 1.0714 | 0.508 |  0.399 |  0.871 |
| chronos_bolt_small | copper_fut   | 2805 |       1.1205 | 1.074  | 0.522 |  0.012 |  1     |
| chronos_bolt_small | platinum_fut | 2803 |       1.1817 | 1.0671 | 0.468 |  1     |  0.986 |
| chronos_bolt_small | corn_fut     | 2802 |       1.1645 | 1.0935 | 0.5   |  0.212 |  1     |
| chronos_bolt_small | wheat_fut    | 2804 |       1.1763 | 1.069  | 0.496 |  0.284 |  0.983 |
| chronos_bolt_small | soybean_fut  | 2804 |       1.1726 | 1.0912 | 0.493 |  0.672 |  1     |
| chronos_bolt_base  | wti_fut      | 2805 |       1.1246 | 1.114  | 0.507 |  0.214 |  1     |
| chronos_bolt_base  | brent_fut    | 2806 |       1.2022 | 1.1121 | 0.517 |  0.024 |  1     |
| chronos_bolt_base  | natgas_fut   | 2806 |       1.1459 | 1.0969 | 0.502 |  0.389 |  1     |
| chronos_bolt_base  | gold_fut     | 2804 |       1.3843 | 1.1142 | 0.527 |  0.023 |  0.983 |
| chronos_bolt_base  | silver_fut   | 2804 |       1.1227 | 1.0908 | 0.517 |  0.033 |  1     |
| chronos_bolt_base  | copper_fut   | 2805 |       1.1026 | 1.0823 | 0.519 |  0.021 |  1     |
| chronos_bolt_base  | platinum_fut | 2803 |       1.1371 | 1.0674 | 0.498 |  0.397 |  0.997 |
| chronos_bolt_base  | corn_fut     | 2802 |       1.1661 | 1.1071 | 0.485 |  0.737 |  1     |
| chronos_bolt_base  | wheat_fut    | 2804 |       1.0952 | 1.054  | 0.496 |  0.416 |  0.972 |
| chronos_bolt_base  | soybean_fut  | 2804 |       1.1785 | 1.0951 | 0.489 |  0.647 |  1     |
| chronos_2          | wti_fut      | 2805 |       1.0748 | 1.042  | 0.496 |  0.617 |  1     |
| chronos_2          | brent_fut    | 2806 |       1.1369 | 1.0465 | 0.495 |  0.537 |  0.954 |
| chronos_2          | natgas_fut   | 2806 |       1.0441 | 1.0325 | 0.517 |  0.03  |  0.951 |
| chronos_2          | gold_fut     | 2804 |       1.0877 | 1.0545 | 0.494 |  0.256 |  0.895 |
| chronos_2          | silver_fut   | 2804 |       1.2189 | 1.0545 | 0.491 |  0.638 |  0.912 |
| chronos_2          | copper_fut   | 2805 |       1.0704 | 1.0427 | 0.507 |  0.11  |  0.999 |
| chronos_2          | platinum_fut | 2803 |       1.1926 | 1.0273 | 0.491 |  0.514 |  0.917 |
| chronos_2          | corn_fut     | 2802 |       1.1179 | 1.0609 | 0.463 |  0.429 |  1     |
| chronos_2          | wheat_fut    | 2804 |       1.3376 | 1.0482 | 0.465 |  0.748 |  0.931 |
| chronos_2          | soybean_fut  | 2804 |       1.0671 | 1.0496 | 0.468 |  0.94  |  1     |
| chronos_2_lora     | wti_fut      | 2805 |       1.0741 | 1.0388 | 0.503 |  0.685 |  1     |
| chronos_2_lora     | brent_fut    | 2806 |       1.1399 | 1.0467 | 0.516 |  0.091 |  0.958 |
| chronos_2_lora     | natgas_fut   | 2806 |       1.0496 | 1.0356 | 0.513 |  0.06  |  0.964 |
| chronos_2_lora     | gold_fut     | 2804 |       1.0725 | 1.0391 | 0.517 |  0.021 |  0.84  |
| chronos_2_lora     | silver_fut   | 2804 |       1.1861 | 1.0458 | 0.499 |  0.672 |  0.927 |
| chronos_2_lora     | copper_fut   | 2805 |       1.0728 | 1.0368 | 0.51  |  0.106 |  0.999 |
| chronos_2_lora     | platinum_fut | 2803 |       1.1663 | 1.0145 | 0.499 |  0.327 |  0.884 |
| chronos_2_lora     | corn_fut     | 2802 |       1.1049 | 1.0548 | 0.475 |  0.174 |  1     |
| chronos_2_lora     | wheat_fut    | 2804 |       1.3005 | 1.0486 | 0.462 |  0.633 |  0.929 |
| chronos_2_lora     | soybean_fut  | 2804 |       1.0753 | 1.0519 | 0.471 |  0.963 |  1     |
| chronos_2_full     | wti_fut      | 2805 |       1.0224 | 1.0769 | 0.501 |  0.619 |  0.607 |
| chronos_2_full     | brent_fut    | 2806 |       1.1937 | 1.1129 | 0.504 |  0.413 |  1     |
| chronos_2_full     | natgas_fut   | 2806 |       1.0537 | 1.0521 | 0.521 |  0.01  |  0.973 |
| chronos_2_full     | gold_fut     | 2804 |       1.1045 | 1.061  | 0.51  |  0.027 |  0.94  |
| chronos_2_full     | silver_fut   | 2804 |       0.9869 | 1.0613 | 0.488 |  0.885 |  0.424 |
| chronos_2_full     | copper_fut   | 2805 |       1.121  | 1.0807 | 0.492 |  0.733 |  1     |
| chronos_2_full     | platinum_fut | 2803 |       1.0605 | 1.0483 | 0.503 |  0.353 |  0.987 |
| chronos_2_full     | corn_fut     | 2802 |       1.152  | 1.1087 | 0.481 |  0.222 |  1     |
| chronos_2_full     | wheat_fut    | 2804 |       1.1293 | 1.0452 | 0.478 |  0.273 |  0.999 |
| chronos_2_full     | soybean_fut  | 2804 |       1.2059 | 1.1199 | 0.482 |  0.778 |  1     |
| timesfm_25         | wti_fut      | 2805 |       0.8656 | 0.999  | 0.521 |  0.022 |  0.179 |
| timesfm_25         | brent_fut    | 2806 |       1.0356 | 1.0149 | 0.517 |  0.054 |  0.999 |
| timesfm_25         | natgas_fut   | 2806 |       0.9985 | 1.0148 | 0.506 |  0.246 |  0.475 |
| timesfm_25         | gold_fut     | 2804 |       1.0313 | 1.0223 | 0.504 |  0.225 |  0.956 |
| timesfm_25         | silver_fut   | 2804 |       1.0277 | 1.0227 | 0.517 |  0.014 |  0.728 |
| timesfm_25         | copper_fut   | 2805 |       1.0096 | 1.0063 | 0.504 |  0.335 |  0.852 |
| timesfm_25         | platinum_fut | 2803 |       1.0321 | 1.0103 | 0.507 |  0.209 |  0.972 |
| timesfm_25         | corn_fut     | 2802 |       1.0296 | 1.0171 | 0.493 |  0.505 |  0.995 |
| timesfm_25         | wheat_fut    | 2804 |       1.0405 | 1.0091 | 0.509 |  0.073 |  0.843 |
| timesfm_25         | soybean_fut  | 2804 |       1.0185 | 1.0159 | 0.495 |  0.429 |  0.976 |
| moirai2_small      | wti_fut      | 2805 |       1.069  | 1.0435 | 0.52  |  0.027 |  1     |
| moirai2_small      | brent_fut    | 2806 |       1.1396 | 1.0549 | 0.511 |  0.21  |  1     |
| moirai2_small      | natgas_fut   | 2806 |       1.0576 | 1.0293 | 0.516 |  0.049 |  1     |
| moirai2_small      | gold_fut     | 2804 |       1.0862 | 1.0171 | 0.546 |  0     |  0.976 |
| moirai2_small      | silver_fut   | 2804 |       1.0267 | 1.021  | 0.519 |  0.082 |  0.71  |
| moirai2_small      | copper_fut   | 2805 |       1.0625 | 1.0438 | 0.525 |  0.004 |  1     |
| moirai2_small      | platinum_fut | 2803 |       1.0618 | 1.0138 | 0.512 |  0.113 |  0.887 |
| moirai2_small      | corn_fut     | 2802 |       1.1342 | 1.0435 | 0.488 |  0.685 |  1     |
| moirai2_small      | wheat_fut    | 2804 |       1.0408 | 1.0298 | 0.49  |  0.452 |  0.99  |
| moirai2_small      | soybean_fut  | 2804 |       1.1069 | 1.0437 | 0.504 |  0.129 |  1     |

## Interval calibration — median PICP (nominal 0.80) by band x regime x h

|                                                |     1 |     5 |    22 |
|:-----------------------------------------------|------:|------:|------:|
| ('chronos_2', 'ACI80', 'ALL')                  | 0.798 | 0.8   | 0.798 |
| ('chronos_2', 'ACI80', 'calm')                 | 0.798 | 0.799 | 0.802 |
| ('chronos_2', 'ACI80', 'covid')                | 0.77  | 0.774 | 0.756 |
| ('chronos_2', 'ACI80', 'ukraine')              | 0.816 | 0.798 | 0.764 |
| ('chronos_2', 'ACI90', 'ALL')                  | 0.899 | 0.9   | 0.895 |
| ('chronos_2', 'ACI90', 'calm')                 | 0.899 | 0.9   | 0.897 |
| ('chronos_2', 'ACI90', 'covid')                | 0.881 | 0.881 | 0.822 |
| ('chronos_2', 'ACI90', 'ukraine')              | 0.916 | 0.885 | 0.874 |
| ('chronos_2', 'CQR80', 'ALL')                  | 0.804 | 0.798 | 0.788 |
| ('chronos_2', 'CQR80', 'calm')                 | 0.806 | 0.802 | 0.795 |
| ('chronos_2', 'CQR80', 'covid')                | 0.756 | 0.76  | 0.737 |
| ('chronos_2', 'CQR80', 'ukraine')              | 0.824 | 0.798 | 0.714 |
| ('chronos_2', 'CQR90', 'ALL')                  | 0.903 | 0.898 | 0.88  |
| ('chronos_2', 'CQR90', 'calm')                 | 0.903 | 0.9   | 0.887 |
| ('chronos_2', 'CQR90', 'covid')                | 0.885 | 0.866 | 0.837 |
| ('chronos_2', 'CQR90', 'ukraine')              | 0.912 | 0.882 | 0.832 |
| ('chronos_2', 'SPCI80', 'ALL')                 | 0.758 | 0.704 | 0.62  |
| ('chronos_2', 'SPCI80', 'calm')                | 0.765 | 0.71  | 0.626 |
| ('chronos_2', 'SPCI80', 'covid')               | 0.696 | 0.663 | 0.578 |
| ('chronos_2', 'SPCI80', 'ukraine')             | 0.698 | 0.638 | 0.557 |
| ('chronos_2', 'SPCI90', 'ALL')                 | 0.857 | 0.804 | 0.708 |
| ('chronos_2', 'SPCI90', 'calm')                | 0.862 | 0.811 | 0.716 |
| ('chronos_2', 'SPCI90', 'covid')               | 0.808 | 0.744 | 0.667 |
| ('chronos_2', 'SPCI90', 'ukraine')             | 0.782 | 0.714 | 0.606 |
| ('chronos_2', 'native80', 'ALL')               | 0.814 | 0.78  | 0.784 |
| ('chronos_2', 'native80', 'calm')              | 0.816 | 0.782 | 0.788 |
| ('chronos_2', 'native80', 'covid')             | 0.789 | 0.74  | 0.726 |
| ('chronos_2', 'native80', 'ukraine')           | 0.806 | 0.764 | 0.683 |
| ('chronos_2', 'native90', 'ALL')               | 0.916 | 0.883 | 0.89  |
| ('chronos_2', 'native90', 'calm')              | 0.918 | 0.886 | 0.897 |
| ('chronos_2', 'native90', 'covid')             | 0.9   | 0.833 | 0.804 |
| ('chronos_2', 'native90', 'ukraine')           | 0.913 | 0.87  | 0.813 |
| ('chronos_2', 'splitCP80', 'ALL')              | 0.795 | 0.789 | 0.78  |
| ('chronos_2', 'splitCP80', 'calm')             | 0.803 | 0.795 | 0.795 |
| ('chronos_2', 'splitCP80', 'covid')            | 0.74  | 0.711 | 0.693 |
| ('chronos_2', 'splitCP80', 'ukraine')          | 0.683 | 0.71  | 0.595 |
| ('chronos_2', 'splitCP90', 'ALL')              | 0.895 | 0.887 | 0.882 |
| ('chronos_2', 'splitCP90', 'calm')             | 0.901 | 0.893 | 0.887 |
| ('chronos_2', 'splitCP90', 'covid')            | 0.848 | 0.841 | 0.818 |
| ('chronos_2', 'splitCP90', 'ukraine')          | 0.82  | 0.82  | 0.744 |
| ('chronos_2_full', 'ACI80', 'ALL')             | 0.799 | 0.8   | 0.798 |
| ('chronos_2_full', 'ACI80', 'calm')            | 0.798 | 0.798 | 0.803 |
| ('chronos_2_full', 'ACI80', 'covid')           | 0.778 | 0.782 | 0.752 |
| ('chronos_2_full', 'ACI80', 'ukraine')         | 0.809 | 0.79  | 0.756 |
| ('chronos_2_full', 'ACI90', 'ALL')             | 0.9   | 0.9   | 0.896 |
| ('chronos_2_full', 'ACI90', 'calm')            | 0.9   | 0.9   | 0.899 |
| ('chronos_2_full', 'ACI90', 'covid')           | 0.889 | 0.885 | 0.852 |
| ('chronos_2_full', 'ACI90', 'ukraine')         | 0.909 | 0.897 | 0.901 |
| ('chronos_2_full', 'CQR80', 'ALL')             | 0.81  | 0.804 | 0.794 |
| ('chronos_2_full', 'CQR80', 'calm')            | 0.814 | 0.808 | 0.801 |
| ('chronos_2_full', 'CQR80', 'covid')           | 0.756 | 0.744 | 0.752 |
| ('chronos_2_full', 'CQR80', 'ukraine')         | 0.756 | 0.756 | 0.687 |
| ('chronos_2_full', 'CQR90', 'ALL')             | 0.907 | 0.9   | 0.892 |
| ('chronos_2_full', 'CQR90', 'calm')            | 0.91  | 0.905 | 0.903 |
| ('chronos_2_full', 'CQR90', 'covid')           | 0.878 | 0.851 | 0.84  |
| ('chronos_2_full', 'CQR90', 'ukraine')         | 0.897 | 0.87  | 0.824 |
| ('chronos_2_full', 'SPCI80', 'ALL')            | 0.756 | 0.707 | 0.618 |
| ('chronos_2_full', 'SPCI80', 'calm')           | 0.766 | 0.712 | 0.624 |
| ('chronos_2_full', 'SPCI80', 'covid')          | 0.667 | 0.648 | 0.563 |
| ('chronos_2_full', 'SPCI80', 'ukraine')        | 0.683 | 0.634 | 0.569 |
| ('chronos_2_full', 'SPCI90', 'ALL')            | 0.856 | 0.802 | 0.702 |
| ('chronos_2_full', 'SPCI90', 'calm')           | 0.863 | 0.81  | 0.711 |
| ('chronos_2_full', 'SPCI90', 'covid')          | 0.792 | 0.73  | 0.645 |
| ('chronos_2_full', 'SPCI90', 'ukraine')        | 0.767 | 0.718 | 0.614 |
| ('chronos_2_full', 'native80', 'ALL')          | 0.74  | 0.748 | 0.747 |
| ('chronos_2_full', 'native80', 'calm')         | 0.743 | 0.753 | 0.756 |
| ('chronos_2_full', 'native80', 'covid')        | 0.685 | 0.696 | 0.66  |
| ('chronos_2_full', 'native80', 'ukraine')      | 0.714 | 0.718 | 0.653 |
| ('chronos_2_full', 'native90', 'ALL')          | 0.861 | 0.852 | 0.861 |
| ('chronos_2_full', 'native90', 'calm')         | 0.863 | 0.858 | 0.867 |
| ('chronos_2_full', 'native90', 'covid')        | 0.811 | 0.782 | 0.8   |
| ('chronos_2_full', 'native90', 'ukraine')      | 0.859 | 0.839 | 0.794 |
| ('chronos_2_full', 'splitCP80', 'ALL')         | 0.796 | 0.796 | 0.788 |
| ('chronos_2_full', 'splitCP80', 'calm')        | 0.806 | 0.802 | 0.801 |
| ('chronos_2_full', 'splitCP80', 'covid')       | 0.73  | 0.704 | 0.682 |
| ('chronos_2_full', 'splitCP80', 'ukraine')     | 0.626 | 0.71  | 0.588 |
| ('chronos_2_full', 'splitCP90', 'ALL')         | 0.898 | 0.891 | 0.881 |
| ('chronos_2_full', 'splitCP90', 'calm')        | 0.903 | 0.897 | 0.888 |
| ('chronos_2_full', 'splitCP90', 'covid')       | 0.851 | 0.833 | 0.814 |
| ('chronos_2_full', 'splitCP90', 'ukraine')     | 0.81  | 0.817 | 0.729 |
| ('chronos_2_lora', 'ACI80', 'ALL')             | 0.799 | 0.8   | 0.798 |
| ('chronos_2_lora', 'ACI80', 'calm')            | 0.798 | 0.799 | 0.801 |
| ('chronos_2_lora', 'ACI80', 'covid')           | 0.77  | 0.77  | 0.748 |
| ('chronos_2_lora', 'ACI80', 'ukraine')         | 0.813 | 0.798 | 0.76  |
| ('chronos_2_lora', 'ACI90', 'ALL')             | 0.9   | 0.9   | 0.896 |
| ('chronos_2_lora', 'ACI90', 'calm')            | 0.899 | 0.9   | 0.898 |
| ('chronos_2_lora', 'ACI90', 'covid')           | 0.885 | 0.878 | 0.837 |
| ('chronos_2_lora', 'ACI90', 'ukraine')         | 0.908 | 0.893 | 0.874 |
| ('chronos_2_lora', 'CQR80', 'ALL')             | 0.804 | 0.799 | 0.788 |
| ('chronos_2_lora', 'CQR80', 'calm')            | 0.805 | 0.805 | 0.798 |
| ('chronos_2_lora', 'CQR80', 'covid')           | 0.76  | 0.76  | 0.741 |
| ('chronos_2_lora', 'CQR80', 'ukraine')         | 0.82  | 0.778 | 0.702 |
| ('chronos_2_lora', 'CQR90', 'ALL')             | 0.903 | 0.899 | 0.883 |
| ('chronos_2_lora', 'CQR90', 'calm')            | 0.903 | 0.899 | 0.89  |
| ('chronos_2_lora', 'CQR90', 'covid')           | 0.874 | 0.874 | 0.84  |
| ('chronos_2_lora', 'CQR90', 'ukraine')         | 0.912 | 0.886 | 0.832 |
| ('chronos_2_lora', 'SPCI80', 'ALL')            | 0.757 | 0.712 | 0.62  |
| ('chronos_2_lora', 'SPCI80', 'calm')           | 0.764 | 0.716 | 0.624 |
| ('chronos_2_lora', 'SPCI80', 'covid')          | 0.682 | 0.671 | 0.589 |
| ('chronos_2_lora', 'SPCI80', 'ukraine')        | 0.702 | 0.653 | 0.565 |
| ('chronos_2_lora', 'SPCI90', 'ALL')            | 0.856 | 0.806 | 0.705 |
| ('chronos_2_lora', 'SPCI90', 'calm')           | 0.864 | 0.813 | 0.712 |
| ('chronos_2_lora', 'SPCI90', 'covid')          | 0.815 | 0.752 | 0.678 |
| ('chronos_2_lora', 'SPCI90', 'ukraine')        | 0.794 | 0.718 | 0.599 |
| ('chronos_2_lora', 'native80', 'ALL')          | 0.815 | 0.779 | 0.786 |
| ('chronos_2_lora', 'native80', 'calm')         | 0.815 | 0.783 | 0.791 |
| ('chronos_2_lora', 'native80', 'covid')        | 0.786 | 0.733 | 0.734 |
| ('chronos_2_lora', 'native80', 'ukraine')      | 0.798 | 0.748 | 0.687 |
| ('chronos_2_lora', 'native90', 'ALL')          | 0.915 | 0.881 | 0.892 |
| ('chronos_2_lora', 'native90', 'calm')         | 0.918 | 0.884 | 0.897 |
| ('chronos_2_lora', 'native90', 'covid')        | 0.896 | 0.833 | 0.808 |
| ('chronos_2_lora', 'native90', 'ukraine')      | 0.909 | 0.87  | 0.809 |
| ('chronos_2_lora', 'splitCP80', 'ALL')         | 0.795 | 0.79  | 0.782 |
| ('chronos_2_lora', 'splitCP80', 'calm')        | 0.804 | 0.796 | 0.796 |
| ('chronos_2_lora', 'splitCP80', 'covid')       | 0.73  | 0.708 | 0.689 |
| ('chronos_2_lora', 'splitCP80', 'ukraine')     | 0.676 | 0.714 | 0.599 |
| ('chronos_2_lora', 'splitCP90', 'ALL')         | 0.898 | 0.886 | 0.882 |
| ('chronos_2_lora', 'splitCP90', 'calm')        | 0.9   | 0.892 | 0.889 |
| ('chronos_2_lora', 'splitCP90', 'covid')       | 0.866 | 0.841 | 0.818 |
| ('chronos_2_lora', 'splitCP90', 'ukraine')     | 0.821 | 0.821 | 0.748 |
| ('chronos_bolt_base', 'ACI80', 'ALL')          | 0.798 | 0.799 | 0.797 |
| ('chronos_bolt_base', 'ACI80', 'calm')         | 0.799 | 0.798 | 0.796 |
| ('chronos_bolt_base', 'ACI80', 'covid')        | 0.763 | 0.782 | 0.756 |
| ('chronos_bolt_base', 'ACI80', 'ukraine')      | 0.809 | 0.802 | 0.786 |
| ('chronos_bolt_base', 'ACI90', 'ALL')          | 0.899 | 0.9   | 0.896 |
| ('chronos_bolt_base', 'ACI90', 'calm')         | 0.899 | 0.9   | 0.901 |
| ('chronos_bolt_base', 'ACI90', 'covid')        | 0.881 | 0.874 | 0.87  |
| ('chronos_bolt_base', 'ACI90', 'ukraine')      | 0.916 | 0.901 | 0.905 |
| ('chronos_bolt_base', 'CQR80', 'ALL')          | 0.796 | 0.796 | 0.782 |
| ('chronos_bolt_base', 'CQR80', 'calm')         | 0.796 | 0.798 | 0.788 |
| ('chronos_bolt_base', 'CQR80', 'covid')        | 0.763 | 0.77  | 0.74  |
| ('chronos_bolt_base', 'CQR80', 'ukraine')      | 0.782 | 0.779 | 0.706 |
| ('chronos_bolt_base', 'SPCI80', 'ALL')         | 0.757 | 0.704 | 0.615 |
| ('chronos_bolt_base', 'SPCI80', 'calm')        | 0.766 | 0.71  | 0.619 |
| ('chronos_bolt_base', 'SPCI80', 'covid')       | 0.7   | 0.637 | 0.592 |
| ('chronos_bolt_base', 'SPCI80', 'ukraine')     | 0.691 | 0.645 | 0.558 |
| ('chronos_bolt_base', 'SPCI90', 'ALL')         | 0.856 | 0.802 | 0.706 |
| ('chronos_bolt_base', 'SPCI90', 'calm')        | 0.862 | 0.81  | 0.714 |
| ('chronos_bolt_base', 'SPCI90', 'covid')       | 0.792 | 0.76  | 0.637 |
| ('chronos_bolt_base', 'SPCI90', 'ukraine')     | 0.775 | 0.74  | 0.607 |
| ('chronos_bolt_base', 'native80', 'ALL')       | 0.829 | 0.787 | 0.736 |
| ('chronos_bolt_base', 'native80', 'calm')      | 0.833 | 0.792 | 0.746 |
| ('chronos_bolt_base', 'native80', 'covid')     | 0.792 | 0.737 | 0.663 |
| ('chronos_bolt_base', 'native80', 'ukraine')   | 0.79  | 0.729 | 0.661 |
| ('chronos_bolt_base', 'splitCP80', 'ALL')      | 0.798 | 0.791 | 0.782 |
| ('chronos_bolt_base', 'splitCP80', 'calm')     | 0.806 | 0.798 | 0.789 |
| ('chronos_bolt_base', 'splitCP80', 'covid')    | 0.722 | 0.719 | 0.622 |
| ('chronos_bolt_base', 'splitCP80', 'ukraine')  | 0.661 | 0.687 | 0.614 |
| ('chronos_bolt_base', 'splitCP90', 'ALL')      | 0.896 | 0.885 | 0.869 |
| ('chronos_bolt_base', 'splitCP90', 'calm')     | 0.904 | 0.892 | 0.878 |
| ('chronos_bolt_base', 'splitCP90', 'covid')    | 0.844 | 0.822 | 0.726 |
| ('chronos_bolt_base', 'splitCP90', 'ukraine')  | 0.817 | 0.824 | 0.767 |
| ('chronos_bolt_small', 'ACI80', 'ALL')         | 0.798 | 0.798 | 0.794 |
| ('chronos_bolt_small', 'ACI80', 'calm')        | 0.798 | 0.798 | 0.8   |
| ('chronos_bolt_small', 'ACI80', 'covid')       | 0.77  | 0.778 | 0.752 |
| ('chronos_bolt_small', 'ACI80', 'ukraine')     | 0.802 | 0.806 | 0.782 |
| ('chronos_bolt_small', 'ACI90', 'ALL')         | 0.899 | 0.899 | 0.895 |
| ('chronos_bolt_small', 'ACI90', 'calm')        | 0.899 | 0.9   | 0.897 |
| ('chronos_bolt_small', 'ACI90', 'covid')       | 0.889 | 0.878 | 0.84  |
| ('chronos_bolt_small', 'ACI90', 'ukraine')     | 0.901 | 0.893 | 0.882 |
| ('chronos_bolt_small', 'CQR80', 'ALL')         | 0.797 | 0.798 | 0.781 |
| ('chronos_bolt_small', 'CQR80', 'calm')        | 0.798 | 0.803 | 0.79  |
| ('chronos_bolt_small', 'CQR80', 'covid')       | 0.792 | 0.774 | 0.76  |
| ('chronos_bolt_small', 'CQR80', 'ukraine')     | 0.802 | 0.782 | 0.74  |
| ('chronos_bolt_small', 'SPCI80', 'ALL')        | 0.761 | 0.704 | 0.62  |
| ('chronos_bolt_small', 'SPCI80', 'calm')       | 0.768 | 0.707 | 0.624 |
| ('chronos_bolt_small', 'SPCI80', 'covid')      | 0.712 | 0.663 | 0.581 |
| ('chronos_bolt_small', 'SPCI80', 'ukraine')    | 0.702 | 0.676 | 0.542 |
| ('chronos_bolt_small', 'SPCI90', 'ALL')        | 0.86  | 0.802 | 0.701 |
| ('chronos_bolt_small', 'SPCI90', 'calm')       | 0.866 | 0.806 | 0.711 |
| ('chronos_bolt_small', 'SPCI90', 'covid')      | 0.8   | 0.756 | 0.615 |
| ('chronos_bolt_small', 'SPCI90', 'ukraine')    | 0.794 | 0.74  | 0.61  |
| ('chronos_bolt_small', 'native80', 'ALL')      | 0.817 | 0.764 | 0.754 |
| ('chronos_bolt_small', 'native80', 'calm')     | 0.822 | 0.77  | 0.768 |
| ('chronos_bolt_small', 'native80', 'covid')    | 0.8   | 0.715 | 0.685 |
| ('chronos_bolt_small', 'native80', 'ukraine')  | 0.79  | 0.756 | 0.66  |
| ('chronos_bolt_small', 'splitCP80', 'ALL')     | 0.793 | 0.788 | 0.785 |
| ('chronos_bolt_small', 'splitCP80', 'calm')    | 0.801 | 0.795 | 0.792 |
| ('chronos_bolt_small', 'splitCP80', 'covid')   | 0.718 | 0.7   | 0.596 |
| ('chronos_bolt_small', 'splitCP80', 'ukraine') | 0.68  | 0.687 | 0.642 |
| ('chronos_bolt_small', 'splitCP90', 'ALL')     | 0.895 | 0.885 | 0.874 |
| ('chronos_bolt_small', 'splitCP90', 'calm')    | 0.898 | 0.891 | 0.886 |
| ('chronos_bolt_small', 'splitCP90', 'covid')   | 0.833 | 0.818 | 0.774 |
| ('chronos_bolt_small', 'splitCP90', 'ukraine') | 0.847 | 0.813 | 0.74  |
| ('garch_t', 'ACI80', 'ALL')                    | 0.799 | 0.8   | 0.798 |
| ('garch_t', 'ACI80', 'calm')                   | 0.799 | 0.798 | 0.802 |
| ('garch_t', 'ACI80', 'covid')                  | 0.782 | 0.77  | 0.763 |
| ('garch_t', 'ACI80', 'ukraine')                | 0.806 | 0.798 | 0.752 |
| ('garch_t', 'ACI90', 'ALL')                    | 0.9   | 0.9   | 0.896 |
| ('garch_t', 'ACI90', 'calm')                   | 0.9   | 0.9   | 0.897 |
| ('garch_t', 'ACI90', 'covid')                  | 0.893 | 0.878 | 0.826 |
| ('garch_t', 'ACI90', 'ukraine')                | 0.908 | 0.889 | 0.901 |
| ('garch_t', 'CQR80', 'ALL')                    | 0.802 | 0.798 | 0.792 |
| ('garch_t', 'CQR80', 'calm')                   | 0.804 | 0.804 | 0.806 |
| ('garch_t', 'CQR80', 'covid')                  | 0.782 | 0.741 | 0.715 |
| ('garch_t', 'CQR80', 'ukraine')                | 0.771 | 0.752 | 0.664 |
| ('garch_t', 'CQR90', 'ALL')                    | 0.903 | 0.898 | 0.887 |
| ('garch_t', 'CQR90', 'calm')                   | 0.904 | 0.903 | 0.896 |
| ('garch_t', 'CQR90', 'covid')                  | 0.885 | 0.848 | 0.833 |
| ('garch_t', 'CQR90', 'ukraine')                | 0.886 | 0.858 | 0.748 |
| ('garch_t', 'SPCI80', 'ALL')                   | 0.758 | 0.71  | 0.623 |
| ('garch_t', 'SPCI80', 'calm')                  | 0.765 | 0.714 | 0.628 |
| ('garch_t', 'SPCI80', 'covid')                 | 0.692 | 0.674 | 0.611 |
| ('garch_t', 'SPCI80', 'ukraine')               | 0.698 | 0.645 | 0.55  |
| ('garch_t', 'SPCI90', 'ALL')                   | 0.856 | 0.809 | 0.706 |
| ('garch_t', 'SPCI90', 'calm')                  | 0.86  | 0.816 | 0.714 |
| ('garch_t', 'SPCI90', 'covid')                 | 0.815 | 0.756 | 0.645 |
| ('garch_t', 'SPCI90', 'ukraine')               | 0.802 | 0.744 | 0.614 |
| ('garch_t', 'native80', 'ALL')                 | 0.796 | 0.79  | 0.789 |
| ('garch_t', 'native80', 'calm')                | 0.8   | 0.796 | 0.804 |
| ('garch_t', 'native80', 'covid')               | 0.774 | 0.737 | 0.7   |
| ('garch_t', 'native80', 'ukraine')             | 0.748 | 0.732 | 0.664 |
| ('garch_t', 'native90', 'ALL')                 | 0.892 | 0.895 | 0.899 |
| ('garch_t', 'native90', 'calm')                | 0.894 | 0.899 | 0.907 |
| ('garch_t', 'native90', 'covid')               | 0.859 | 0.826 | 0.804 |
| ('garch_t', 'native90', 'ukraine')             | 0.855 | 0.851 | 0.802 |
| ('garch_t', 'splitCP80', 'ALL')                | 0.794 | 0.794 | 0.784 |
| ('garch_t', 'splitCP80', 'calm')               | 0.802 | 0.799 | 0.798 |
| ('garch_t', 'splitCP80', 'covid')              | 0.734 | 0.704 | 0.626 |
| ('garch_t', 'splitCP80', 'ukraine')            | 0.664 | 0.694 | 0.618 |
| ('garch_t', 'splitCP90', 'ALL')                | 0.896 | 0.889 | 0.878 |
| ('garch_t', 'splitCP90', 'calm')               | 0.899 | 0.894 | 0.884 |
| ('garch_t', 'splitCP90', 'covid')              | 0.848 | 0.826 | 0.734 |
| ('garch_t', 'splitCP90', 'ukraine')            | 0.836 | 0.817 | 0.736 |
| ('moirai2_small', 'ACI80', 'ALL')              | 0.799 | 0.8   | 0.795 |
| ('moirai2_small', 'ACI80', 'calm')             | 0.799 | 0.798 | 0.798 |
| ('moirai2_small', 'ACI80', 'covid')            | 0.778 | 0.766 | 0.778 |
| ('moirai2_small', 'ACI80', 'ukraine')          | 0.813 | 0.794 | 0.775 |
| ('moirai2_small', 'ACI90', 'ALL')              | 0.899 | 0.9   | 0.893 |
| ('moirai2_small', 'ACI90', 'calm')             | 0.9   | 0.901 | 0.898 |
| ('moirai2_small', 'ACI90', 'covid')            | 0.885 | 0.878 | 0.829 |
| ('moirai2_small', 'ACI90', 'ukraine')          | 0.905 | 0.893 | 0.882 |
| ('moirai2_small', 'CQR80', 'ALL')              | 0.804 | 0.802 | 0.784 |
| ('moirai2_small', 'CQR80', 'calm')             | 0.806 | 0.806 | 0.788 |
| ('moirai2_small', 'CQR80', 'covid')            | 0.792 | 0.756 | 0.73  |
| ('moirai2_small', 'CQR80', 'ukraine')          | 0.806 | 0.763 | 0.729 |
| ('moirai2_small', 'CQR90', 'ALL')              | 0.905 | 0.899 | 0.88  |
| ('moirai2_small', 'CQR90', 'calm')             | 0.905 | 0.901 | 0.886 |
| ('moirai2_small', 'CQR90', 'covid')            | 0.9   | 0.84  | 0.822 |
| ('moirai2_small', 'CQR90', 'ukraine')          | 0.886 | 0.87  | 0.851 |
| ('moirai2_small', 'SPCI80', 'ALL')             | 0.758 | 0.704 | 0.622 |
| ('moirai2_small', 'SPCI80', 'calm')            | 0.768 | 0.714 | 0.63  |
| ('moirai2_small', 'SPCI80', 'covid')           | 0.674 | 0.637 | 0.56  |
| ('moirai2_small', 'SPCI80', 'ukraine')         | 0.695 | 0.642 | 0.523 |
| ('moirai2_small', 'SPCI90', 'ALL')             | 0.858 | 0.806 | 0.718 |
| ('moirai2_small', 'SPCI90', 'calm')            | 0.863 | 0.815 | 0.72  |
| ('moirai2_small', 'SPCI90', 'covid')           | 0.785 | 0.722 | 0.626 |
| ('moirai2_small', 'SPCI90', 'ukraine')         | 0.802 | 0.722 | 0.595 |
| ('moirai2_small', 'native80', 'ALL')           | 0.806 | 0.782 | 0.763 |
| ('moirai2_small', 'native80', 'calm')          | 0.806 | 0.787 | 0.766 |
| ('moirai2_small', 'native80', 'covid')         | 0.782 | 0.722 | 0.622 |
| ('moirai2_small', 'native80', 'ukraine')       | 0.778 | 0.748 | 0.634 |
| ('moirai2_small', 'native90', 'ALL')           | 0.909 | 0.896 | 0.863 |
| ('moirai2_small', 'native90', 'calm')          | 0.912 | 0.903 | 0.872 |
| ('moirai2_small', 'native90', 'covid')         | 0.908 | 0.815 | 0.752 |
| ('moirai2_small', 'native90', 'ukraine')       | 0.89  | 0.866 | 0.794 |
| ('moirai2_small', 'splitCP80', 'ALL')          | 0.796 | 0.79  | 0.786 |
| ('moirai2_small', 'splitCP80', 'calm')         | 0.8   | 0.799 | 0.79  |
| ('moirai2_small', 'splitCP80', 'covid')        | 0.708 | 0.671 | 0.634 |
| ('moirai2_small', 'splitCP80', 'ukraine')      | 0.694 | 0.706 | 0.607 |
| ('moirai2_small', 'splitCP90', 'ALL')          | 0.894 | 0.89  | 0.876 |
| ('moirai2_small', 'splitCP90', 'calm')         | 0.897 | 0.895 | 0.889 |
| ('moirai2_small', 'splitCP90', 'covid')        | 0.848 | 0.796 | 0.734 |
| ('moirai2_small', 'splitCP90', 'ukraine')      | 0.835 | 0.809 | 0.718 |
| ('qr_ar', 'ACI80', 'ALL')                      | 0.798 | 0.8   | 0.798 |
| ('qr_ar', 'ACI80', 'calm')                     | 0.799 | 0.798 | 0.8   |
| ('qr_ar', 'ACI80', 'covid')                    | 0.77  | 0.77  | 0.76  |
| ('qr_ar', 'ACI80', 'ukraine')                  | 0.809 | 0.802 | 0.782 |
| ('qr_ar', 'ACI90', 'ALL')                      | 0.9   | 0.9   | 0.896 |
| ('qr_ar', 'ACI90', 'calm')                     | 0.9   | 0.901 | 0.897 |
| ('qr_ar', 'ACI90', 'covid')                    | 0.889 | 0.881 | 0.848 |
| ('qr_ar', 'ACI90', 'ukraine')                  | 0.908 | 0.893 | 0.897 |
| ('qr_ar', 'CQR80', 'ALL')                      | 0.802 | 0.797 | 0.784 |
| ('qr_ar', 'CQR80', 'calm')                     | 0.808 | 0.805 | 0.804 |
| ('qr_ar', 'CQR80', 'covid')                    | 0.674 | 0.66  | 0.611 |
| ('qr_ar', 'CQR80', 'ukraine')                  | 0.74  | 0.722 | 0.68  |
| ('qr_ar', 'CQR90', 'ALL')                      | 0.899 | 0.895 | 0.883 |
| ('qr_ar', 'CQR90', 'calm')                     | 0.905 | 0.899 | 0.894 |
| ('qr_ar', 'CQR90', 'covid')                    | 0.8   | 0.792 | 0.718 |
| ('qr_ar', 'CQR90', 'ukraine')                  | 0.882 | 0.839 | 0.775 |
| ('qr_ar', 'SPCI80', 'ALL')                     | 0.761 | 0.708 | 0.621 |
| ('qr_ar', 'SPCI80', 'calm')                    | 0.766 | 0.714 | 0.628 |
| ('qr_ar', 'SPCI80', 'covid')                   | 0.688 | 0.671 | 0.626 |
| ('qr_ar', 'SPCI80', 'ukraine')                 | 0.694 | 0.645 | 0.55  |
| ('qr_ar', 'SPCI90', 'ALL')                     | 0.856 | 0.804 | 0.704 |
| ('qr_ar', 'SPCI90', 'calm')                    | 0.861 | 0.81  | 0.709 |
| ('qr_ar', 'SPCI90', 'covid')                   | 0.8   | 0.76  | 0.663 |
| ('qr_ar', 'SPCI90', 'ukraine')                 | 0.778 | 0.733 | 0.603 |
| ('qr_ar', 'native80', 'ALL')                   | 0.781 | 0.774 | 0.78  |
| ('qr_ar', 'native80', 'calm')                  | 0.796 | 0.796 | 0.797 |
| ('qr_ar', 'native80', 'covid')                 | 0.585 | 0.608 | 0.589 |
| ('qr_ar', 'native80', 'ukraine')               | 0.63  | 0.622 | 0.607 |
| ('qr_ar', 'native90', 'ALL')                   | 0.882 | 0.884 | 0.888 |
| ('qr_ar', 'native90', 'calm')                  | 0.899 | 0.904 | 0.905 |
| ('qr_ar', 'native90', 'covid')                 | 0.782 | 0.726 | 0.67  |
| ('qr_ar', 'native90', 'ukraine')               | 0.779 | 0.774 | 0.729 |
| ('qr_ar', 'splitCP80', 'ALL')                  | 0.79  | 0.794 | 0.783 |
| ('qr_ar', 'splitCP80', 'calm')                 | 0.802 | 0.799 | 0.792 |
| ('qr_ar', 'splitCP80', 'covid')                | 0.733 | 0.689 | 0.622 |
| ('qr_ar', 'splitCP80', 'ukraine')              | 0.664 | 0.698 | 0.607 |
| ('qr_ar', 'splitCP90', 'ALL')                  | 0.896 | 0.891 | 0.876 |
| ('qr_ar', 'splitCP90', 'calm')                 | 0.9   | 0.895 | 0.886 |
| ('qr_ar', 'splitCP90', 'covid')                | 0.855 | 0.815 | 0.748 |
| ('qr_ar', 'splitCP90', 'ukraine')              | 0.832 | 0.816 | 0.729 |
| ('timesfm_25', 'ACI80', 'ALL')                 | 0.798 | 0.8   | 0.798 |
| ('timesfm_25', 'ACI80', 'calm')                | 0.798 | 0.799 | 0.801 |
| ('timesfm_25', 'ACI80', 'covid')               | 0.774 | 0.763 | 0.752 |
| ('timesfm_25', 'ACI80', 'ukraine')             | 0.809 | 0.794 | 0.74  |
| ('timesfm_25', 'ACI90', 'ALL')                 | 0.899 | 0.899 | 0.896 |
| ('timesfm_25', 'ACI90', 'calm')                | 0.899 | 0.9   | 0.901 |
| ('timesfm_25', 'ACI90', 'covid')               | 0.885 | 0.874 | 0.855 |
| ('timesfm_25', 'ACI90', 'ukraine')             | 0.916 | 0.901 | 0.882 |
| ('timesfm_25', 'CQR80', 'ALL')                 | 0.8   | 0.798 | 0.782 |
| ('timesfm_25', 'CQR80', 'calm')                | 0.8   | 0.798 | 0.789 |
| ('timesfm_25', 'CQR80', 'covid')               | 0.782 | 0.785 | 0.756 |
| ('timesfm_25', 'CQR80', 'ukraine')             | 0.82  | 0.809 | 0.706 |
| ('timesfm_25', 'SPCI80', 'ALL')                | 0.756 | 0.715 | 0.621 |
| ('timesfm_25', 'SPCI80', 'calm')               | 0.762 | 0.723 | 0.629 |
| ('timesfm_25', 'SPCI80', 'covid')              | 0.726 | 0.663 | 0.563 |
| ('timesfm_25', 'SPCI80', 'ukraine')            | 0.706 | 0.649 | 0.542 |
| ('timesfm_25', 'SPCI90', 'ALL')                | 0.857 | 0.808 | 0.71  |
| ('timesfm_25', 'SPCI90', 'calm')               | 0.862 | 0.815 | 0.715 |
| ('timesfm_25', 'SPCI90', 'covid')              | 0.814 | 0.752 | 0.692 |
| ('timesfm_25', 'SPCI90', 'ukraine')            | 0.79  | 0.76  | 0.622 |
| ('timesfm_25', 'native80', 'ALL')              | 0.879 | 0.812 | 0.796 |
| ('timesfm_25', 'native80', 'calm')             | 0.879 | 0.811 | 0.8   |
| ('timesfm_25', 'native80', 'covid')            | 0.874 | 0.792 | 0.686 |
| ('timesfm_25', 'native80', 'ukraine')          | 0.885 | 0.809 | 0.68  |
| ('timesfm_25', 'splitCP80', 'ALL')             | 0.794 | 0.79  | 0.783 |
| ('timesfm_25', 'splitCP80', 'calm')            | 0.801 | 0.796 | 0.792 |
| ('timesfm_25', 'splitCP80', 'covid')           | 0.74  | 0.711 | 0.611 |
| ('timesfm_25', 'splitCP80', 'ukraine')         | 0.656 | 0.694 | 0.576 |
| ('timesfm_25', 'splitCP90', 'ALL')             | 0.893 | 0.888 | 0.885 |
| ('timesfm_25', 'splitCP90', 'calm')            | 0.897 | 0.894 | 0.885 |
| ('timesfm_25', 'splitCP90', 'covid')           | 0.852 | 0.826 | 0.778 |
| ('timesfm_25', 'splitCP90', 'ukraine')         | 0.828 | 0.82  | 0.729 |

## CRPS by model (mean over series, per regime; lower = better)

|                            |   crps_ALL |   crps_calm |   crps_covid |   crps_ukraine |
|:---------------------------|-----------:|------------:|-------------:|---------------:|
| ('chronos_2', 1)           |      4.187 |       3.987 |        4.545 |          7.682 |
| ('chronos_2', 5)           |      9.111 |       8.62  |       10.524 |         17.165 |
| ('chronos_2', 22)          |     18.744 |      17.939 |       19.19  |         33.883 |
| ('chronos_2_full', 1)      |      4.31  |       4.115 |        4.62  |          7.787 |
| ('chronos_2_full', 5)      |      9.134 |       8.641 |       10.578 |         17.192 |
| ('chronos_2_full', 22)     |     18.505 |      17.65  |       19.329 |         34.23  |
| ('chronos_2_lora', 1)      |      4.174 |       3.974 |        4.52  |          7.68  |
| ('chronos_2_lora', 5)      |      9.088 |       8.591 |       10.494 |         17.264 |
| ('chronos_2_lora', 22)     |     18.638 |      17.819 |       19.073 |         34.054 |
| ('chronos_bolt_base', 1)   |      4.356 |       4.166 |        4.642 |          7.732 |
| ('chronos_bolt_base', 5)   |      9.278 |       8.792 |       10.638 |         17.291 |
| ('chronos_bolt_base', 22)  |     19.526 |      18.692 |       21.56  |         33.572 |
| ('chronos_bolt_small', 1)  |      4.349 |       4.147 |        4.774 |          7.821 |
| ('chronos_bolt_small', 5)  |      9.265 |       8.773 |       10.922 |         17.088 |
| ('chronos_bolt_small', 22) |     19.465 |      18.617 |       21.396 |         33.897 |
| ('garch_t', 1)             |      4.036 |       3.825 |        4.648 |          7.483 |
| ('garch_t', 5)             |      9.201 |       8.48  |       15.138 |         17.048 |
| ('garch_t', 22)            |     31.366 |      17.271 |      293.578 |         34.319 |
| ('moirai2_small', 1)       |      4.137 |       3.931 |        4.559 |          7.705 |
| ('moirai2_small', 5)       |      9.061 |       8.568 |       10.635 |         16.977 |
| ('moirai2_small', 22)      |     18.912 |      18.144 |       19.513 |         33.167 |
| ('qr_ar', 1)               |      4.09  |       3.877 |        4.561 |          7.72  |
| ('qr_ar', 5)               |      9.081 |       8.56  |       10.832 |         17.379 |
| ('qr_ar', 22)              |     18.406 |      17.472 |       21.002 |         33.827 |