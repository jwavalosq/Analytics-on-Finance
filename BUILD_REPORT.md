# Build Report: Finance Analytics, Markets, Risk, and the SVB Lesson

Built locally only. Nothing was published, pushed, posted, or signed
into. No GitHub repository was created, no remote was added, and no
account was used.

Build date: November 2 to 3, 2026. Folder:
~/workspace/repo-builds/finance-analytics/

## What ran successfully

All 6 notebooks were executed end to end with jupyter nbconvert, using
the project venv at ~/.venvs/elections, and finished with zero cell
errors. Each notebook starts with a pip install cell.

| Notebook | Cells | Result |
|---|---|---|
| 00_setup_and_data_check.ipynb | 7 | 14 processed files checked. S and P 500 1970-01-02 to 2026-11-02. Chart: 00_data_coverage.png |
| 01_market_history.ipynb | 8 | Era table, log scale chart, rebased comparison, decade chart. Charts: 01_sp500_log.png, 01_sp500_vs_nasdaq.png, 01_decade_cagr.png |
| 02_volatility_and_drawdowns.ipynb | 9 | 8 major drawdowns found. Charts: 02_rolling_vol.png, 02_drawdown_underwater.png, 02_major_drawdowns.png, 02_vix.png |
| 03_portfolio_risk_metrics.ipynb | 10 | Portfolio window 2016-11-03 to 2026-10-29, 2,509 daily returns. Charts: 03_risk_return.png, 03_correlation.png, 03_diversification.png, 03_portfolio_cumulative.png |
| 04_svb_case_study.ipynb | 8 | Sourced SVB facts table, rates chart, illustrative bond chart, SVB week market chart. Charts: 04_rates_2020_2023.png, 04_illustrative_bond.png, 04_market_svb_window.png |
| 05_recovery_score_and_era_comparison.ipynb | 7 | Recovery Score for all 8 major falls, era risk table. Charts: 05_recovery_score.png, 05_era_risk_adjusted.png |

Total: 6 notebooks, 17 charts in charts/, plus copies in docs/charts/.

## Every dataset used, with its URL

See data/raw/PROVENANCE.md for the full table. Summary:

- yahoo_sp500_daily.csv: Yahoo Finance public chart API, ^GSPC daily.
  https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?period1=0&period2=9999999999&interval=1d
  14,331 rows, 1970-01-02 to 2026-11-02.
- fred_nasdaqcom.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=NASDAQCOM
- fred_sp500.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500
- fred_djia.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=DJIA
- fred_vixcls.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS
- fred_dgs10.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10
- fred_dgs2.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2
- fred_fedfunds.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS
- fred_cpiaucsl.csv: https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL

Processed tables in data/processed/:

sp500_daily.csv, sp500_annual.csv, sp500_by_era.csv,
sp500_major_drawdowns.csv, sp500_all_drawdown_episodes.csv,
sp500_nasdaq_daily.csv, vix_daily.csv, vix_monthly_max.csv,
rates_daily.csv, fedfunds_monthly.csv, cpi_monthly.csv,
portfolio_inputs_daily.csv, svb_window_markets.csv,
svb_window_rates.csv.

Scripts:

- scripts/download_data.py: Python downloader, FRED via curl subprocess
  plus Yahoo via requests.
- scripts/download_data.sh: shell downloader for FRED files, the path
  actually tested in this sandbox. See failures below.
- scripts/process_data.py: builds every processed table above.
- scripts/build_notebooks.py: builds all 6 notebooks from scratch.
- scripts/run_notebooks.py: executes all notebooks in order and fails
  if any cell errors.

## Key verified numbers

These are computed from the downloaded data, except SVB facts, which
are sourced as noted:

- S and P 500: 93.0 on 1970-01-02 to 7,541.4 on 2026-11-02, price only.
- Nasdaq: 100.0 on 1971-02-05 to 26,184.72 on 2026-10-29, price only.
- Best year 1995 plus 34.11 percent, worst year 2008 minus 38.49 percent.
- 1990s CAGR 15.12 percent, 2000s CAGR minus 2.63 percent.
- Deepest drawdown: 2007-10-09 to 2009-03-09, minus 56.78 percent,
  recovered 2013-03-28. Recovery Score 8.6.
- 2020 drawdown: minus 33.92 percent, recovered in 4.9 months from
  trough, Recovery Score 46.9.
- Highest Recovery Score: 1980 to 1982 fall, 59.5, depth minus 27.11
  percent, trough to recovery about 2.7 months.
- VIX max: 82.69 on 2020-03-16. VIX on 2023-03-13: 26.52.
- Portfolio window: correlations 0.949, 0.943, 0.819. Equal mix vol
  18.67 percent, average single vol 19.31 percent, diversification
  benefit 0.64 percentage points.
- SVB: assets about 209 billion dollars, HTM book about 91 billion,
  HTM fair value about 76 billion, unrealized loss about 15.2 billion,
  equity about 16.3 billion, AFS sale about 21 billion at a loss of
  about 1.8 billion, capital raise about 2.25 billion, March 9
  withdrawals about 42 billion, closed March 10, 2023, all deposits
  protected March 12, 2023.
- Rates in FRED data: 10 year yield low 0.52 percent on 2020-08-04,
  3.98 percent on 2023-03-08, 3.70 percent on 2023-03-10.

## Failures, approximations, and honest cuts

1. Stooq was tried first and failed. Its daily CSV endpoint returned
   a browser verification page, not data, so no Stooq file is used.
   Yahoo Finance chart API and FRED replaced it, both public and no
   key. This is documented in scripts/download_data.py.
2. Python downloads were flaky in this sandbox. Python requests timed
   out on FRED, and a Python subprocess curl call also timed out, while
   direct curl from the shell succeeded in seconds for the same URLs.
   The FRED files in data/raw/ were therefore downloaded with direct
   curl commands, identical to scripts/download_data.sh. The Python
   script is kept for rebuilds outside this sandbox, with the shell
   script as the tested path. Yahoo data was downloaded successfully
   with Python requests.
3. FRED SP500 and DJIA downloads only return a recent window, from
   November 3, 2016 onward, in the fredgraph.csv form used here. They
   are therefore used only for the portfolio window and as a cross
   check, not for long history. Long S and P 500 history comes from
   Yahoo, and long Nasdaq history comes from FRED NASDAQCOM, which
   does go back to 1971.
4. Old pandas in the system Python does not accept YE or ME resample
   codes. scripts/process_data.py was fixed to use A and M, which work
   in both old and new pandas. The venv used for notebooks has newer
   pandas, but the processed tables were built with the system Python
   and are version neutral CSVs.
5. Era max drawdown is defined as the deepest point below a prior peak
   during that era, not necessarily a fall that started in that era.
   Example: 2010s minus 34.67 percent is the July 2010 point of the
   2007 fall. The episode table gives each fall its own dates.
6. Returns are price returns only, no dividends. This understates total
   returns and is stated in every notebook, in README.md, and here.
7. Return per unit of risk in notebooks 03 and 05 is a Sharpe style
   measure, not a formal Sharpe ratio, because no safe rate is
   subtracted. The notebooks say this in plain words.
8. The SVB bond chart is illustrative only. It uses the formula price
   change about minus duration times yield change, for durations 2, 5,
   8, and 12 years at a 3 point yield rise. It is not SVB's actual
   portfolio, and SVB's exact duration is not recovered here.
9. SVB uninsured deposit share is reported as a range, about 88 percent
   to about 94 percent, because sources differ by measure and date.
   No single exact figure is claimed.
10. No bond price series, no non US series, and no individual stock
    series were added, because the no key sources that worked reliably
    here were index and rate series. The portfolio chapter is therefore
    limited to three US stock indexes, and that limit is stated as a
    finding, not hidden.
11. CPI was downloaded but is not used in the main charts. It is kept
    in data/raw/ and data/processed/ for a future inflation adjusted
    version. No inflation adjusted return is claimed in this build.
12. Original repo files were not present locally. Analysis_SVB.ipynb,
    AI-trading.py, and logs/ were not copied, deleted, or overwritten.
    AI-trading.py was not run and not used as evidence. No MLTrader
    backtest is reproduced. No trading strategy is presented as
    profitable or validated anywhere in this project.

## What was cut, and why

- Stooq daily index downloads: cut, verification page blocked the CSV.
- A bond total return portfolio: cut, no reliable no key bond price
  series was found in the time available. Rates are used as context
  instead, and the limit is stated.
- A map or geographic cut: cut, not relevant to market and bank risk
  data, and no map would add evidence here.
- Any backtest of AI-trading.py: cut on purpose, the script is
  unverified and the task requires not presenting unverified trading
  as evidence.

## What still needs the user, if this is ever published

Nothing except publishing access, which was explicitly excluded. To
publish, the user would need to create the repo or grant access, copy
this folder alongside the original Analysis_SVB.ipynb, AI-trading.py,
and logs/ files (not overwriting them), and enable GitHub Pages for
docs/. The docs/index.html file is already written in GitHub Pages
story style, with chart copies in docs/charts/, so that step is only
a copy and a Pages setting, not a rebuild.

## Rebuild steps

```
pip install -r requirements.txt
bash scripts/download_data.sh
python scripts/download_data.py
python scripts/process_data.py
python scripts/build_notebooks.py
python scripts/run_notebooks.py
```

Note: scripts/build_notebooks.py overwrites the notebooks in
notebooks/ with fresh, unexecuted versions. Run
scripts/run_notebooks.py after it to re-execute them and regenerate
charts/. If you only want to re-execute without rebuilding, run
scripts/run_notebooks.py alone.
