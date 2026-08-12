"""Full-history daily commodity price collection (free sources, verified 2026-08-11).

Sources:
  - EIA hist_xls direct: daily spot (WTI, Brent, Henry Hub, heating oil, RBOB)
  - Yahoo v8 chart API: daily front-month futures, fetched in 1-year chunks
    (range=max silently degrades to monthly — never use it)
  - World Bank Pink Sheet: monthly cross-check panel

Output: data/raw/prices/{series}.csv + retrieval_metadata.json
Raw files are never edited; reruns overwrite the raw mirror only.
Run:  python fetch_daily_panel.py
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "prices"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
START_YEAR = 2000
END_TS = int(datetime(2026, 8, 11, tzinfo=timezone.utc).timestamp())

EIA_XLS = {
    "wti_spot": "https://www.eia.gov/dnav/pet/hist_xls/RWTCd.xls",
    "brent_spot": "https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls",
    "henryhub_spot": "https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls",
    # NY Harbor No.2 heating oil / RBOB conventional gasoline (names follow EIA dnav pattern)
    "heatingoil_spot": "https://www.eia.gov/dnav/pet/hist_xls/EER_EPD2F_PF4_Y35NY_DPGd.xls",
    "rbob_spot": "https://www.eia.gov/dnav/pet/hist_xls/EER_EPMRU_PF4_Y35NY_DPGd.xls",
}

YAHOO_FUTURES = {
    "wti_fut": "CL=F",
    "brent_fut": "BZ=F",
    "natgas_fut": "NG=F",
    "gold_fut": "GC=F",
    "silver_fut": "SI=F",
    "copper_fut": "HG=F",
    "platinum_fut": "PL=F",
    "corn_fut": "ZC=F",
    "wheat_fut": "ZW=F",
    "soybean_fut": "ZS=F",
}

PINKSHEET_URL = (
    "https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021"
    "/related/CMO-Historical-Data-Monthly.xlsx"
)


def fetch_eia(name: str, url: str) -> dict:
    resp = requests.get(url, timeout=90, headers=UA)
    resp.raise_for_status()
    xls_path = OUT_DIR / f"{name}.xls"
    xls_path.write_bytes(resp.content)
    df = pd.read_excel(xls_path, sheet_name="Data 1", skiprows=2)
    df = df.rename(columns={df.columns[0]: "date", df.columns[1]: "price"})[["date", "price"]]
    df = df.dropna()
    df["date"] = pd.to_datetime(df["date"])
    csv_path = OUT_DIR / f"{name}.csv"
    df.to_csv(csv_path, index=False)
    return {
        "name": name, "source": "EIA", "url": url, "rows": len(df),
        "first_date": str(df["date"].min().date()), "last_date": str(df["date"].max().date()),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(), "file": str(csv_path),
    }


def fetch_yahoo_chunked(name: str, symbol: str) -> dict:
    frames = []
    for year in range(START_YEAR, 2027):
        p1 = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
        p2 = min(int(datetime(year + 1, 1, 1, tzinfo=timezone.utc).timestamp()), END_TS)
        if p1 >= END_TS:
            break
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        resp = requests.get(
            url, params={"period1": p1, "period2": p2, "interval": "1d"},
            timeout=60, headers=UA,
        )
        if resp.status_code in (400, 404):  # symbol not listed yet in this window
            continue
        resp.raise_for_status()
        result = resp.json()["chart"]["result"]
        if not result or "timestamp" not in result[0]:
            continue
        res = result[0]
        quote = res["indicators"]["quote"][0]
        frames.append(pd.DataFrame({
            "date": pd.to_datetime(res["timestamp"], unit="s", utc=True).tz_convert(None).normalize(),
            "open": quote["open"], "high": quote["high"], "low": quote["low"],
            "close": quote["close"], "volume": quote["volume"],
        }))
        time.sleep(0.6)
    if not frames:
        raise ValueError(f"{name}: no data returned for any chunk")
    df = pd.concat(frames).dropna(subset=["close"]).drop_duplicates(subset="date").sort_values("date")
    csv_path = OUT_DIR / f"{name}.csv"
    df.to_csv(csv_path, index=False)
    return {
        "name": name, "source": "Yahoo", "symbol": symbol, "rows": len(df),
        "first_date": str(df["date"].min().date()), "last_date": str(df["date"].max().date()),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(), "file": str(csv_path),
    }


def fetch_pinksheet() -> dict:
    resp = requests.get(PINKSHEET_URL, timeout=120, headers=UA)
    resp.raise_for_status()
    path = OUT_DIR / "worldbank_pinksheet_monthly.xlsx"
    path.write_bytes(resp.content)
    df = pd.read_excel(path, sheet_name="Monthly Prices", skiprows=4)
    return {
        "name": "worldbank_pinksheet", "source": "WorldBank", "url": PINKSHEET_URL,
        "rows": len(df), "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "file": str(path),
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results, failures = [], []
    jobs = [(n, lambda n=n, u=u: fetch_eia(n, u)) for n, u in EIA_XLS.items()]
    jobs += [(n, lambda n=n, s=s: fetch_yahoo_chunked(n, s)) for n, s in YAHOO_FUTURES.items()]
    jobs.append(("worldbank_pinksheet", fetch_pinksheet))

    for name, job in jobs:
        try:
            meta = job()
            results.append(meta)
            span = f"{meta.get('first_date', '?')} .. {meta.get('last_date', '?')}"
            print(f"OK   {name:20s} {meta['rows']:>6} rows  {span}")
        except Exception as exc:  # noqa: BLE001 - collection must report every failure kind
            failures.append({"name": name, "error": repr(exc)})
            print(f"FAIL {name:20s} {exc!r}")

    (OUT_DIR / "retrieval_metadata.json").write_text(
        json.dumps({"results": results, "failures": failures}, indent=2), encoding="utf-8"
    )
    print(f"\n{len(results)} OK / {len(failures)} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
