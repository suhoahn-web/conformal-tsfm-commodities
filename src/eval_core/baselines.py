"""Point-forecast baselines: no-change and recursive AR(p) on asinh-transformed prices.

The asinh transform (Lago-style variance stabilization; also handles WTI's
negative April-2020 print, unlike logs) is used for AR modeling; forecasts are
mapped back to price levels for evaluation.
"""
import numpy as np
import pandas as pd


def no_change(prices: pd.Series, horizon: int) -> pd.Series:
    """RW-without-drift: forecast for t+h made at t equals price at t (AKV benchmark).

    Returned series is indexed by the TARGET date, aligned to available targets.
    """
    fc = prices.shift(horizon)
    return fc.dropna()


def _fit_ar_ols(x: np.ndarray, p: int) -> np.ndarray:
    """OLS AR(p) with intercept on a 1-D array; returns coefficients [c, phi1..phip]."""
    rows = len(x) - p
    X = np.ones((rows, p + 1))
    for k in range(1, p + 1):
        X[:, k] = x[p - k: len(x) - k]
    y = x[p:]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def _iterate_ar(history: np.ndarray, beta: np.ndarray, p: int, horizon: int) -> float:
    buf = list(history[-p:])
    val = np.nan
    for _ in range(horizon):
        lags = buf[::-1][:p]
        val = beta[0] + float(np.dot(beta[1:], lags))
        buf.append(val)
    return val


def recursive_ar_returns_forecast(
    prices: pd.Series, horizon: int, origins: pd.DatetimeIndex, p: int = 5,
    refit_every: int = 21,
) -> pd.Series:
    """Recursive AR(p) on asinh-DIFFERENCES (returns), cumulated to a level forecast.

    Differencing removes the unit root that distorted the level-AR fit
    (2020 negative WTI print; see smoke-A deviation note). asinh handles
    nonpositive prices where log returns are undefined.
    """
    z = pd.Series(np.arcsinh(prices.values), index=prices.index)
    dz = z.diff().dropna()
    pos = prices.index.get_indexer(origins)
    if (pos < 0).any():
        raise ValueError("some origins not present in price index")
    out_idx, out_val = [], []
    beta = None
    for j, t_pos in enumerate(pos):
        if t_pos + horizon >= len(prices.index):
            break
        hist = dz.values[: t_pos]  # dz[k] = z[k+1]-z[k]; strictly pre-origin info
        if len(hist) < p + 30:
            continue
        if beta is None or j % refit_every == 0:
            beta = _fit_ar_ols(hist, p)
        buf = list(hist[-p:])
        cum = 0.0
        for _ in range(horizon):
            step = beta[0] + float(np.dot(beta[1:], buf[::-1][:p]))
            cum += step
            buf.append(step)
        out_idx.append(prices.index[t_pos + horizon])
        out_val.append(np.sinh(z.values[t_pos] + cum))
    return pd.Series(out_val, index=pd.DatetimeIndex(out_idx), name=f"ar{p}r_h{horizon}")


def recursive_ar_forecast(
    prices: pd.Series, horizon: int, origins: pd.DatetimeIndex, p: int = 5,
    refit_every: int = 21,
) -> pd.Series:
    """Recursive-origin (expanding window) AR(p) forecasts in asinh space.

    For each origin t in `origins`, fit on data up to t (refit every
    `refit_every` origins; coefficients reused in between — recalibration cost
    is negligible for OLS but this mirrors the monthly-recalibration protocol),
    iterate h steps ahead, return level forecast indexed by target date.
    """
    z = pd.Series(np.arcsinh(prices.values), index=prices.index)
    pos = prices.index.get_indexer(origins)
    if (pos < 0).any():
        raise ValueError("some origins not present in price index")
    out_idx, out_val = [], []
    beta = None
    for j, t_pos in enumerate(pos):
        if t_pos + horizon >= len(prices.index):
            break
        history = z.values[: t_pos + 1]
        if len(history) < p + 30:
            continue
        if beta is None or j % refit_every == 0:
            beta = _fit_ar_ols(history, p)
        zf = _iterate_ar(history, beta, p, horizon)
        out_idx.append(prices.index[t_pos + horizon])
        out_val.append(np.sinh(zf))
    return pd.Series(out_val, index=pd.DatetimeIndex(out_idx), name=f"ar{p}_h{horizon}")
