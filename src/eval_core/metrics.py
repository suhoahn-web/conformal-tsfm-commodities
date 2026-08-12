"""Evaluation metrics and tests per AKV (2013) + Lago et al. (2021) protocol.

All functions operate on aligned 1-D numpy arrays (no NaNs allowed; callers
must align explicitly — silent dropping is forbidden by project standards).
"""
import numpy as np
from scipy import stats


def _check(*arrays):
    n = {len(a) for a in arrays}
    if len(n) != 1:
        raise ValueError(f"length mismatch: {sorted(n)}")
    for a in arrays:
        if np.isnan(np.asarray(a, dtype=float)).any():
            raise ValueError("NaNs present — align and handle missing values explicitly")


def mspe_ratio(pred: np.ndarray, bench: np.ndarray, actual: np.ndarray) -> dict:
    """MSPE of `pred` relative to benchmark (`<1` means pred beats benchmark)."""
    _check(pred, bench, actual)
    mspe_p = np.mean((pred - actual) ** 2)
    mspe_b = np.mean((bench - actual) ** 2)
    return {"mspe": mspe_p, "mspe_bench": mspe_b, "mspe_ratio": mspe_p / mspe_b}


def rmae(pred: np.ndarray, naive: np.ndarray, actual: np.ndarray) -> float:
    """Relative MAE vs naive forecast (Lago et al. 2021; MAPE is banned)."""
    _check(pred, naive, actual)
    return float(np.mean(np.abs(pred - actual)) / np.mean(np.abs(naive - actual)))


def success_ratio(pred_change: np.ndarray, actual_change: np.ndarray) -> float:
    """Fraction of correctly predicted signs (AKV directional accuracy)."""
    _check(pred_change, actual_change)
    return float(np.mean(np.sign(pred_change) == np.sign(actual_change)))


def pesaran_timmermann(pred_change: np.ndarray, actual_change: np.ndarray) -> dict:
    """Pesaran-Timmermann sign-predictability test (static version).

    Returns NaN p-value when predicted signs never vary (test inapplicable,
    per AKV protocol note).
    """
    _check(pred_change, actual_change)
    x = (pred_change > 0).astype(float)
    y = (actual_change > 0).astype(float)
    n = len(y)
    if x.std() == 0 or y.std() == 0:
        return {"stat": np.nan, "pvalue": np.nan, "note": "sign never varies — PT inapplicable"}
    p_hat = np.mean(x == y)
    py, px = y.mean(), x.mean()
    p_star = py * px + (1 - py) * (1 - px)
    v_p = p_star * (1 - p_star) / n
    v_star = ((2 * py - 1) ** 2 * px * (1 - px) / n
              + (2 * px - 1) ** 2 * py * (1 - py) / n
              + 4 * py * px * (1 - py) * (1 - px) / n**2)
    denom = v_p - v_star
    if denom <= 0:
        return {"stat": np.nan, "pvalue": np.nan, "note": "degenerate variance"}
    stat = (p_hat - p_star) / np.sqrt(denom)
    return {"stat": float(stat), "pvalue": float(1 - stats.norm.cdf(stat))}


def diebold_mariano(e1: np.ndarray, e2: np.ndarray, h: int = 1, power: int = 2) -> dict:
    """DM test with Harvey-Leybourne-Newbold small-sample correction.

    H0: equal predictive accuracy. One-sided p (model 1 better) and two-sided p.
    Loss = |e|^power. Long-run variance via uniform (Bartlett-free) truncation
    at h-1 lags, per standard DM practice.
    """
    _check(e1, e2)
    d = np.abs(e1) ** power - np.abs(e2) ** power
    n = len(d)
    dbar = d.mean()
    gamma0 = np.mean((d - dbar) ** 2)
    lrv = gamma0
    for k in range(1, h):
        cov = np.mean((d[k:] - dbar) * (d[:-k] - dbar))
        lrv += 2 * cov
    if lrv <= 0:
        return {"stat": np.nan, "p_onesided": np.nan, "p_twosided": np.nan,
                "note": "nonpositive LRV (short sample / large h)"}
    dm = dbar / np.sqrt(lrv / n)
    hln = dm * np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    p_two = 2 * stats.t.sf(abs(hln), df=n - 1)
    p_one = stats.t.cdf(hln, df=n - 1)  # small loss diff (model1 better) -> negative stat
    return {"stat": float(hln), "p_onesided": float(p_one), "p_twosided": float(p_two)}


def giacomini_white(e1: np.ndarray, e2: np.ndarray, h: int = 1, power: int = 2) -> dict:
    """Giacomini-White (2006) conditional predictive ability test.

    Instruments: constant + lagged loss differential. Statistic is
    T * zbar' Omega^{-1} zbar ~ chi2(q) with a (h-1)-lag HAC Omega for h>1.
    """
    _check(e1, e2)
    d = np.abs(e1) ** power - np.abs(e2) ** power
    d_t = d[1:]
    z = np.column_stack([np.ones(len(d_t)), d[:-1]])
    zd = z * d_t[:, None]
    T = len(d_t)
    zbar = zd.mean(axis=0)
    omega = zd.T @ zd / T
    for k in range(1, h):
        g = zd[k:].T @ zd[:-k] / T
        omega += (g + g.T)
    try:
        stat = float(T * zbar @ np.linalg.solve(omega, zbar))
    except np.linalg.LinAlgError:
        return {"stat": np.nan, "pvalue": np.nan, "note": "singular omega"}
    if stat < 0:
        return {"stat": float(stat), "pvalue": np.nan, "note": "negative stat (HAC not PSD)"}
    p = float(1 - stats.chi2.cdf(stat, df=z.shape[1]))
    return {"stat": stat, "pvalue": p}


def model_confidence_set(
    losses: np.ndarray, model_names: list[str], alpha: float = 0.10,
    n_boot: int = 1000, block: int = 22, seed: int = 20260811,
) -> dict:
    """Hansen-Lunde-Nason (2011) MCS, range statistic, moving-block bootstrap.

    losses: (T, M) loss matrix. Returns surviving set at level alpha and
    elimination order with p-values.
    """
    rng = np.random.default_rng(seed)
    T, M = losses.shape
    if len(model_names) != M:
        raise ValueError("model_names length mismatch")
    n_blocks = int(np.ceil(T / block))
    boot_idx = np.empty((n_boot, n_blocks * block), dtype=int)
    starts = rng.integers(0, T - block + 1, size=(n_boot, n_blocks))
    for b in range(n_boot):
        boot_idx[b] = np.concatenate([np.arange(s, s + block) for s in starts[b]])
    boot_idx = boot_idx[:, :T]

    active = list(range(M))
    eliminated, pvals = [], []
    p_prev = 0.0
    while len(active) > 1:
        L = losses[:, active]
        dbar = L.mean(axis=0)[:, None] - L.mean(axis=0)[None, :]
        boot_means = losses[boot_idx][:, :, active].mean(axis=1)
        bd = boot_means[:, :, None] - boot_means[:, None, :]
        var_d = ((bd - dbar[None]) ** 2).mean(axis=0)
        np.fill_diagonal(var_d, 1.0)
        tstat_signed = dbar / np.sqrt(var_d)   # >0 where row i loses to column j
        tstat = np.abs(tstat_signed)
        TR = tstat.max()
        bt = np.abs(bd - dbar[None]) / np.sqrt(var_d[None])
        TR_boot = bt.reshape(n_boot, -1).max(axis=1)
        p = float((TR_boot >= TR).mean())
        p = max(p, p_prev)  # MCS p-values are made monotone
        p_prev = p
        # Hansen-Lunde-Nason elimination rule: drop the model with the largest
        # STUDENTISED loss differential against any competitor, e_R = argmax_i
        # max_j t_ij. Using argmax of the raw mean loss (as an earlier version of
        # this function did) is not the published rule and changes which model
        # leaves the set when variances differ across pairs.
        worst = int(np.argmax(tstat_signed.max(axis=1)))
        if p < alpha:
            eliminated.append(model_names[active[worst]])
            pvals.append(p)
            active.pop(worst)
        else:
            break
    return {
        "survivors": [model_names[i] for i in active],
        "eliminated": eliminated,
        "elim_pvalues": [round(v, 4) for v in pvals],
        "alpha": alpha,
    }


def interval_metrics(lo: np.ndarray, hi: np.ndarray, actual: np.ndarray, alpha: float) -> dict:
    """PICP, mean width, and Winkler (interval) score at nominal 1-alpha coverage."""
    _check(lo, hi, actual)
    covered = (actual >= lo) & (actual <= hi)
    width = hi - lo
    winkler = width.copy()
    below = actual < lo
    above = actual > hi
    winkler[below] += (2 / alpha) * (lo[below] - actual[below])
    winkler[above] += (2 / alpha) * (actual[above] - hi[above])
    return {
        "picp": float(covered.mean()),
        "nominal": 1 - alpha,
        "mean_width": float(width.mean()),
        "winkler": float(winkler.mean()),
    }


def pinball_loss(q_pred: np.ndarray, actual: np.ndarray, q: float) -> float:
    _check(q_pred, actual)
    diff = actual - q_pred
    return float(np.mean(np.maximum(q * diff, (q - 1) * diff)))


def var_backtest(var_q: np.ndarray, actual: np.ndarray, coverage: float) -> dict:
    """VaR backtests: Kupiec POF (unconditional) + Christoffersen independence
    and conditional coverage. `var_q` is the lower quantile forecast (e.g. q05
    for 95% VaR of a long position); a hit = actual < var_q.
    """
    _check(var_q, actual)
    hits = (actual < var_q).astype(int)
    n = len(hits)
    x = int(hits.sum())
    p = 1 - coverage
    pi_hat = x / n if n else np.nan
    eps = 1e-12
    lr_pof = -2 * (
        x * np.log(p + eps) + (n - x) * np.log(1 - p + eps)
        - (x * np.log(pi_hat + eps) + (n - x) * np.log(1 - pi_hat + eps))
    )
    p_pof = float(1 - stats.chi2.cdf(lr_pof, df=1))
    t00 = t01 = t10 = t11 = 0
    for a, b in zip(hits[:-1], hits[1:]):
        t00 += (a == 0) & (b == 0); t01 += (a == 0) & (b == 1)
        t10 += (a == 1) & (b == 0); t11 += (a == 1) & (b == 1)
    pi0 = t01 / (t00 + t01) if (t00 + t01) else 0.0
    pi1 = t11 / (t10 + t11) if (t10 + t11) else 0.0
    pi_all = (t01 + t11) / max(t00 + t01 + t10 + t11, 1)
    ll_ind = (t00 * np.log(1 - pi0 + eps) + t01 * np.log(pi0 + eps)
              + t10 * np.log(1 - pi1 + eps) + t11 * np.log(pi1 + eps))
    ll_null = ((t00 + t10) * np.log(1 - pi_all + eps) + (t01 + t11) * np.log(pi_all + eps))
    lr_ind = -2 * (ll_null - ll_ind)
    p_ind = float(1 - stats.chi2.cdf(max(lr_ind, 0), df=1))
    lr_cc = lr_pof + max(lr_ind, 0)
    p_cc = float(1 - stats.chi2.cdf(lr_cc, df=2))
    return {
        "hit_rate": round(pi_hat, 4), "expected": round(p, 4), "n": n,
        "kupiec_p": round(p_pof, 4), "christoffersen_ind_p": round(p_ind, 4),
        "conditional_coverage_p": round(p_cc, 4),
    }
