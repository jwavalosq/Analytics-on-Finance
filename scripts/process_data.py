"""Turn data/raw/ into data/processed/ tables used by every notebook.

Run from the project root:
    python scripts/process_data.py

All returns here are price returns, not total returns, because the index
series used are price indexes and do not include reinvested dividends.
That choice is stated in every notebook that uses returns.
"""
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)


def load_fred(name, col):
    df = pd.read_csv(RAW / f"fred_{name}.csv", parse_dates=["observation_date"])
    df = df.rename(columns={"observation_date": "date", name.upper(): col})
    df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=[col]).sort_values("date").reset_index(drop=True)


def load_sp500():
    df = pd.read_csv(RAW / "yahoo_sp500_daily.csv", parse_dates=["date"])
    return df.rename(columns={"close": "sp500"}).sort_values("date").reset_index(drop=True)


def drawdown_episodes(prices):
    """Split a price series into episodes from a peak until it recovers.

    An episode starts at a new running peak, falls to a trough, and ends
    on the first later date when the price reaches the old peak again.
    Episodes still open at the end of the data are marked recovered=False.
    """
    peak = prices.cummax()
    dd = prices / peak - 1.0
    episodes = []
    in_episode = False
    start = trough = None
    trough_value = 1.0
    for i, (date, price, d) in enumerate(zip(prices.index, prices.values, dd.values)):
        # prices.index here is the date column after reset, handled by caller
        pass
    return episodes


def episodes_from_frame(df, price_col="sp500"):
    prices = df[price_col].values
    dates = pd.to_datetime(df["date"]).values
    peak_val = prices[0]
    peak_date = dates[0]
    in_ep = False
    ep_peak = ep_peak_date = None
    ep_trough = None
    ep_trough_date = None
    ep_trough_dd = 0.0
    out = []
    for price, date in zip(prices, dates):
        if price >= peak_val:
            if in_ep:
                out.append(
                    {
                        "peak_date": pd.Timestamp(ep_peak_date).date().isoformat(),
                        "trough_date": pd.Timestamp(ep_trough_date).date().isoformat(),
                        "recovery_date": pd.Timestamp(date).date().isoformat(),
                        "depth_pct": round(float(ep_trough_dd * 100), 2),
                        "recovered": True,
                    }
                )
                in_ep = False
            peak_val = price
            peak_date = date
        else:
            dd = price / peak_val - 1.0
            if not in_ep:
                in_ep = True
                ep_peak = peak_val
                ep_peak_date = peak_date
                ep_trough = price
                ep_trough_date = date
                ep_trough_dd = dd
            elif dd < ep_trough_dd:
                ep_trough = price
                ep_trough_date = date
                ep_trough_dd = dd
    if in_ep:
        out.append(
            {
                "peak_date": pd.Timestamp(ep_peak_date).date().isoformat(),
                "trough_date": pd.Timestamp(ep_trough_date).date().isoformat(),
                "recovery_date": "",
                "depth_pct": round(float(ep_trough_dd * 100), 2),
                "recovered": False,
            }
        )
    return pd.DataFrame(out)


def recovery_score(depth_pct, recovery_months):
    """Original metric for this project: Drawdown Recovery Score, 0 to 100.

    Plain words: a fall scores higher when it is shallow and when it
    recovers fast. Depth factor is (1 minus depth as a fraction).
    Speed factor is 1 divided by (1 plus recovery years).
    Score is 100 times depth factor times speed factor.
    A 20 percent fall recovered in 6 months scores about 53.
    A 50 percent fall recovered in 60 months scores about 8.
    Unrecovered episodes get no score, shown as blank.
    """
    if recovery_months is None or (isinstance(recovery_months, float) and math.isnan(recovery_months)):
        return np.nan
    depth = abs(depth_pct) / 100.0
    return round(100 * (1 - depth) / (1 + recovery_months / 12.0), 1)


def main():
    sp = load_sp500()
    nasdaq = load_fred("nasdaqcom", "nasdaq")
    vix = load_fred("vixcls", "vix")
    dgs10 = load_fred("dgs10", "yield_10y")
    dgs2 = load_fred("dgs2", "yield_2y")
    fedfunds = load_fred("fedfunds", "fedfunds")
    cpi = load_fred("cpiaucsl", "cpi")

    sp = sp[["date", "sp500"]].copy()
    sp["return"] = sp["sp500"].pct_change()
    sp["rolling_vol_30d"] = sp["return"].rolling(30).std() * np.sqrt(252)
    sp["running_peak"] = sp["sp500"].cummax()
    sp["drawdown"] = sp["sp500"] / sp["running_peak"] - 1.0
    sp.to_csv(PROC / "sp500_daily.csv", index=False)

    # Annual and decade tables
    yearly = sp.set_index("date")["sp500"].resample("A").last()
    annual = pd.DataFrame({"year": yearly.index.year, "year_end_close": yearly.values})
    annual["annual_return_pct"] = annual["year_end_close"].pct_change() * 100
    annual.to_csv(PROC / "sp500_annual.csv", index=False)

    decades = []
    for label, start, end in [
        ("1970s (partial, from 1970)", "1970-01-02", "1979-12-31"),
        ("1980s", "1980-01-01", "1989-12-31"),
        ("1990s", "1990-01-01", "1999-12-31"),
        ("2000s", "2000-01-01", "2009-12-31"),
        ("2010s", "2010-01-01", "2019-12-31"),
        ("2020s (partial, to 2026)", "2020-01-01", "2026-11-02"),
    ]:
        sub = sp[(sp["date"] >= start) & (sp["date"] <= end)]
        if len(sub) < 10:
            continue
        rets = sub["return"].dropna()
        years = (sub["date"].iloc[-1] - sub["date"].iloc[0]).days / 365.25
        cagr = (sub["sp500"].iloc[-1] / sub["sp500"].iloc[0]) ** (1 / years) - 1 if years > 0 else np.nan
        vol = rets.std() * np.sqrt(252)
        decades.append(
            {
                "era": label,
                "start_close": round(float(sub["sp500"].iloc[0]), 2),
                "end_close": round(float(sub["sp500"].iloc[-1]), 2),
                "cagr_pct": round(float(cagr * 100), 2),
                "annual_vol_pct": round(float(vol * 100), 2),
                "return_per_unit_risk": round(float(cagr / vol), 2) if vol else np.nan,
                "max_drawdown_pct": round(float(sub["drawdown"].min() * 100), 2),
                "n_trading_days": len(sub),
            }
        )
    pd.DataFrame(decades).to_csv(PROC / "sp500_by_era.csv", index=False)

    # Drawdown episodes, major only
    eps = episodes_from_frame(sp, "sp500")
    eps["peak_date_dt"] = pd.to_datetime(eps["peak_date"])
    eps["trough_date_dt"] = pd.to_datetime(eps["trough_date"])
    eps["recovery_date_dt"] = pd.to_datetime(eps["recovery_date"], errors="coerce")
    eps["decline_months"] = ((eps["trough_date_dt"] - eps["peak_date_dt"]).dt.days / 30.44).round(1)
    eps["recovery_months"] = ((eps["recovery_date_dt"] - eps["trough_date_dt"]).dt.days / 30.44).round(1)
    eps["total_months"] = ((eps["recovery_date_dt"] - eps["peak_date_dt"]).dt.days / 30.44).round(1)
    eps["recovery_score"] = [
        recovery_score(d, m) if rec else np.nan
        for d, m, rec in zip(eps["depth_pct"], eps["recovery_months"], eps["recovered"])
    ]
    major = eps[eps["depth_pct"] <= -20].copy()
    major = major.sort_values("depth_pct")
    major.drop(columns=["peak_date_dt", "trough_date_dt", "recovery_date_dt"]).to_csv(
        PROC / "sp500_major_drawdowns.csv", index=False
    )
    eps.drop(columns=["peak_date_dt", "trough_date_dt", "recovery_date_dt"]).to_csv(
        PROC / "sp500_all_drawdown_episodes.csv", index=False
    )

    # Nasdaq long series and rebased comparison
    merged = pd.merge(sp[["date", "sp500"]], nasdaq, on="date", how="inner")
    merged["sp500_rebased"] = merged["sp500"] / merged["sp500"].iloc[0] * 100
    merged["nasdaq_rebased"] = merged["nasdaq"] / merged["nasdaq"].iloc[0] * 100
    merged.to_csv(PROC / "sp500_nasdaq_daily.csv", index=False)

    # Volatility and VIX context
    vix_m = vix.copy()
    vix_m.to_csv(PROC / "vix_daily.csv", index=False)
    vix_monthly_max = vix.set_index("date")["vix"].resample("M").max().reset_index()
    vix_monthly_max.to_csv(PROC / "vix_monthly_max.csv", index=False)

    # Rates context
    rates = pd.merge(dgs10, dgs2, on="date", how="outer").sort_values("date")
    rates["spread_10y_minus_2y"] = rates["yield_10y"] - rates["yield_2y"]
    rates.to_csv(PROC / "rates_daily.csv", index=False)
    fedfunds.to_csv(PROC / "fedfunds_monthly.csv", index=False)
    cpi.to_csv(PROC / "cpi_monthly.csv", index=False)

    # Portfolio window: FRED SP500, Nasdaq, Dow, overlapping from Nov 2016
    fred_sp = load_fred("sp500", "fred_sp500")
    fred_dow = load_fred("djia", "fred_dow")
    port = fred_sp.merge(nasdaq, on="date", how="inner").merge(fred_dow, on="date", how="inner")
    port = port.sort_values("date").reset_index(drop=True)
    for col in ["fred_sp500", "nasdaq", "fred_dow"]:
        port[col + "_ret"] = port[col].pct_change()
    port.to_csv(PROC / "portfolio_inputs_daily.csv", index=False)

    # SVB window: Feb 1 to Mar 31 2023, rebased
    window = merged[(merged["date"] >= "2023-02-01") & (merged["date"] <= "2023-03-31")].copy()
    window["sp500_rebased_feb1"] = window["sp500"] / window["sp500"].iloc[0] * 100
    window["nasdaq_rebased_feb1"] = window["nasdaq"] / window["nasdaq"].iloc[0] * 100
    window.to_csv(PROC / "svb_window_markets.csv", index=False)

    # Rates window 2020 to 2023 for the SVB chapter
    rates_window = rates[(rates["date"] >= "2020-01-01") & (rates["date"] <= "2023-12-31")].copy()
    rates_window.to_csv(PROC / "svb_window_rates.csv", index=False)

    print(f"S&P 500 rows: {len(sp)}, {sp['date'].min().date()} to {sp['date'].max().date()}")
    print(f"Major drawdowns (20 pct or more): {len(major)}")
    print(major[["peak_date", "trough_date", "recovery_date", "depth_pct", "recovery_score"]].to_string(index=False))
    print(f"Portfolio window rows: {len(port)}, {port['date'].min().date()} to {port['date'].max().date()}")


if __name__ == "__main__":
    main()
