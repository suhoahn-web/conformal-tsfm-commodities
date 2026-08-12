# FINAL Hormuz Window Results (2026-02-28 .. 2026-07-31) — single pass

Generated 2026-08-11T20:19:40.040551+00:00 | missing: 0

## Point: median MSPE ratio vs no-change

| model              |      1 |      5 |     22 |
|:-------------------|-------:|-------:|-------:|
| ar5_returns        | 1.0054 | 1.0014 | 1.0004 |
| chronos_2          | 1.1018 | 1.0638 | 1.0634 |
| chronos_2_full     | 1.1608 | 1.0515 | 1.0085 |
| chronos_2_lora     | 1.1019 | 1.0814 | 1.0812 |
| chronos_bolt_base  | 1.1374 | 1.1299 | 1.1092 |
| chronos_bolt_small | 1.1716 | 1.1365 | 1.2189 |
| garch_t            | 1.0022 | 1.0074 | 1.0448 |
| lear_lite          | 1.025  | 1.038  | 1.031  |
| moirai2_small      | 1.094  | 1.0466 | 0.9777 |
| qr_ar              | 1.0141 | 1.0209 | 1.0332 |
| timesfm_25         | 1.0268 | 1.0278 | 0.9542 |

## Intervals: median PICP by band (nominal 0.80/0.90)

|                                     |     1 |     5 |    22 |
|:------------------------------------|------:|------:|------:|
| ('chronos_2', 'ACI80')              | 0.807 | 0.778 | 0.826 |
| ('chronos_2', 'ACI90')              | 0.911 | 0.878 | 0.944 |
| ('chronos_2', 'CQR80')              | 0.788 | 0.802 | 0.722 |
| ('chronos_2', 'SPCI80')             | 0.67  | 0.717 | 0.552 |
| ('chronos_2', 'SPCI90')             | 0.825 | 0.774 | 0.599 |
| ('chronos_2', 'native80')           | 0.802 | 0.806 | 0.674 |
| ('chronos_2', 'splitCP80')          | 0.726 | 0.722 | 0.67  |
| ('chronos_2', 'splitCP90')          | 0.882 | 0.849 | 0.802 |
| ('chronos_2_full', 'ACI80')         | 0.798 | 0.778 | 0.82  |
| ('chronos_2_full', 'ACI90')         | 0.897 | 0.877 | 0.916 |
| ('chronos_2_full', 'CQR80')         | 0.745 | 0.774 | 0.726 |
| ('chronos_2_full', 'SPCI80')        | 0.665 | 0.702 | 0.599 |
| ('chronos_2_full', 'SPCI90')        | 0.812 | 0.778 | 0.661 |
| ('chronos_2_full', 'native80')      | 0.712 | 0.769 | 0.661 |
| ('chronos_2_full', 'splitCP80')     | 0.722 | 0.703 | 0.698 |
| ('chronos_2_full', 'splitCP90')     | 0.877 | 0.853 | 0.811 |
| ('chronos_2_lora', 'ACI80')         | 0.797 | 0.778 | 0.83  |
| ('chronos_2_lora', 'ACI90')         | 0.906 | 0.872 | 0.944 |
| ('chronos_2_lora', 'CQR80')         | 0.797 | 0.792 | 0.708 |
| ('chronos_2_lora', 'SPCI80')        | 0.689 | 0.698 | 0.552 |
| ('chronos_2_lora', 'SPCI90')        | 0.812 | 0.764 | 0.618 |
| ('chronos_2_lora', 'native80')      | 0.792 | 0.788 | 0.665 |
| ('chronos_2_lora', 'splitCP80')     | 0.722 | 0.712 | 0.665 |
| ('chronos_2_lora', 'splitCP90')     | 0.867 | 0.844 | 0.802 |
| ('chronos_bolt_base', 'ACI80')      | 0.806 | 0.769 | 0.83  |
| ('chronos_bolt_base', 'ACI90')      | 0.911 | 0.872 | 0.948 |
| ('chronos_bolt_base', 'CQR80')      | 0.783 | 0.769 | 0.792 |
| ('chronos_bolt_base', 'SPCI80')     | 0.694 | 0.666 | 0.628 |
| ('chronos_bolt_base', 'SPCI90')     | 0.802 | 0.76  | 0.698 |
| ('chronos_bolt_base', 'native80')   | 0.783 | 0.774 | 0.665 |
| ('chronos_bolt_base', 'splitCP80')  | 0.736 | 0.698 | 0.769 |
| ('chronos_bolt_base', 'splitCP90')  | 0.867 | 0.849 | 0.892 |
| ('chronos_bolt_small', 'ACI80')     | 0.802 | 0.802 | 0.878 |
| ('chronos_bolt_small', 'ACI90')     | 0.901 | 0.882 | 0.972 |
| ('chronos_bolt_small', 'CQR80')     | 0.792 | 0.806 | 0.811 |
| ('chronos_bolt_small', 'SPCI80')    | 0.717 | 0.67  | 0.633 |
| ('chronos_bolt_small', 'SPCI90')    | 0.83  | 0.722 | 0.674 |
| ('chronos_bolt_small', 'native80')  | 0.826 | 0.792 | 0.684 |
| ('chronos_bolt_small', 'splitCP80') | 0.717 | 0.708 | 0.698 |
| ('chronos_bolt_small', 'splitCP90') | 0.854 | 0.835 | 0.872 |
| ('garch_t', 'ACI80')                | 0.797 | 0.783 | 0.769 |
| ('garch_t', 'ACI90')                | 0.906 | 0.878 | 0.953 |
| ('garch_t', 'CQR80')                | 0.774 | 0.783 | 0.75  |
| ('garch_t', 'SPCI80')               | 0.722 | 0.698 | 0.618 |
| ('garch_t', 'SPCI90')               | 0.821 | 0.769 | 0.656 |
| ('garch_t', 'native80')             | 0.769 | 0.778 | 0.74  |
| ('garch_t', 'splitCP80')            | 0.736 | 0.694 | 0.651 |
| ('garch_t', 'splitCP90')            | 0.853 | 0.84  | 0.821 |
| ('moirai2_small', 'ACI80')          | 0.802 | 0.778 | 0.806 |
| ('moirai2_small', 'ACI90')          | 0.906 | 0.882 | 0.976 |
| ('moirai2_small', 'CQR80')          | 0.783 | 0.802 | 0.867 |
| ('moirai2_small', 'SPCI80')         | 0.736 | 0.703 | 0.556 |
| ('moirai2_small', 'SPCI90')         | 0.802 | 0.764 | 0.618 |
| ('moirai2_small', 'native80')       | 0.788 | 0.806 | 0.754 |
| ('moirai2_small', 'splitCP80')      | 0.703 | 0.698 | 0.679 |
| ('moirai2_small', 'splitCP90')      | 0.887 | 0.849 | 0.878 |
| ('qr_ar', 'ACI80')                  | 0.792 | 0.788 | 0.806 |
| ('qr_ar', 'ACI90')                  | 0.906 | 0.872 | 0.962 |
| ('qr_ar', 'CQR80')                  | 0.769 | 0.76  | 0.651 |
| ('qr_ar', 'SPCI80')                 | 0.712 | 0.708 | 0.584 |
| ('qr_ar', 'SPCI90')                 | 0.825 | 0.769 | 0.665 |
| ('qr_ar', 'native80')               | 0.698 | 0.698 | 0.694 |
| ('qr_ar', 'splitCP80')              | 0.74  | 0.698 | 0.646 |
| ('qr_ar', 'splitCP90')              | 0.849 | 0.849 | 0.82  |
| ('timesfm_25', 'ACI80')             | 0.816 | 0.788 | 0.844 |
| ('timesfm_25', 'ACI90')             | 0.906 | 0.882 | 0.944 |
| ('timesfm_25', 'CQR80')             | 0.783 | 0.792 | 0.774 |
| ('timesfm_25', 'SPCI80')            | 0.703 | 0.722 | 0.556 |
| ('timesfm_25', 'SPCI90')            | 0.825 | 0.783 | 0.613 |
| ('timesfm_25', 'native80')          | 0.872 | 0.825 | 0.75  |
| ('timesfm_25', 'splitCP80')         | 0.75  | 0.75  | 0.689 |
| ('timesfm_25', 'splitCP90')         | 0.849 | 0.853 | 0.863 |

## 95% VaR: Kupiec pass share by model

| model          |   1 |   5 |   22 |
|:---------------|----:|----:|-----:|
| chronos_2      | 0.9 | 0.9 |  0.4 |
| chronos_2_full | 1   | 1   |  0.4 |
| chronos_2_lora | 0.9 | 1   |  0.4 |
| garch_t        | 0.7 | 0.7 |  0.2 |
| moirai2_small  | 0.9 | 0.8 |  0.2 |
| qr_ar          | 0.4 | 0.3 |  0.1 |