"""Download public, no-key market data into data/raw/.

Sources used here:
- Yahoo Finance public chart API for the S and P 500 daily close (^GSPC).
  No key, no sign-in. Price index only, no dividends.
- FRED (Federal Reserve Bank of St. Louis) public CSV downloads, no key:
  NASDAQCOM, DJIA, SP500, VIXCLS, DGS10, DGS2, FEDFUNDS, CPIAUCSL.
  FRED series pages are the source of truth for series definitions.

Stooq was tried first and is documented as a cut in BUILD_REPORT.md:
its daily CSV endpoint returned a browser verification page, not data.

Run from the project root:
    python scripts/download_data.py
"""
import json
import subprocess
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (finance-analytics portfolio build)"}


def curl_download(url, out):
    # curl is used here because, in this sandbox, it handles the egress
    # proxy reliably, while Python requests intermittently timed out on FRED.
    subprocess.run(
        ["curl", "-sL", "-A", HEADERS["User-Agent"], url, "-o", str(out)],
        check=True,
        timeout=120,
    )
    print(f"{url} -> {out.name} ({out.stat().st_size} bytes)")
    return out


def download_fred(series):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    out = RAW / f"fred_{series.lower()}.csv"
    if out.exists() and out.stat().st_size > 1000:
        print(f"{series}: already present, skipping ({out.name})")
        return out
    return curl_download(url, out)


def download_yahoo_sp500():
    # Daily closes, earliest available to the latest available day.
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC"
        "?period1=0&period2=9999999999&interval=1d"
    )
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    result = resp.json()["chart"]["result"][0]
    timestamps = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]
    volumes = result["indicators"]["quote"][0].get("volume", [None] * len(timestamps))
    import csv
    from datetime import datetime, timezone

    out = RAW / "yahoo_sp500_daily.csv"
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "close", "volume"])
        for ts, close, vol in zip(timestamps, closes, volumes):
            if close is None:
                continue
            date = datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()
            writer.writerow([date, close, vol])
    print(f"Yahoo ^GSPC: {len(timestamps)} timestamps -> {out.name}")
    return out


def main():
    for series in ["NASDAQCOM", "DJIA", "SP500", "VIXCLS", "DGS10", "DGS2", "FEDFUNDS", "CPIAUCSL"]:
        download_fred(series)
        time.sleep(1)
    download_yahoo_sp500()
    print("Done. See data/raw/PROVENANCE.md for every URL.")


if __name__ == "__main__":
    main()
