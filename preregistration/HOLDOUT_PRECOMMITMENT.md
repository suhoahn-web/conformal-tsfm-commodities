# Pre-commitment: how the Hormuz holdout will be interpreted

Written **before** unsealing (2026-08-11). Required by RESEARCH_PLAN_v1 §4 step 6 and by
the structure map (¶5.11–5.12, ¶7.4). Purpose: fix the interpretation of every possible
outcome in advance so the write-up cannot be reverse-engineered from the result.

The holdout window is 2026-02-28 .. 2026-07-31 (Iran–Hormuz shock; Brent's largest
one-month move on record). All model predictions for this window already exist in the
immutable cache and were produced by frozen, zero-shot or pre-2015-trained models; no
tuning decision has ever seen this window. `analysis/final_hormuz/run_hormuz_final.py`
is written, refuses to run without an approval file, and refuses to run twice.

---

## Primary pre-registered hypothesis (H-Hormuz)

> Native TSFM prediction intervals and static split-conformal intervals will under-cover
> in the Hormuz window (PICP materially below nominal), while ACI will remain close to
> nominal; the point-forecast ranking (no-change and statistical baselines at least as
> good as TSFMs) will be unchanged.

This is the pattern already established out-of-sample in COVID-2020 and Ukraine-2022.

---

## Outcome A — pattern replicates (ACI ≈ nominal, native/split under-cover)

**Interpretation (pre-committed):** the calibration failure is a general property of
crisis regimes, now confirmed on the largest oil shock in the sample and on a window that
post-dates every model's pretraining decision. Adaptive conformal calibration is the
recommended practice for commodity uncertainty quantification.

**Writing consequence:** ¶5.11 reports it as confirmation; the abstract may state the
crisis-calibration claim without hedging; Discussion ¶6.x keeps the practitioner
recommendation as-is.

**Forbidden:** describing this as "prediction" of the shock. Nothing here forecasts the
war; the claim is strictly about coverage of intervals during it.

---

## Outcome B — everything degrades, ACI included (ACI also far below nominal)

**Interpretation (pre-committed):** adaptive conformal calibration mitigates but does not
solve extreme structural breaks; the adaptation horizon (γ, calibration window) is too
slow for a shock of this speed. This is a **limitation finding, reported as prominently as
the positive ones**, and it strengthens rather than weakens the paper's core message that
uncertainty quantification in commodity markets is unsolved.

**Writing consequence:** ¶5.11 reports the failure; the abstract's conformal claim gets an
explicit scope restriction ("moderate crises"); Discussion gains a paragraph on the
adaptation-speed limit and names it as future work (faster γ schedules, regime-aware
recalibration). The title's "across crisis regimes" stays — the audit still spans them.

**Forbidden:** re-tuning γ or the calibration window on this data and reporting the tuned
version as the result. If a γ sensitivity analysis is run at all, it must be labeled
post hoc and exploratory, and the pre-registered γ = 0.02 result must be reported first
and in the abstract.

---

## Outcome C — TSFMs unexpectedly beat no-change in this window

**Interpretation (pre-committed):** a single 5-month crisis window with ~110 business days
per series is far too small to overturn an 11-year, 30-combination MCS result; a trending
market mechanically favors any model with drift over a random walk. It would be reported
as an intriguing regime-dependent exception, **not** as a reversal of the paper's finding,
and accompanied by (i) the point that no-change is hardest to beat in calm markets and
(ii) an explicit note about the sample size.

**Writing consequence:** ¶5.12 reports it with those caveats; the abstract's point-forecast
claim is qualified with "outside acute trending shocks"; no change to the conclusion that
practitioners should not expect zero-shot TSFM gains in general.

**Forbidden:** promoting this into the headline claim, or dropping the calm/COVID/Ukraine
evidence to feature it.

---

## Rules binding all outcomes

1. `run_hormuz_final.py` runs **exactly once**. Its metric set is frozen; no metric may be
   added after seeing the output.
2. Every number in the manuscript comes from the script's CSV output, quoted directly —
   never retyped from a conversation summary. (A mis-transcribed figure already occurred
   once during this project and was caught by cross-checking against source files.)
3. The window is never used to select models, horizons, series, conformal variants, or
   hyperparameters.
4. If the script errors, the fix must not depend on the values observed; any code change
   after unsealing is logged in the Deviation Log with the reason.
5. Series with fewer than 30 usable observations in the window are dropped by the script's
   own rule, uniformly across models, and the count is reported.

---

## Approval procedure

Unsealing requires the user to create
`analysis/final_hormuz/HORMUZ_UNSEAL_APPROVED.txt` containing an explicit sentence of
approval and the date. Claude will not create this file.
