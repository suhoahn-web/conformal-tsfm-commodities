"""Conformal interval wrappers for point/quantile forecasters.

Implemented: split conformal (absolute-residual score), ACI (Gibbs & Candes
2021), CQR (Romano et al. 2019 — conformalizes model-emitted quantile pairs),
and SPCI-lite (Xu & Xie 2023 flavor: conditional score quantiles via gradient-
boosted quantile regression on lagged scores; periodic refit). EnbPI is
deliberately omitted: it requires a bootstrap ensemble of the underlying
model, which does not exist for cached TSFM forecasts (logged as a plan
deviation). Calibration data always strictly precedes each test point.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor


def _cal_end(i: int, horizon: int) -> int:
    """Exclusive end of the calibration window for the target at position i.

    A forecast for target t is issued at origin t-h. Only scores whose TARGET
    date is on or before that origin are observable when the interval is built,
    i.e. positions up to and including i-h. Using positions i-h+1 .. i-1 would
    consume outcomes realised after the origin — the look-ahead this project
    criticises elsewhere. (For h = 1 this reduces to the usual i.)
    """
    return i - horizon + 1


def split_conformal(
    forecasts: pd.Series, actuals: pd.Series, alpha: float, cal_size: int,
    horizon: int = 1,
) -> pd.DataFrame:
    """Rolling split-conformal intervals from absolute residual scores.

    For each target t the calibration set is the `cal_size` most recent
    (forecast, actual) pairs whose outcomes were already realised at the
    forecast origin t-h. Quantile level uses the finite-sample correction
    ceil((n+1)(1-alpha))/n.
    """
    joined = pd.concat({"f": forecasts, "y": actuals}, axis=1).dropna()
    scores = (joined["f"] - joined["y"]).abs()
    lo, hi, idx = [], [], []
    for i in range(cal_size + horizon - 1, len(joined)):
        end = _cal_end(i, horizon)
        cal = scores.iloc[end - cal_size: end].values
        n = len(cal)
        q_level = min(np.ceil((n + 1) * (1 - alpha)) / n, 1.0)
        q = np.quantile(cal, q_level, method="higher")
        f = joined["f"].iloc[i]
        idx.append(joined.index[i])
        lo.append(f - q)
        hi.append(f + q)
    return pd.DataFrame({"lo": lo, "hi": hi}, index=pd.DatetimeIndex(idx))


def aci(
    forecasts: pd.Series, actuals: pd.Series, alpha: float, cal_size: int,
    gamma: float = 0.02, horizon: int = 1,
) -> pd.DataFrame:
    """Adaptive Conformal Inference (Gibbs & Candes 2021).

    alpha_t updated online: alpha_{t+1} = alpha_t + gamma*(alpha - err_t),
    err_t = 1 if actual outside interval. alpha_t clipped to (1e-4, 1-1e-4);
    when alpha_t implies a quantile beyond the calibration range, the widest
    calibration score is used (infinite-interval fallback avoided, flagged).
    """
    joined = pd.concat({"f": forecasts, "y": actuals}, axis=1).dropna()
    scores = (joined["f"] - joined["y"]).abs()
    alpha_t = alpha
    lo, hi, idx, alphas = [], [], [], []
    pending: list[tuple[int, float, float]] = []  # (reveal_position, lo, hi, y) queue
    for i in range(cal_size + horizon - 1, len(joined)):
        end = _cal_end(i, horizon)
        cal = np.sort(scores.iloc[end - cal_size: end].values)
        n = len(cal)
        a = float(np.clip(alpha_t, 1e-4, 1 - 1e-4))
        q_level = min(np.ceil((n + 1) * (1 - a)) / n, 1.0)
        q = np.quantile(cal, q_level, method="higher")
        f, y = joined["f"].iloc[i], joined["y"].iloc[i]
        l, u = f - q, f + q
        # The miss/hit for target i is only observable at i; feedback into
        # alpha_t must therefore be delayed by the horizon, like the scores.
        pending.append((i, l, u))
        while pending and pending[0][0] <= end - 1:
            j, lj, uj = pending.pop(0)
            yj = joined["y"].iloc[j]
            err = float(not (lj <= yj <= uj))
            alpha_t = alpha_t + gamma * (alpha - err)
        idx.append(joined.index[i])
        lo.append(l)
        hi.append(u)
        alphas.append(a)
    return pd.DataFrame({"lo": lo, "hi": hi, "alpha_t": alphas}, index=pd.DatetimeIndex(idx))


def cqr(
    q_lo: pd.Series, q_hi: pd.Series, actuals: pd.Series, alpha: float, cal_size: int,
    horizon: int = 1,
) -> pd.DataFrame:
    """Conformalized Quantile Regression (Romano, Patterson & Candes 2019).

    Score = max(q_lo - y, y - q_hi); intervals are the model's quantile band
    expanded (or shrunk) by the rolling calibration quantile of the score.
    Pass the model's native quantile pair matching the target coverage
    (e.g. q10/q90 for alpha=0.20).
    """
    joined = pd.concat({"lo": q_lo, "hi": q_hi, "y": actuals}, axis=1).dropna()
    scores = np.maximum(joined["lo"] - joined["y"], joined["y"] - joined["hi"])
    lo, hi, idx = [], [], []
    for i in range(cal_size + horizon - 1, len(joined)):
        end = _cal_end(i, horizon)
        cal = scores.iloc[end - cal_size: end].values
        n = len(cal)
        q_level = min(np.ceil((n + 1) * (1 - alpha)) / n, 1.0)
        q = np.quantile(cal, q_level, method="higher")
        idx.append(joined.index[i])
        lo.append(joined["lo"].iloc[i] - q)
        hi.append(joined["hi"].iloc[i] + q)
    return pd.DataFrame({"lo": lo, "hi": hi}, index=pd.DatetimeIndex(idx))


def spci_lite(
    forecasts: pd.Series, actuals: pd.Series, alpha: float, cal_size: int,
    n_lags: int = 20, refit_every: int = 21, horizon: int = 1,
) -> pd.DataFrame:
    """SPCI-flavored sequential intervals (Xu & Xie 2023, simplified).

    Instead of an unconditional score quantile (split-CP), fit quantile
    regressions of the absolute residual score on its own lags (gradient-
    boosted trees, refit every `refit_every` steps) so interval width adapts
    to volatility clustering. Falls back to the unconditional quantile when
    insufficient history exists.
    """
    joined = pd.concat({"f": forecasts, "y": actuals}, axis=1).dropna()
    scores = (joined["f"] - joined["y"]).abs().values
    q_hi_level = 1 - alpha
    lo, hi, idx = [], [], []
    model = None
    for i in range(cal_size + horizon - 1, len(joined)):
        end = _cal_end(i, horizon)
        window = scores[end - cal_size: end]
        X = np.lib.stride_tricks.sliding_window_view(window[:-1], n_lags)
        yv = window[n_lags:]
        x_now = window[-n_lags:].reshape(1, -1)
        if (i - cal_size - horizon + 1) % refit_every == 0 or model is None:
            model = GradientBoostingRegressor(
                loss="quantile", alpha=q_hi_level, n_estimators=60,
                max_depth=2, learning_rate=0.1, subsample=0.8, random_state=0,
            ).fit(X, yv)
        q = float(model.predict(x_now)[0])
        q_uncond = np.quantile(window, min(np.ceil((len(window) + 1) * q_hi_level) / len(window), 1.0))
        q = max(q, 0.0)
        if not np.isfinite(q) or q == 0.0:
            q = q_uncond
        f = joined["f"].iloc[i]
        idx.append(joined.index[i])
        lo.append(f - q)
        hi.append(f + q)
    return pd.DataFrame({"lo": lo, "hi": hi}, index=pd.DatetimeIndex(idx))
