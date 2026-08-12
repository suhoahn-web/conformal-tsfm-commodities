"""Generate the data-quality report for the raw daily price panel.

Checks per series: coverage span, business-day gap statistics, zero/negative
prices, extreme daily moves; cross-source WTI/Brent spot-vs-futures agreement;
regime-window coverage (COVID / Ukraine / Hormuz holdout).
Output: data/DATA_QUALITY_REPORT.md
Run:  python data_quality_report.py
"""
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PRICES = ROOT / "data" / "raw" / "prices"
OUT_MD = ROOT / "data" / "DATA_QUALITY_REPORT.md"

REGIMES = {
    "COVID": ("2020-02-20", "2020-08-31"),
    "Ukraine": ("2022-02-24", "2022-08-31"),
    "Hormuz (HOLDOUT)": ("2026-02-28", "2026-07-31"),
}

SERIES = sorted(p.stem for p in PRICES.glob("*.csv"))


def load(name: str) -> pd.Series:
    df = pd.read_csv(PRICES / f"{name}.csv", parse_dates=["date"])
    col = "close" if "close" in df.columns else "price"
    return df.set_index("date")[col].sort_index()


def series_checks(name: str, s: pd.Series) -> dict:
    bdays = pd.bdate_range(s.index.min(), s.index.max())
    missing_bdays = len(bdays.difference(s.index))
    ret = np.log(s).diff()
    max_gap = int(s.index.to_series().diff().dt.days.max())
    regime_cov = {}
    for rname, (a, b) in REGIMES.items():
        window = pd.bdate_range(a, b)
        have = len(s.loc[a:b])
        regime_cov[rname] = f"{have}/{len(window)}"
    return {
        "series": name,
        "rows": len(s),
        "span": f"{s.index.min().date()} .. {s.index.max().date()}",
        "missing_bdays_pct": round(100 * missing_bdays / max(len(bdays), 1), 1),
        "max_gap_days": max_gap,
        "nonpositive": int((s <= 0).sum()),
        "abs_ret_gt20pct": int((ret.abs() > 0.20).sum()),
        **regime_cov,
    }


def main() -> None:
    rows, series_map = [], {}
    for name in SERIES:
        s = load(name)
        series_map[name] = s
        rows.append(series_checks(name, s))
    table = pd.DataFrame(rows)

    # Cross-source agreement: EIA spot vs Yahoo front-month futures (levels correlate;
    # basis exists, so we check log-return correlation, not price equality)
    xchecks = []
    for spot, fut in [("wti_spot", "wti_fut"), ("brent_spot", "brent_fut"),
                      ("henryhub_spot", "natgas_fut")]:
        if spot in series_map and fut in series_map:
            a = np.log(series_map[spot]).diff()
            b = np.log(series_map[fut]).diff()
            j = pd.concat([a, b], axis=1, join="inner").dropna()
            xchecks.append({
                "pair": f"{spot} vs {fut}", "overlap_days": len(j),
                "return_corr": round(j.corr().iloc[0, 1], 3),
            })
    xtable = pd.DataFrame(xchecks)

    lines = [
        "# Data Quality Report — Raw Daily Price Panel",
        f"\nGenerated: {datetime.now(timezone.utc).isoformat()} (script: src/data_cleaning/data_quality_report.py)",
        "\n## Per-series checks\n",
        table.to_markdown(index=False),
        "\nNotes: `missing_bdays_pct` counts business days without an observation "
        "(holidays inflate this slightly; investigate any series far above peers). "
        "`abs_ret_gt20pct` flags daily log-moves >20% (verify against known events, "
        "e.g., April 2020 negative WTI, Hormuz spike days — do NOT delete).",
        "\n## Cross-source agreement (daily log-return correlation)\n",
        xtable.to_markdown(index=False),
        "\nExpectation: spot-vs-front-month return correlation > 0.9 for WTI/Brent; "
        "Henry Hub spot-futures basis is looser. Investigate anything below 0.8.",
        "\n## Nonpositive prices",
        "\nWTI April 2020 contains a negative settlement (-$37.63, 2020-04-20) — this is REAL, "
        "keep it; it motivates evaluating in levels + asinh transform rather than logs for WTI.",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(table.to_string(index=False))
    print()
    print(xtable.to_string(index=False))
    print(f"\nReport written: {OUT_MD}")


if __name__ == "__main__":
    main()
