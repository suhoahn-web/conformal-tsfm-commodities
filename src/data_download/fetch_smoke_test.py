"""Smoke test: verify free daily commodity price sources are reachable and parseable.

Working sources found 2026-08-11 (this environment):
  - EIA hist_xls direct downloads (daily spot: WTI, Brent, Henry Hub, ...)
  - Yahoo Finance v8 chart API (daily front-month futures: GC=F, HG=F, ...)
  - World Bank Pink Sheet monthly xlsx (cross-check)
Blocked in this environment: FRED fredgraph.csv (bot protection; use official
FRED API with a key later as cross-check), Stooq (JS challenge).

Run:  python fetch_smoke_test.py
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "smoke_test"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

EIA_XLS = {
    "wti_spot_eia": "https://www.eia.gov/dnav/pet/hist_xls/RWTCd.xls",
    "brent_spot_eia": "https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls",
    "henryhub_spot_eia": "https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls",
}

YAHOO_FUTURES = {
    "gold_fut_yahoo": "GC=F",
    "silver_fut_yahoo": "SI=F",
    "copper_fut_yahoo": "HG=F",
    "corn_fut_yahoo": "ZC=F",
    "wheat_fut_yahoo": "ZW=F",
    "soybean_fut_yahoo": "ZS=F",
}

WORLDBANK_PINKSHEET = (
    "https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021"
    "/related/CMO-Historical-Data-Monthly.xlsx"
)


def _meta(name: str, url: str, df: pd.DataFrame, date_col: str, path: Path) -> dict:
    return {
        "name": name,
        "url": url,
        "rows": len(df),
        "first_date": str(df[date_col].min().date()),
        "last_date": str(df[date_col].max().date()),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "file": str(path),
    }


def fetch_eia(name: str, url: str) -> dict:
    resp = requests.get(url, timeout=60, headers=UA)
    resp.raise_for_status()
    path = RAW_DIR / f"{name}.xls"
    path.write_bytes(resp.content)
    # EIA hist_xls: sheet "Data 1", header on row 3 (0-indexed 2)
    df = pd.read_excel(path, sheet_name="Data 1", skiprows=2)
    df = df.rename(columns={df.columns[0]: "date"}).dropna()
    df["date"] = pd.to_datetime(df["date"])
    return _meta(name, url, df, "date", path)


def fetch_yahoo(name: str, symbol: str) -> dict:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=max&interval=1d"
    resp = requests.get(url, timeout=60, headers=UA)
    resp.raise_for_status()
    result = resp.json()["chart"]["result"][0]
    quote = result["indicators"]["quote"][0]
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_convert(None),
            "open": quote["open"],
            "high": quote["high"],
            "low": quote["low"],
            "close": quote["close"],
            "volume": quote["volume"],
        }
    ).dropna(subset=["close"])
    path = RAW_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    return _meta(name, url, df, "date", path)


def fetch_pinksheet() -> dict:
    resp = requests.get(WORLDBANK_PINKSHEET, timeout=90, headers=UA)
    resp.raise_for_status()
    path = RAW_DIR / "worldbank_pinksheet_monthly.xlsx"
    path.write_bytes(resp.content)
    df = pd.read_excel(path, sheet_name="Monthly Prices", skiprows=4)
    return {
        "name": "worldbank_pinksheet",
        "url": WORLDBANK_PINKSHEET,
        "rows": len(df),
        "first_date": "1960-01 (monthly)",
        "last_date": "see sheet",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "file": str(path),
    }


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results, failures = [], []

    jobs = [(n, lambda n=n, u=u: fetch_eia(n, u)) for n, u in EIA_XLS.items()]
    jobs += [(n, lambda n=n, s=s: fetch_yahoo(n, s)) for n, s in YAHOO_FUTURES.items()]
    jobs.append(("worldbank_pinksheet", fetch_pinksheet))

    for name, job in jobs:
        try:
            meta = job()
            results.append(meta)
            print(f"OK   {name:22s} {meta['rows']:>6} rows  {meta['first_date']} .. {meta['last_date']}")
        except Exception as exc:  # noqa: BLE001 - smoke test reports every failure kind
            failures.append({"name": name, "error": repr(exc)})
            print(f"FAIL {name:22s} {exc!r}")
        time.sleep(1)  # be polite to free endpoints

    (RAW_DIR / "retrieval_metadata.json").write_text(
        json.dumps({"results": results, "failures": failures}, indent=2), encoding="utf-8"
    )
    print(f"\n{len(results)} OK / {len(failures)} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
