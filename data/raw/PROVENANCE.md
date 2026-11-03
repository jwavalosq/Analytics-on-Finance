# Data provenance

Every file in this folder, where it came from, and what it covers.
All downloads are public and need no key and no sign-in.
Download date for this build: November 2 to 3, 2026.

## Market and macro series

| File | Source | URL | Coverage in this download |
|---|---|---|---|
| yahoo_sp500_daily.csv | Yahoo Finance public chart API, S and P 500 (^GSPC), daily close, price only, no dividends | https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?period1=0&period2=9999999999&interval=1d | 1970-01-02 to 2026-11-02, 14,331 rows |
| fred_nasdaqcom.csv | FRED, Nasdaq Composite, series NASDAQCOM, Federal Reserve Bank of St. Louis | https://fred.stlouisfed.org/graph/fredgraph.csv?id=NASDAQCOM | 1971-02-05 to 2026-10-29, 14,539 rows |
| fred_sp500.csv | FRED, S and P 500, series SP500 | https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500 | 2016-11-03 to 2026-10-30, 2,607 rows. Note: this FRED download only returns the recent window, so it is used only as a cross check and for the portfolio window, not for long history. Long S and P 500 history comes from Yahoo above. |
| fred_djia.csv | FRED, Dow Jones Industrial Average, series DJIA | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DJIA | 2016-11-03 to 2026-11-02, 2,608 rows. Same recent window limit as FRED SP500. |
| fred_vixcls.csv | FRED, Cboe Volatility Index, series VIXCLS | https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS | 1990-01-02 to 2026-10-30, 9,609 rows |
| fred_dgs10.csv | FRED, 10 year Treasury constant maturity rate, series DGS10 | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10 | 1962-01-02 to 2026-10-30, 16,914 rows |
| fred_dgs2.csv | FRED, 2 year Treasury constant maturity rate, series DGS2 | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2 | 1976-06-01 to 2026-10-30, 13,154 rows |
| fred_fedfunds.csv | FRED, effective federal funds rate, monthly, series FEDFUNDS | https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS | 1954-07-01 to 2026-10-01, 868 rows |
| fred_cpiaucsl.csv | FRED, Consumer Price Index for All Urban Consumers, monthly, series CPIAUCSL | https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL | 1947-01-01 to 2026-09-01, 957 rows. Downloaded for context, not used in the main charts. |

## SVB facts, not market downloads

The SVB numbers in notebook 04 are a sourced facts table, not a
downloaded market series. Sources:

- Board of Governors of the Federal Reserve System, Review of the
  Federal Reserve's Supervision and Regulation of Silicon Valley Bank,
  April 2023. https://www.federalreserve.gov/publications/files/svb-review-20230428.pdf
- SVB Financial Group annual report (Form 10-K) for year end 2022,
  held to maturity figures as summarized in the Federal Reserve review
  and in a Council of Institutional Investors comment letter to FASB,
  April 27, 2023. HTM book value about 91 billion dollars, fair value
  about 76 billion dollars, unrealized loss about 15.2 billion dollars,
  total equity about 16.3 billion dollars.
- Joint statement by the Department of the Treasury, the Federal
  Reserve, and the FDIC, March 12, 2023, protecting all SVB deposits.
- FDIC failed bank information and contemporaneous reporting for the
  March 9, 2023 withdrawal figure of about 42 billion dollars and the
  March 10, 2023 closure date.

Uninsured deposit share: sources differ by measure and date, from about
88 percent to about 94 percent. This project reports that range and
does not pick a single exact figure.

## Original repo files, not downloaded here

The original repo, github.com/jwavalosq/Analytics-on-Finance, is
described in the task as containing Analysis_SVB.ipynb, AI-trading.py,
and logs/ with MLTrader backtest outputs. No local copy of that repo
was present in this workspace, so none of those files were copied,
deleted, or overwritten in this fresh folder. This build is meant to
sit alongside them, not replace them. AI-trading.py is treated as a
prior unverified experiment and is not used as evidence anywhere in
this project. No backtest from logs/ is reproduced or claimed.
