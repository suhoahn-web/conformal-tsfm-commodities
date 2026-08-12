# Conformalized time-series foundation models for commodity prices

Replication material for *"Conformalized time-series foundation models for commodity prices:
an econometric audit across crisis regimes"* (Suho Ahn, KAIST BTM).

This repository contains everything needed to check the paper's numbers without rerunning a
GPU: the cached forecasts of every model, the evaluation code, the statistical tests, the
leakage tests that enforce the information set, the frozen pre-registration, its deviation
log, and the pre-committed interpretation of the sealed holdout.

---

## What the paper finds

Five time-series foundation models (TSFMs) — Chronos-Bolt small and base, Chronos-2,
TimesFM 2.5 and Moirai-2 — are audited on ten daily commodity futures over 2015–2026 against
a classical panel, under a Model Confidence Set, with interval coverage evaluated inside
named crisis regimes.

**Point accuracy.** No foundation model beats the no-change benchmark on median at any
horizon; median MSPE ratios run from 1.02 (TimesFM 2.5) to 1.17 (Chronos-Bolt small). Under
a Model Confidence Set at the 10% level, every classical model survives more of the thirty
series–horizon cells (0.867–0.967) than every foundation model (0.400–0.833). Foundation
models are usually *in* the set — they are not usually excluded — but the ordering between
families is clean.

**Interval calibration.** Static split conformal prediction is worse than no calibration at
all in a crisis, falling to 0.599 coverage against a nominal 0.80 at the monthly horizon.
Adaptive conformal inference (ACI) is the best construction at every horizon and regime: it
holds nominal at h = 1 and h = 5, and at h = 22 removes about two-thirds of the crisis
shortfall (0.756–0.763 against 0.599–0.637 for split conformal) at a cost of roughly 25%
more width. It does not close the gap entirely, and the paper says so.

**Sealed holdout.** The 2026 Iran–Hormuz window was excluded from all development results by
a hard-coded embargo, its metric set frozen in advance, the interpretation of each possible
outcome written down before unsealing, and it was evaluated exactly once under a single-use
guard. The calibration ranking replicated there. The point-accuracy ordering held at h = 1
and h = 5 but not at h = 22, which is reported as a regime-dependent exception under the
pre-committed rule rather than as a reversal.

---

## Repository layout

```
preregistration/
  PREREGISTRATION.md          frozen plan (approved 2026-08-11; not edited after freezing)
  DEVIATION_LOG.md            every departure from it, dated, with reasons
  HOLDOUT_PRECOMMITMENT.md    how each possible holdout outcome would be read — written
                              before unsealing
data/
  DATA_SOURCES.md             which endpoints work, which are blocked, and how each was tested
  DATA_QUALITY_REPORT.md      per-series gaps, coverage and extreme-move counts
  raw/                        the daily price panel and its retrieval metadata
src/
  data_download/              panel construction (EIA + market-data endpoints)
  data_cleaning/              quality report generator
  eval_core/                  metrics, statistical tests, conformal constructions, leakage test
  server/                     GPU inference and fine-tuning scripts
  visualization/              figure generation and palette check
  manuscript/make_tables.py   result CSVs -> manuscript tables
analysis/
  smoke_a/, smoke_b/          end-to-end validation runs (not paper results)
  phase1_local/               point accuracy, interval coverage, CRPS  (embargoed window)
  phase2_local/               MCS, Giacomini-White, VaR backtests
  final_hormuz/               the single-use sealed-holdout evaluation and its audit trail
outputs/
  predictions/                361 cached forecast files — every model x series x horizon
  tables/                     the 14 manuscript tables as CSV
  figures/                    the 5 manuscript figures as PNG
docs/
  REFERENCES.md               the paper's reference list
```

## Reproducing the results

Nothing here requires a GPU. The cached predictions are the expensive part and they are
included.

```bash
pip install numpy pandas scipy scikit-learn statsmodels arch pyarrow matplotlib python-docx

python src/eval_core/test_no_leakage.py          # information-set test, 9 checks
python analysis/phase1_local/evaluate_phase1.py  # point accuracy, coverage, CRPS
python analysis/phase1_local/recompute_crps.py   # CRPS on the common quantile grid
python analysis/phase2_local/run_phase2_tests.py # MCS, Giacomini-White, VaR
python src/manuscript/make_tables.py             # regenerate the manuscript tables
python src/visualization/make_figures.py         # regenerate the figures
```

`analysis/final_hormuz/run_hormuz_final.py` is the sealed-holdout script. It refuses to run
without an approval file and refuses to run twice; both guards, and the marker showing it
ran once, are preserved here as the audit trail. Re-running it in a clone will not reproduce
the "evaluated once" property of the original run, which is a property of the history rather
than of the code.

## Regenerating the forecasts (GPU)

Only needed to reproduce `outputs/predictions/` from scratch. Model weights are **not**
redistributed here; these are the exact checkpoints evaluated:

| Model | Checkpoint |
|---|---|
| Chronos-Bolt small | `amazon/chronos-bolt-small` |
| Chronos-Bolt base | `amazon/chronos-bolt-base` |
| Chronos-2 | `amazon/chronos-2` |
| TimesFM 2.5 (200M) | `google/timesfm-2.5-200m-pytorch` |
| Moirai-2 small | `Salesforce/moirai-2.0-R-small` |

Inference used a single A100. Zero-shot inference over ~2,900 rolling origins took 1–2
seconds per series–horizon for Chronos-2 and Moirai-2 and 13–14 seconds for TimesFM 2.5;
each fine-tuning run took about 25 minutes. Fine-tuning used only observations on or before
2012-12-31, with 2013–2014 for validation.

## Three things worth knowing before you read the code

**The conformal wrappers are indexed by forecast origin, not by target date.** A forecast for
target *t* is issued at origin *t − h*, so only scores whose target falls on or before that
origin may enter the calibration set. Indexing by target date leaks future information at
h > 1 — the exact failure this paper criticises in others. `src/eval_core/conformal.py`
enforces the ordering and `src/eval_core/test_no_leakage.py` verifies it by perturbing the
series after a break date and asserting that intervals whose origins precede it are
bit-identical.

**The MCS uses the studentised elimination rule.** Hansen, Lunde and Nason define the range
statistic on *absolute* t-statistics but the elimination rule on *signed* ones
(`e_R,M = argmax_i sup_j t_ij`, their p. 466). Eliminating on mean loss instead — or on
absolute t-statistics — removes the wrong model. `src/eval_core/metrics.py` implements the
published rule.

**CRPS is computed on the grid every model can express, {0.10, 0.50, 0.90}.** Chronos-Bolt
clamps its quantile head to [0.1, 0.9] and TimesFM 2.5 emits deciles, so a quantile-based
CRPS on each model's own grid measures grid geometry rather than distributional quality. Any
study ranking foundation models on CRPS should state which quantiles its models actually
emit.

## Known limitations, stated here as well as in the paper

- The information set is univariate and price-only. A richer specification would likely help
  whichever family can exploit it.
- Regimes are fixed by calendar rather than estimated, which is conservative for inference
  but crude as description.
- The sequential conformal construction is a simplified variant, not a faithful
  implementation of the published method it approximates; its underperformance here is not
  evidence against that method.
- The directional-accuracy test is the Pesaran–Timmermann (1992) statistic, which assumes
  independent observations; our origins overlap at h = 5 and h = 22, so it is
  anti-conservative there. The directional results are at chance level regardless.
- The foundation models are frozen at their 2026 releases. This is a measurement at a point
  in time, which is why the predictions and code are released.

## What is deliberately not in this repository

- **Third-party PDFs.** The reference list is in `docs/REFERENCES.md`; the papers themselves
  are the publishers' to distribute.
- **Model weights.** 1.4 GB of third-party checkpoints; the identifiers above are what
  reproduces.
- **Manuscript drafts and internal reviews.** Not part of the scientific claim.

## Citation

See `CITATION.cff`. Please cite the paper rather than the repository alone.

## License

Code is released under the MIT License. Result files, tables and figures are released under
CC BY 4.0. The raw price data is redistributed under the terms of its original public
sources, which are documented per series in `data/DATA_SOURCES.md`.
