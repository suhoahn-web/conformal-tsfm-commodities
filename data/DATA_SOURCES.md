# Commodity Price Forecasting — Free Data Source Inventory

## ⚡ Access verification (tested 2026-08-11, this machine)

| Source | Status | Note |
|---|---|---|
| EIA hist_xls (WTI/Brent/HH daily spot) | ✅ WORKS | 1986–2026-08-03 confirmed, direct xls |
| Yahoo v8 chart API (futures daily) | ✅ WORKS | must chunk by ~1-year period1/period2 windows; `range=max` silently degrades to monthly |
| World Bank Pink Sheet monthly | ✅ WORKS | 781 monthly rows |
| FRED `fredgraph.csv` | ❌ BLOCKED (bot protection) | use official FRED API with free key instead |
| Stooq CSV | ❌ BLOCKED (JS challenge) | drop |
| Smoke-test script | `src/data_download/fetch_smoke_test.py` | outputs + metadata in `data/raw/smoke_test/` |

Compiled 2026-08-10. All sources below are free. Verify exact series IDs and coverage at download time; log retrieval date + URL per the project's coding standards.

## 1. Commodity prices (targets)

| Source | Coverage | Frequency | Access |
|---|---|---|---|
| **World Bank Pink Sheet (Commodity Price Data)** | ~70 commodities (energy, metals, agri, fertilizers), 1960– | Monthly | Direct xlsx download, no key |
| **FRED (St. Louis Fed)** | WTI, Brent, natural gas (HH), copper, gold (via LBMA), global price indices | Daily/Monthly | Free API key, `fredapi` Python |
| **U.S. EIA Open Data** | WTI/Brent spot & futures, petroleum products, natural gas | Daily/Weekly | Free API key |
| **Yahoo Finance (`yfinance`)** | Front-month futures: CL=F, BZ=F, GC=F, SI=F, HG=F, ZC=F, ZW=F, ZS=F, NG=F etc. | Daily (intraday limited) | No key; unofficial — cross-validate |
| **Stooq** | Commodity futures/spot, long daily history | Daily | Free CSV download |
| **LBMA** | Gold/silver benchmark prices | Daily | Free on site |
| **IMF Primary Commodity Prices** | Broad commodity indices | Monthly | Free xlsx |

Note: strictly licensed exchange data (LME official settlement, ICE, CME granular) is paid — avoid designs that require it; front-month continuous futures from free sources suffice for most forecasting papers.

## 2. Predictors / exogenous variables

| Variable | Source | Notes |
|---|---|---|
| Geopolitical Risk (GPR) index, daily+monthly, country-level | Caldara & Iacoviello, matteoiacoviello.com | Free xlsx, updated monthly |
| Economic Policy Uncertainty (EPU), incl. country indices | policyuncertainty.com | Free |
| VIX, OVX (oil VIX), GVZ (gold VIX) | CBOE / FRED | Free |
| USD index, exchange rates | FRED | Free |
| Interest rates, term spreads | FRED | Free |
| Baltic Dry Index | Stooq / TradingView scrape | Verify licensing |
| CFTC Commitments of Traders (positioning) | CFTC website | Free CSV, weekly |
| EIA fundamentals (production, inventories, OPEC) | EIA API | Free |
| Kilian global real economic activity index | Dallas Fed | Free, monthly |
| News text (headlines) | GDELT (free), Common Crawl news | For text-augmented ideas |
| Google Trends | pytrends | Free |
| Weather/climate (for agri) | NOAA, ERA5 (CDS API), ECMWF open forecasts | Free with registration |

## 3. Benchmark conventions to respect (oil-forecasting literature)

- No-change (random walk) benchmark and futures-based benchmark are mandatory comparisons.
- Report MSPE ratios vs no-change, directional success ratios, Diebold-Mariano / Clark-West tests.
- Rolling/expanding out-of-sample evaluation; never tune on the final holdout (pre-register hyperparameters).
- For probabilistic forecasts: CRPS, interval coverage (PICP), winkler score; pinball loss for quantiles.

## 4. Ready-made benchmark datasets (if useful for credibility)

- M4/M5 competition data (for method-transfer framing)
- Monash Time Series Forecasting Repository (includes some commodity-related series)
- Kaggle commodity datasets — use only as convenience mirrors; always re-pull from primary sources for the paper.
