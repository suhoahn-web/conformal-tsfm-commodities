"""Phase 2 statistical baselines: GARCH(1,1)-t, LEAR-lite, QR-AR.

All operate in asinh-difference (return) space, cumulated to h-step price
forecasts, recursive origins with monthly (21-origin) refits, expanding window
capped at the most recent 1500 obs (Lago 4y-window spirit, adapted to daily
commodities — adaptation noted in plan §3.3).

Outputs: same immutable-cache schema as phase 1 (point + q05..q95 where the
model is distributional).
Run:  python run_phase2_baselines.py [garch|lear|qrar|all]
"""
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
PRICES = ROOT / "data" / "raw" / "prices"
PRED = ROOT / "outputs" / "predictions"
SERIES = ["wti_fut", "brent_fut", "natgas_fut", "gold_fut", "silver_fut",
          "copper_fut", "platinum_fut", "corn_fut", "wheat_fut", "soybean_fut"]
HORIZONS = [1, 5, 22]
EVAL_START = "2015-01-01"
CONTEXT = 512  # keep origin set identical to phase 1
QUANTILES = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
REFIT = 21
MAX_WIN = 1500
np.random.seed(20260811)


def load(name: str) -> pd.Series:
    df = pd.read_csv(PRICES / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].sort_index()


def targets(prices: pd.Series, h: int) -> np.ndarray:
    idx = prices.index
    pos = np.arange(len(idx))
    return pos[(idx >= EVAL_START) & (pos >= CONTEXT + h)]


def save(rows: list, model: str, series: str, h: int) -> None:
    out = PRED / f"{model}__{series}__h{h}.csv"
    if out.exists():
        raise FileExistsError(out)
    pd.DataFrame(rows).set_index("target_date").to_csv(out)


def run_garch(series: str) -> None:
    from arch import arch_model
    prices = load(series)
    z = np.arcsinh(prices.values)
    dz = np.diff(z) * 100  # arch prefers pct-scale
    idx = prices.index
    for h in HORIZONS:
        out = PRED / f"garch_t__{series}__h{h}.csv"
        if out.exists():
            print(f"skip {out.name}", flush=True)
            continue
        tps = targets(prices, h)
        rows, res = [], None
        t0 = time.time()
        for j, tp in enumerate(tps):
            op = tp - h
            hist = dz[max(0, op - MAX_WIN): op]  # dz[k]=z[k+1]-z[k]; last usable ends at op-1
            if j % REFIT == 0 or res is None:
                am = arch_model(hist, vol="GARCH", p=1, q=1, dist="t", mean="Constant")
                res = am.fit(disp="off", show_warning=False)
            fc = res.forecast(horizon=h, reindex=False)
            var_path = fc.variance.values[-1, :h]
            mu = float(res.params.get("mu", 0.0))
            nu = float(res.params.get("nu", 8.0))
            tot_mu = mu * h
            tot_sd = float(np.sqrt(var_path.sum()))
            scale = tot_sd * np.sqrt((nu - 2) / nu) if nu > 2 else tot_sd
            qv = {}
            for q in QUANTILES:
                dq = tot_mu + scale * sps.t.ppf(q, df=nu)
                qv[f"q{int(q*100):02d}"] = float(np.sinh(z[op] + dq / 100))
            rows.append({
                "target_date": idx[tp], "origin_date": idx[op],
                "actual": prices.values[tp], "point": qv["q50"], **qv,
            })
        save(rows, "garch_t", series, h)
        print(f"garch_t {series} h={h}: {len(rows)} in {time.time()-t0:.0f}s", flush=True)


def _lag_matrix(dz: np.ndarray, p: int, dow: np.ndarray, h: int):
    """Features at origin k: dz[k-p..k-1] + day-of-week; target: sum dz[k..k+h-1]."""
    n = len(dz)
    rows_X, rows_y, ks = [], [], []
    for k in range(p, n - h + 1):
        rows_X.append(np.concatenate([dz[k - p: k][::-1], dow[k]]))
        rows_y.append(dz[k: k + h].sum())
        ks.append(k)
    return np.array(rows_X), np.array(rows_y), np.array(ks)


def run_lear(series: str) -> None:
    from sklearn.linear_model import LassoLarsIC
    prices = load(series)
    z = np.arcsinh(prices.values)
    dz = np.diff(z)
    idx = prices.index
    dow_all = pd.get_dummies(pd.Series(idx[1:].dayofweek)).reindex(columns=range(5), fill_value=0).values.astype(float)
    P = 21
    for h in HORIZONS:
        out = PRED / f"lear_lite__{series}__h{h}.csv"
        if out.exists():
            print(f"skip {out.name}", flush=True)
            continue
        tps = targets(prices, h)
        rows, model = [], None
        t0 = time.time()
        for j, tp in enumerate(tps):
            op = tp - h  # origin position in price index; dz index k = price pos k+1... dz[k]=z[k+1]-z[k]
            k_end = op  # last dz usable: dz[op-1]; target = dz[op..op+h-1]
            lo = max(P, k_end - MAX_WIN)
            X_tr, y_tr, _ = _lag_matrix(dz[lo - P: k_end], P, dow_all[lo - P: k_end], h)
            if len(y_tr) < 100:
                continue
            if j % REFIT == 0 or model is None:
                model = LassoLarsIC(criterion="aic").fit(X_tr[:-1], y_tr[:-1])
            x_now = np.concatenate([dz[k_end - P: k_end][::-1], dow_all[min(k_end, len(dow_all) - 1)]])
            cum = float(model.predict(x_now.reshape(1, -1))[0])
            # Numerical guard: sinh() amplifies exponentially, so an occasional wild
            # LASSO extrapolation (observed on WTI around the April-2020 negative
            # print) produced forecasts ~1e13 times the price level and corrupted
            # every statistic downstream. Clip the cumulated asinh move to the
            # historical range of h-step moves in the training window. Applied
            # uniformly, using training data only.
            hist_cum = np.convolve(y_tr, np.ones(1), mode="valid")
            lim_lo, lim_hi = np.quantile(hist_cum, [0.001, 0.999])
            span = lim_hi - lim_lo
            cum = float(np.clip(cum, lim_lo - span, lim_hi + span))
            rows.append({
                "target_date": idx[tp], "origin_date": idx[op],
                "actual": prices.values[tp], "point": float(np.sinh(z[op] + cum)),
            })
        save(rows, "lear_lite", series, h)
        print(f"lear_lite {series} h={h}: {len(rows)} in {time.time()-t0:.0f}s", flush=True)


def run_qrar(series: str) -> None:
    import statsmodels.api as sm
    prices = load(series)
    z = np.arcsinh(prices.values)
    dz = np.diff(z)
    idx = prices.index
    P = 5
    for h in HORIZONS:
        out = PRED / f"qr_ar__{series}__h{h}.csv"
        if out.exists():
            print(f"skip {out.name}", flush=True)
            continue
        tps = targets(prices, h)
        rows, fits = [], None
        t0 = time.time()
        for j, tp in enumerate(tps):
            op = tp - h
            k_end = op
            lo = max(P, k_end - MAX_WIN)
            X_tr, y_tr, _ = _lag_matrix(dz[lo - P: k_end], P, np.zeros((k_end - (lo - P), 0)), h)
            if len(y_tr) < 100:
                continue
            if j % REFIT == 0 or fits is None:
                Xc = sm.add_constant(X_tr[:-1], has_constant="add")
                fits = {}
                for q in QUANTILES:
                    fits[q] = sm.QuantReg(y_tr[:-1], Xc).fit(q=q, max_iter=200)
            x_now = np.concatenate([[1.0], dz[k_end - P: k_end][::-1]])
            qv = {}
            for q in QUANTILES:
                cum = float(fits[q].predict(x_now.reshape(1, -1))[0])
                qv[f"q{int(q*100):02d}"] = float(np.sinh(z[op] + cum))
            vals = np.sort([qv[f"q{int(q*100):02d}"] for q in QUANTILES])
            for q, v in zip(QUANTILES, vals):  # enforce monotonicity
                qv[f"q{int(q*100):02d}"] = float(v)
            rows.append({
                "target_date": idx[tp], "origin_date": idx[op],
                "actual": prices.values[tp], "point": qv["q50"], **qv,
            })
        save(rows, "qr_ar", series, h)
        print(f"qr_ar {series} h={h}: {len(rows)} in {time.time()-t0:.0f}s", flush=True)


def main() -> None:
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    PRED.mkdir(parents=True, exist_ok=True)
    for s in SERIES:
        if which in ("garch", "all"):
            run_garch(s)
        if which in ("lear", "all"):
            run_lear(s)
        if which in ("qrar", "all"):
            run_qrar(s)
    print("phase 2 baselines complete", flush=True)


if __name__ == "__main__":
    main()
