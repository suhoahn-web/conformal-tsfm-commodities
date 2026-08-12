# E2 — value-at-risk backtests on non-overlapping origins

Generated 2026-08-12T16:50:40.619960+00:00 | 95% VaR from the 5% predictive quantile | embargoed sample only

The non-overlapping sample keeps every h-th origin, so retained forecasts share no target period. Exceedance rates are reported first; the Kupiec p-value is secondary because failing to reject is not evidence of validity.

## h = 1

| model | sample | median n | median exceedance rate | median Kupiec p | share rejecting at 5% |
|---|---|---|---|---|---|
| garch_t | overlapping | 2804 | 0.0551 | 0.155 | 0.3 |
| garch_t | non_overlapping | 2804 | 0.0551 | 0.155 | 0.3 |
| qr_ar | overlapping | 2804 | 0.0556 | 0.124 | 0.4 |
| qr_ar | non_overlapping | 2804 | 0.0556 | 0.124 | 0.4 |
| chronos_2 | overlapping | 2804 | 0.0435 | 0.113 | 0.4 |
| chronos_2 | non_overlapping | 2804 | 0.0435 | 0.113 | 0.4 |
| chronos_2_lora | overlapping | 2804 | 0.0494 | 0.211 | 0.2 |
| chronos_2_lora | non_overlapping | 2804 | 0.0494 | 0.211 | 0.2 |
| chronos_2_full | overlapping | 2804 | 0.0904 | 0.000 | 0.9 |
| chronos_2_full | non_overlapping | 2804 | 0.0904 | 0.000 | 0.9 |
| moirai2_small | overlapping | 2804 | 0.0474 | 0.343 | 0.3 |
| moirai2_small | non_overlapping | 2804 | 0.0474 | 0.343 | 0.3 |

## h = 5

| model | sample | median n | median exceedance rate | median Kupiec p | share rejecting at 5% |
|---|---|---|---|---|---|
| garch_t | overlapping | 2804 | 0.0518 | 0.132 | 0.4 |
| garch_t | non_overlapping | 561 | 0.0498 | 0.255 | 0.0 |
| qr_ar | overlapping | 2804 | 0.0563 | 0.040 | 0.5 |
| qr_ar | non_overlapping | 561 | 0.0499 | 0.517 | 0.1 |
| chronos_2 | overlapping | 2804 | 0.0569 | 0.125 | 0.5 |
| chronos_2 | non_overlapping | 561 | 0.0571 | 0.332 | 0.0 |
| chronos_2_lora | overlapping | 2804 | 0.0614 | 0.008 | 0.7 |
| chronos_2_lora | non_overlapping | 561 | 0.0632 | 0.182 | 0.1 |
| chronos_2_full | overlapping | 2804 | 0.0965 | 0.000 | 1.0 |
| chronos_2_full | non_overlapping | 561 | 0.0963 | 0.000 | 0.8 |
| moirai2_small | overlapping | 2804 | 0.0478 | 0.142 | 0.3 |
| moirai2_small | non_overlapping | 561 | 0.0464 | 0.332 | 0.0 |

## h = 22

| model | sample | median n | median exceedance rate | median Kupiec p | share rejecting at 5% |
|---|---|---|---|---|---|
| garch_t | overlapping | 2804 | 0.0471 | 0.006 | 0.8 |
| garch_t | non_overlapping | 128 | 0.0547 | 0.247 | 0.2 |
| qr_ar | overlapping | 2804 | 0.0535 | 0.084 | 0.4 |
| qr_ar | non_overlapping | 128 | 0.0664 | 0.425 | 0.1 |
| chronos_2 | overlapping | 2804 | 0.0512 | 0.038 | 0.6 |
| chronos_2 | non_overlapping | 128 | 0.0586 | 0.319 | 0.0 |
| chronos_2_lora | overlapping | 2804 | 0.0519 | 0.035 | 0.6 |
| chronos_2_lora | non_overlapping | 128 | 0.0586 | 0.319 | 0.0 |
| chronos_2_full | overlapping | 2804 | 0.0877 | 0.000 | 0.8 |
| chronos_2_full | non_overlapping | 128 | 0.0938 | 0.042 | 0.6 |
| moirai2_small | overlapping | 2804 | 0.0601 | 0.000 | 0.7 |
| moirai2_small | non_overlapping | 128 | 0.0547 | 0.308 | 0.1 |

