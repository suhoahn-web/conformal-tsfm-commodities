# Pre-commitment: how the E3/E4 sweep will be read

Written 2026-08-13 **while the sweep was still running and before any output existed**,
for the same reason the Hormuz window has `HORMUZ_PRECOMMIT.md`: a robustness check that
threatens the paper's headline is exactly the check whose interpretation is easiest to
bend after the fact.

## The question

The manuscript compares one rolling conformal baseline (250 observations, fixed nominal
level) against ACI (γ = 0.02) and concludes that the non-adaptive construction fails in
crises. A referee will ask whether a **shorter** window would have adapted on its own.

Reference values from the pre-registered run, nominal 0.80, pooled median PICP:

| construction | h=5 COVID | h=5 Ukraine | h=22 COVID | h=22 Ukraine |
|---|---|---|---|---|
| Rolling-SC(250) | 0.704 | 0.698 | 0.637 | 0.599 |
| ACI (γ=0.02) | 0.774 | 0.794 | 0.756 | 0.763 |

## Outcome A — short windows do NOT close the gap

*Definition:* the best window in {50, 100, 500} stays materially below ACI in the crisis
cells — say, still 3+ points under ACI and under nominal.

**Then the headline strengthens and we say so plainly.** The failure is a property of
fixed-level trailing calibration, not of our particular window choice, and we can state
that we looked for the obvious escape route and it was not there. Text change: rename to
`Rolling-SC(w)`, report the sweep as a robustness table, keep the claim.

## Outcome B — short windows largely close the gap

*Definition:* a 50- or 100-observation window reaches within ~1–2 points of ACI in the
crisis cells.

**Then our headline is partly self-inflicted and must be narrowed.** The honest claim
becomes: *a 250-observation trailing window adapts too slowly; shortening it recovers most
of the benefit, and ACI achieves the same without having to pick a window.* The abstract,
§1.6 contribution 2, §5.4 and §7.3 all change. ACI's remaining advantage — one fewer
tuning decision, and no window that has to be chosen per regime — is real but much
smaller, and we say that.

## Outcome C — short windows overshoot

*Definition:* short windows over-cover (well above 0.80) or their intervals blow out in
width.

**Then the comparison must be reported on both axes, not coverage alone.** Coverage bought
with unbounded width is not a win; we report width and interval score alongside, and the
claim becomes about the coverage–width frontier rather than coverage.

## Binding rules

1. Whatever comes out is reported. The sweep is **not** re-run with different grids to get
   a friendlier answer.
2. The pre-registered configuration (250, γ = 0.02) stays the headline configuration. This
   is a post-hoc robustness analysis and is labelled as one.
3. γ sensitivity (E4) is reported even if it shows the pre-registered γ was not the best
   choice. Especially then.
4. The full sweep CSV goes into the public repository regardless of outcome.
5. If Outcome B holds, the deviation log records that the original framing overstated the
   result, with the date.
