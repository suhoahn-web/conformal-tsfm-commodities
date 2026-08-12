# Phase 2 Tests — MCS / GW / VaR (EMBARGOED: no Hormuz)

Generated 2026-08-11T18:25:04.061556+00:00 | missing caches: 0

## MCS survivors per series x h (10% level, squared loss)

| series       |   h | survivors                                                                                                                                           |   n_survivors | eliminated_first3                                   |
|:-------------|----:|:----------------------------------------------------------------------------------------------------------------------------------------------------|--------------:|:----------------------------------------------------|
| wti_fut      |   1 | no_change;lear_lite;garch_t;qr_ar;chronos_2_full;timesfm_25                                                                                         |             6 | chronos_bolt_base;ar5_returns;moirai2_small         |
| wti_fut      |   5 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                   |            11 | chronos_bolt_base                                   |
| wti_fut      |  22 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                   |            11 | chronos_bolt_base                                   |
| brent_fut    |   1 | no_change;ar5_returns;garch_t;qr_ar;chronos_2;chronos_2_lora                                                                                        |             6 | chronos_bolt_base;chronos_bolt_small;chronos_2_full |
| brent_fut    |   5 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_2;chronos_2_lora;timesfm_25                                                                   |             8 | chronos_bolt_small;chronos_bolt_base;moirai2_small  |
| brent_fut    |  22 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                   |            11 | chronos_bolt_base                                   |
| natgas_fut   |   1 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_2;chronos_2_lora;timesfm_25                                                                   |             8 | chronos_bolt_base;moirai2_small;chronos_bolt_small  |
| natgas_fut   |   5 | no_change;ar5_returns;garch_t;qr_ar;chronos_bolt_small;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                             |            10 | chronos_bolt_base;lear_lite                         |
| natgas_fut   |  22 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                   |            11 | chronos_bolt_base                                   |
| gold_fut     |   1 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;timesfm_25                              |            10 | chronos_2_full;moirai2_small                        |
| gold_fut     |   5 | ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small           |            11 | no_change                                           |
| gold_fut     |  22 | ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2_full;timesfm_25;moirai2_small                                    |             9 | chronos_2;no_change;chronos_2_lora                  |
| silver_fut   |   1 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small |            12 |                                                     |
| silver_fut   |   5 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small |            12 |                                                     |
| silver_fut   |  22 | no_change;ar5_returns;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small           |            11 | lear_lite                                           |
| copper_fut   |   1 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;timesfm_25                                                                                            |             6 | chronos_bolt_base;chronos_bolt_small;chronos_2_full |
| copper_fut   |   5 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25                                 |            10 | moirai2_small;chronos_bolt_base                     |
| copper_fut   |  22 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small |            12 |                                                     |
| platinum_fut |   1 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small |            12 |                                                     |
| platinum_fut |   5 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                    |            11 | chronos_bolt_small                                  |
| platinum_fut |  22 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                    |            11 | chronos_bolt_small                                  |
| corn_fut     |   1 | no_change;ar5_returns;lear_lite;garch_t;qr_ar                                                                                                       |             5 | chronos_bolt_small;chronos_bolt_base;chronos_2_full |
| corn_fut     |   5 | no_change;ar5_returns;lear_lite;garch_t;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small                                            |             9 | qr_ar;chronos_bolt_base;chronos_bolt_small          |
| corn_fut     |  22 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;timesfm_25                                                                                            |             6 | chronos_bolt_base;chronos_bolt_small;moirai2_small  |
| wheat_fut    |   1 | no_change;ar5_returns;garch_t;qr_ar;chronos_2;chronos_2_lora;timesfm_25                                                                             |             7 | chronos_bolt_base;moirai2_small;chronos_bolt_small  |
| wheat_fut    |   5 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small |            12 |                                                     |
| wheat_fut    |  22 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_bolt_small;chronos_bolt_base;chronos_2;chronos_2_lora;chronos_2_full;timesfm_25;moirai2_small |            12 |                                                     |
| soybean_fut  |   1 | no_change;ar5_returns;lear_lite;garch_t;qr_ar                                                                                                       |             5 | chronos_bolt_base;chronos_2_full;chronos_2_lora     |
| soybean_fut  |   5 | no_change;ar5_returns;lear_lite;garch_t;qr_ar;chronos_2;moirai2_small                                                                               |             7 | chronos_2_full;chronos_bolt_base;chronos_bolt_small |
| soybean_fut  |  22 | no_change;ar5_returns;lear_lite;qr_ar;moirai2_small                                                                                                 |             5 | chronos_bolt_small;chronos_bolt_base;chronos_2_full |

## MCS survivor frequency by model

| survivors          |   count |
|:-------------------|--------:|
| qr_ar              |   0.967 |
| garch_t            |   0.967 |
| ar5_returns        |   0.967 |
| no_change          |   0.933 |
| lear_lite          |   0.867 |
| timesfm_25         |   0.833 |
| chronos_2          |   0.767 |
| chronos_2_lora     |   0.733 |
| moirai2_small      |   0.633 |
| chronos_2_full     |   0.633 |
| chronos_bolt_small |   0.533 |
| chronos_bolt_base  |   0.4   |

## GW conditional-ability rejections vs no-change (p<0.10 share by model)

| model              |   rej |
|:-------------------|------:|
| ar5_returns        | 0.433 |
| chronos_2          | 0.467 |
| chronos_2_full     | 0.633 |
| chronos_2_lora     | 0.4   |
| chronos_bolt_base  | 0.8   |
| chronos_bolt_small | 0.7   |
| garch_t            | 0.6   |
| lear_lite          | 0.5   |
| moirai2_small      | 0.767 |
| qr_ar              | 0.367 |
| timesfm_25         | 0.467 |

## 95% VaR backtest — share of series passing Kupiec (p>0.05) by model x regime

|                               |   1 |   5 |   22 |
|:------------------------------|----:|----:|-----:|
| ('chronos_2', 'ALL')          | 0.6 | 0.5 |  0.4 |
| ('chronos_2', 'covid')        | 0.9 | 0.7 |  0.3 |
| ('chronos_2', 'ukraine')      | 0.9 | 0.7 |  0.6 |
| ('chronos_2_full', 'ALL')     | 0.1 | 0   |  0.2 |
| ('chronos_2_full', 'covid')   | 0.5 | 0.4 |  0.4 |
| ('chronos_2_full', 'ukraine') | 0.9 | 0.4 |  0.4 |
| ('chronos_2_lora', 'ALL')     | 0.8 | 0.3 |  0.4 |
| ('chronos_2_lora', 'covid')   | 0.9 | 0.6 |  0.3 |
| ('chronos_2_lora', 'ukraine') | 1   | 0.5 |  0.6 |
| ('garch_t', 'ALL')            | 0.7 | 0.6 |  0.2 |
| ('garch_t', 'covid')          | 0.8 | 0.5 |  0.2 |
| ('garch_t', 'ukraine')        | 0.6 | 0.5 |  0.3 |
| ('moirai2_small', 'ALL')      | 0.7 | 0.7 |  0.3 |
| ('moirai2_small', 'covid')    | 1   | 0.7 |  0.1 |
| ('moirai2_small', 'ukraine')  | 0.5 | 0.6 |  0.5 |
| ('qr_ar', 'ALL')              | 0.6 | 0.5 |  0.6 |
| ('qr_ar', 'covid')            | 0.5 | 0.5 |  0.2 |
| ('qr_ar', 'ukraine')          | 0.2 | 0.1 |  0.3 |