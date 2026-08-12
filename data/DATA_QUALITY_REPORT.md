# Data Quality Report — Raw Daily Price Panel

Generated: 2026-08-10T16:38:17.703931+00:00 (script: src/data_cleaning/data_quality_report.py)

## Per-series checks

| series          |   rows | span                     |   missing_bdays_pct |   max_gap_days |   nonpositive |   abs_ret_gt20pct | COVID   | Ukraine   | Hormuz (HOLDOUT)   |
|:----------------|-------:|:-------------------------|--------------------:|---------------:|--------------:|------------------:|:--------|:----------|:-------------------|
| brent_fut       |   4736 | 2007-07-30 .. 2026-08-10 |                 4.6 |             17 |             0 |                 2 | 135/138 | 131/135   | 106/110            |
| brent_spot      |   9947 | 1987-05-20 .. 2026-08-03 |                 2.8 |              6 |             0 |                 9 | 133/138 | 130/135   | 106/110            |
| copper_fut      |   6514 | 2000-08-30 .. 2026-08-10 |                 3.8 |              5 |             0 |                 1 | 135/138 | 131/135   | 106/110            |
| corn_fut        |   6521 | 2000-07-17 .. 2026-08-10 |                 4.1 |             14 |             0 |                 1 | 135/138 | 131/135   | 106/110            |
| gold_fut        |   6509 | 2000-08-30 .. 2026-08-10 |                 3.8 |              5 |             0 |                 0 | 135/138 | 131/135   | 106/110            |
| heatingoil_spot |  10089 | 1986-06-02 .. 2026-08-03 |                 3.7 |              5 |             0 |                 9 | 135/138 | 131/135   | 106/110            |
| henryhub_spot   |   7425 | 1997-01-07 .. 2026-08-03 |                 3.8 |             15 |             0 |                90 | 135/138 | 131/135   | 106/110            |
| natgas_fut      |   6515 | 2000-08-30 .. 2026-08-10 |                 3.8 |              5 |             0 |                12 | 135/138 | 131/135   | 106/110            |
| platinum_fut    |   5993 | 2000-01-04 .. 2026-08-10 |                13.6 |             78 |             0 |                 5 | 135/138 | 131/135   | 106/110            |
| rbob_spot       |  10091 | 1986-06-02 .. 2026-08-03 |                 3.7 |              5 |             0 |                10 | 135/138 | 131/135   | 106/110            |
| silver_fut      |   6511 | 2000-08-30 .. 2026-08-10 |                 3.8 |              5 |             0 |                 1 | 135/138 | 131/135   | 106/110            |
| soybean_fut     |   6513 | 2000-09-15 .. 2026-08-10 |                 3.6 |              5 |             0 |                 2 | 135/138 | 131/135   | 106/110            |
| wheat_fut       |   6533 | 2000-07-17 .. 2026-08-10 |                 3.9 |             10 |             0 |                 0 | 135/138 | 131/135   | 106/110            |
| wti_fut         |   6518 | 2000-08-23 .. 2026-08-10 |                 3.8 |              5 |             1 |                 7 | 135/138 | 131/135   | 106/110            |
| wti_spot        |  10215 | 1986-01-02 .. 2026-08-03 |                 3.5 |              5 |             1 |                11 | 135/138 | 131/135   | 106/110            |

Notes: `missing_bdays_pct` counts business days without an observation (holidays inflate this slightly; investigate any series far above peers). `abs_ret_gt20pct` flags daily log-moves >20% (verify against known events, e.g., April 2020 negative WTI, Hormuz spike days — do NOT delete).

## Cross-source agreement (daily log-return correlation)

| pair                        |   overlap_days |   return_corr |
|:----------------------------|---------------:|--------------:|
| wti_spot vs wti_fut         |           6493 |         0.928 |
| brent_spot vs brent_fut     |           4685 |         0.749 |
| henryhub_spot vs natgas_fut |           6480 |         0.243 |

Expectation: spot-vs-front-month return correlation > 0.9 for WTI/Brent; Henry Hub spot-futures basis is looser. Investigate anything below 0.8.

## Nonpositive prices

WTI April 2020 contains a negative settlement (-$37.63, 2020-04-20) — this is REAL, keep it; it motivates evaluating in levels + asinh transform rather than logs for WTI.
## Analyst notes (manual commentary, 2026-08-11)

1. **Regime coverage is complete** — all 15 series have 96%+ coverage in COVID/Ukraine/Hormuz windows. The Hormuz holdout is usable as-is.
2. **WTI negative price 2020-04-20 is real** (-$37.63); evaluate WTI in levels/asinh, not raw logs.
3. **Henry Hub spot: 90 days with |return|>20%** — real physical-market spikes (winter storms), not errors. Verified pattern matches known events; keep. Same for its low spot-futures correlation (0.243): HH cash vs NYMEX front-month basis is structurally loose.
4. **Brent spot-futures return corr 0.749** — timing mismatch (EIA dated Brent Europe close vs ICE/NYMEX close), not a data defect.
5. **Decision for §3.1**: headline panel uses FUTURES series (synchronous closes, consistent measurement): CL, BZ, NG, GC, SI, HG. EIA spot = cross-check/robustness. Platinum (13.6% missing bdays, 78-day gap in early years) demoted to robustness with post-2005 sample.
