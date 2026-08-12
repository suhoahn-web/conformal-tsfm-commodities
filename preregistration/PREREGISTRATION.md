# Research Plan v1 — Conformalized TSFM Evaluation on Commodity Prices

Status: **FROZEN — approved by user 2026-08-11.** The "Pre-registered choices" section may no longer be edited; any deviation must be logged in the Deviation Log with date and reason. The Hormuz window (2026-02-28..2026-07-31) is under evaluation embargo until the final pre-registered pass.
Created: 2026-08-11. Basis: `IDEATION_REPORT_2026-08.md` (idea #1, narrowed claims per §3a).

## 1. Headline claim (frozen wording; refined 2026-08-11 after close reading of all prior art)

> The first **conformalized (ACI/SPCI/EnbPI/CQR)**, **econometrically audited** evaluation of time-series foundation models on **daily energy and metals prices** across **crisis regimes** (COVID 2020, Russia–Ukraine 2022, Iran–Hormuz 2026).

Every qualifier is load-bearing against a specific prior work (see `litereature review/notes/`):
- *conformalized beyond split-CP*: Achour et al. 2025 ran split-conformal only, on TSFMs, no commodities, no tests
- *econometrically audited*: FinVerse 2026 evaluates 43 TSFMs incl. some commodity series but zero UQ, no tests, admits leakage
- *daily …prices*: Ma et al. 2026 covers Chinese commodity futures but 5-min realized volatility, 1 year, no TSFMs
- *crisis regimes*: Wang & Zhang 2026 (agri, monthly, zero-shot, point-only) **excluded** COVID rather than stratifying; probabilistic eval is their self-declared future work
- FedChronos 2026 = federated/DP on Indian vegetable mandis; its naive-LoRA-underperforms-zero-shot result motivates our careful FT protocol (cite as motivation, not competition)

Forbidden claims: "first TSFM on commodities" (agri taken), "first TSFM+conformal" (methods combo taken). Agricultural series are robustness, not headline.

## 2. Research questions

- RQ1: Do zero-shot TSFMs beat the no-change and futures-based benchmarks on energy/metals prices under the oil-econometrics protocol (MSPE ratios, success ratios, DM/CW, MCS)?
- RQ2: Does LoRA/full fine-tuning on commodity history change the answer? (A100)
- RQ3: Are TSFM native prediction intervals calibrated (CRPS, PICP, Winkler) — and does calibration survive crisis regimes?
- RQ4: Does conformal calibration (ACI, SPCI, EnbPI, CQR wrappers) repair crisis-regime miscoverage, and at what sharpness cost?
- RQ5 (economic value): Does any calibration advantage translate into utility in a simple risk-management exercise (VaR backtest or hedging utility)?

## 3. Pre-registered choices (FROZEN upon approval)

### 3.1 Data (all free; log retrieval date+URL; never edit raw)
- Headline panel (daily FUTURES, per data-quality decision 2026-08-11): WTI (CL), Brent (BZ, 2007–), natural gas (NG), gold (GC), silver (SI), copper (HG). [6 series]
- Robustness panel: corn, wheat, soybeans, platinum (post-2005); EIA spot series (WTI/Brent/HH/heating oil/RBOB) as measurement cross-check.
- Data collected 2026-08-11: 16/16 sources OK (`data/raw/prices/`, quality report `data/DATA_QUALITY_REPORT.md`; Hormuz-window coverage 106/110 business days on all series).
- Sources: Stooq / FRED / EIA primary; yfinance only as cross-check. Discrepancy >0.5% between sources on any day → flag in data-quality report.
- Sample: 2000-01 (or earliest available) to 2026-07. 
- Exogenous (for baselines only, not TSFM inputs in v1): none in headline (univariate evaluation keeps the comparison clean); futures curve for the futures-based benchmark.

### 3.2 Evaluation protocol (AKV 2013 + Lago 2021 compliant; see protocol notes)
- Horizons: h = 1, 5, 22 trading days.
- Scheme: **recursive (expanding) origin** per AKV convention, recalibrate monthly; OOS evaluation 2015-01 – 2026-07. (Changed from rolling per AKV protocol note, 2026-08-11.)
- Two price tracks where deflators are defensible at daily frequency: nominal (headline) + log-real robustness at monthly aggregation.
- Overfitting audit (AKV): recursive MSPE-ratio paths over the OOS period + crisis-excluded subsample re-evaluation (one extreme episode must not carry a model's "success").
- Point metrics: MSPE ratio vs no-change (+ benchmark MSPE level); **rMAE** (Lago — MAPE banned, MASE avoided in recalibration settings); directional success ratio with **Pesaran–Timmermann** test; DM (one-sided) and **Giacomini–White**; Clark-West only where nested-direct applies (with AKV's caveat on marginal rejections); MCS (10%).
- Regime segmentation of the OOS window (event dates fixed here):
  - COVID shock: 2020-02-20 – 2020-08-31
  - Ukraine shock: 2022-02-24 – 2022-08-31
  - **Hormuz shock: 2026-02-28 – 2026-07-31 (SACRED HOLDOUT — no tuning decision may touch it, in code or in analysis order)**
  - Calm: all remaining OOS days.
- Point metrics: MSPE ratio vs no-change; directional success ratio; DM (rolling, HLN small-sample correction) and Clark-West where nested; MCS (10% level).
- Probabilistic metrics: CRPS; PICP + Winkler at 80%/95%; pinball loss at {0.05,…,0.95}; coverage reported per regime.
- Economic value: 95% VaR backtest (Kupiec + Christoffersen) per regime.

### 3.3 Models
- TSFMs (zero-shot): Chronos-2, TimesFM 2.5, Moirai-2, Time-MoE, TTM. (TimeGPT via API only if license permits academic use — decide before running, else drop.)
- Fine-tuned: LoRA on Chronos-2 + full fine-tune of TTM (smallest) on pre-2015 commodity panel; NO tuning on post-2015 data beyond the rolling window's train split.
- Baselines: no-change; futures-based (oil); AR(p) by AIC; LEAR (Lago spec: asinh/MAD transform, LARS-AIC lambda, multi-window ensemble — adapted from hourly to daily); GARCH(1,1)-t intervals; DeepAR; quantile regression (linear); **simplified QBVAR-spirit penalized quantile regression with Bjornland-style uncertainty/financial predictors** (their paper reports pinball only, no coverage — a gap we cite and fill).
- Conformal wrappers: split-conformal, EnbPI, ACI, SPCI, CQR — applied uniformly to every model that emits intervals or quantiles.
- Hyperparameters: defaults from source papers wherever they exist; anything tuned uses only pre-2015 data; all settings recorded in `configs/` before the full run.

### 3.4 Leakage controls
- Leakage unit tests in code (no future timestamps in any feature/window; conformal calibration sets strictly precede test points).
- TSFM pretraining-contamination discussion: document each model's pretraining cutoff vs our OOS window; flag models whose pretraining data may include our test period (this is a known critique — we address it head-on in a dedicated subsection).
- Decomposition methods deliberately excluded (leakage-tainted literature — cited as motivation).

### 3.5 Infrastructure
- Local (Windows): data pipeline, baselines, conformal wrappers, evaluation.
- the GPU server A100 server: TSFM inference + fine-tuning in a NEW conda env `commodity` (never touch `solar` env or its folders; respect GPU-sharing rules — queue behind running jobs).
- Immutable prediction cache: every model run writes `outputs/predictions/{model}_{series}_{horizon}_{date}.parquet` + metadata JSON; never overwritten.

## 4. Execution order

1. [USER] Approve this plan; provide PDFs from `litereature review/DOWNLOAD_LIST_v1.md`; confirm the GPU server access for this project.
2. Data pipeline + data-quality report (local).
3. Smoke test A (local, CPU): no-change + AR + split-conformal on 3 series, tiny window — validates evaluation code end-to-end.
4. Smoke test B (A100): zero-shot Chronos-2 on the same 3 series, same window — validates model harness.
5. Full baseline runs → full zero-shot TSFM runs → fine-tuning runs.
6. Analysis strictly in order: calm+COVID+Ukraine first; Hormuz window LAST, once, after all code frozen.
7. Results-integrity report → manuscript (structure-reference paper method, per user profile).

## 4a. Reproducibility commitments (Lago 2021 practice)

- Publish: data loaders, model code, hyperparameter logs, and the raw forecasts as CSV (enables others to test against us — also a review-stage credibility asset).
- Report per-recalibration compute time for every model (TSFM inference cost vs LEAR seconds is itself a finding).

The deviation log is a separate file: `DEVIATION_LOG.md`.
