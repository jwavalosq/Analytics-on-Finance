# Finance Analytics: Markets, Risk, and the SVB Lesson

A beginner friendly, story driven tour of US stock market history,
how bumpy that history was, what portfolio risk really means, and what
the failure of Silicon Valley Bank in March 2023 can teach us.

No trading strategy is sold here. No return is promised. Everything is
described from past data, with sources stated, so you can check it.

## Start here

Read the notebooks in order. Each one explains its ideas before it uses
them, and each one ends with a plain words summary.

1. 00_setup_and_data_check: what data we have, and how far back it goes.
2. 01_market_history: the long rise, bull and bear periods, by decade.
3. 02_volatility_and_drawdowns: rolling volatility, underwater charts,
   the largest falls, and the VIX.
4. 03_portfolio_risk_metrics: volatility, return per unit of risk,
   correlation, and diversification benefit, with formulas in plain words.
5. 04_svb_case_study: duration risk, held to maturity accounting, and
   the bank run of March 2023.
6. 05_recovery_score_and_era_comparison: our original metric, the
   Drawdown Recovery Score, plus a risk adjusted era comparison.

## How to run it

You need Python 3, plus the packages in requirements.txt.

```
pip install -r requirements.txt
bash scripts/download_data.sh
python scripts/download_data.py
python scripts/process_data.py
python scripts/build_notebooks.py
python scripts/run_notebooks.py
```

Note: in the original build sandbox, direct curl in
scripts/download_data.sh succeeded while Python requests intermittently
timed out on FRED. If the Python download stalls for you, use the shell
script for the FRED files and the Python script for the Yahoo file.
See BUILD_REPORT.md for the full story.

Charts live in charts/. Processed tables live in data/processed/.
A story website version lives in docs/index.html, with chart copies in
docs/charts/.

## Key findings, with exact numbers

All returns below are price returns, not total returns. Price returns
do not include reinvested dividends, so they are slightly lower than
total returns would be.

Market history:

- S and P 500 daily closes run from 93.0 on January 2, 1970 to 7,541.4
  on November 2, 2026, in the Yahoo series used here. That is about
  81.1 times the starting value, price only.
- Nasdaq Composite runs from 100.0 on February 5, 1971 to 26,184.72 on
  October 29, 2026, in the FRED series, about 261.8 times the starting
  value, price only.
- Best calendar year for the S and P 500 in this file: 1995, plus 34.1
  percent. Worst: 2008, minus 38.5 percent.
- Strongest full decade: the 1990s, compound growth about 15.1 percent
  per year. Weakest full decade: the 2000s, about minus 2.6 percent per
  year, ending lower than it started on a price basis.

Volatility and drawdowns:

- There were 8 falls of 20 percent or more from a peak in the S and P
  500 series, 1970 to 2026.
- Deepest: October 9, 2007 to March 9, 2009, down 56.78 percent, back to
  the old peak on March 28, 2013.
- Fastest deep fall: February 19, 2020 to March 23, 2020, down 33.92
  percent in about a month, recovered by August 18, 2020.
- Highest VIX close in the file: 82.69 on March 16, 2020. Highest 30 day
  rolling volatility: 85.3 percent annualized, on April 8, 2020.
- In March 2023, during the SVB week, the VIX rose only to 26.52 on
  March 13, 2023. Broad market stress was real, but it was not at 2020
  or 2008 panic levels.

Portfolio risk, November 2016 to October 2026, three US stock indexes:

- Annualized return, price only: Nasdaq 17.96 percent, S and P 500
  14.03 percent, Dow 11.36 percent. Equal mix: 14.58 percent.
- Annualized volatility: Nasdaq 22.20 percent, S and P 500 18.09
  percent, Dow 17.64 percent. Equal mix: 18.67 percent.
- Correlation of daily returns: S and P 500 with Nasdaq 0.949, S and P
  500 with Dow 0.943, Nasdaq with Dow 0.819.
- Diversification benefit: average single index volatility 19.31
  percent minus equal mix volatility 18.67 percent, equals 0.64
  percentage points. That is small, because the three indexes move
  together most of the time. Mixing similar stock indexes smooths the
  ride only a little.

Original metric: the Drawdown Recovery Score:

- Score, 0 to 100, higher is better. Score equals 100 times (1 minus
  depth as a fraction) divided by (1 plus recovery years from trough).
- Highest major fall score: the 1980 to 1982 fall, 59.5. It fell 27.11
  percent but recovered from trough in only about 2.7 months.
- 2020 fall: 46.9. 2022 fall: 32.9. 1987 fall: 25.2.
- Lowest scores: 1973 to 1974 fall, 7.6; 2007 to 2009 fall, 8.6; 2000
  to 2002 fall, 9.0. All three were 48 to 57 percent deep and took 49
  to 69 months from trough to recover.
- Risk adjusted eras: 1990s return per unit of risk 1.07, highest of
  the full decades. 1980s and 2010s: 0.75 each. 2000s: minus 0.12, the
  only negative full decade.

SVB, March 2023, from official sources:

- Total assets at failure: about 209 billion dollars.
- Held to maturity bonds at year end 2022: book value about 91 billion
  dollars, fair value about 76 billion dollars, unrealized loss about
  15.2 billion dollars, against total equity of about 16.3 billion
  dollars. The unrealized loss alone was about 16.7 percent of the book
  value of those bonds.
- On March 8, 2023, SVB sold about 21 billion dollars of available for
  sale bonds at a loss of about 1.8 billion dollars, and announced a
  capital raise of about 2.25 billion dollars.
- On March 9, 2023, depositors tried to withdraw about 42 billion
  dollars in one day, roughly one quarter of deposits.
- SVB was closed on March 10, 2023. On March 12, 2023, the Treasury,
  the Federal Reserve, and the FDIC announced that all SVB deposits,
  insured and uninsured, would be protected.
- Market context from our data: the S and P 500 fell from 100 on
  February 1, 2023 to about 93.7 on March 10, and was back to about
  99.8 by March 31. The Nasdaq was above its February 1 level by March
  31, at about 103.4. A single bank can fail fast even while the broad
  market recovers.

## A note on era drawdowns

In the era table, max drawdown means the deepest point below a prior
peak that occurred during that era, even if the fall started in an
earlier era. Example: the 2010s figure of minus 34.67 percent is the
July 2010 low point of the fall that started in 2007, not a new fall
that started in the 2010s. The drawdown episode table is the place to
see each fall with its own peak, trough, and recovery dates.

## Limits, stated honestly

- Price only, no dividends. Total returns would be higher.
- The portfolio chapter uses only three US stock indexes, so its
  diversification result does not apply to bonds, cash, or non US
  assets. Those were not in the no key downloads used here.
- The SVB bond chart in notebook 04 is illustrative math, not SVB's
  actual portfolio. It shows how longer bonds fall more when yields
  rise. SVB's exact portfolio duration is not recovered from public
  summaries in this project.
- Uninsured deposit share for SVB is reported as a range, about 88
  percent to about 94 percent, because sources differ by measure and
  date.
- Nothing here is investment advice, and no strategy is presented as
  profitable or validated.

## Sources

Market and macro data: Yahoo Finance public chart API and FRED, Federal
Reserve Bank of St. Louis. Every file and URL is listed in
data/raw/PROVENANCE.md. SVB facts: Federal Reserve review of SVB
supervision, April 2023; SVB Financial Group 10-K for year end 2022;
joint Treasury, Federal Reserve, and FDIC statement, March 12, 2023;
FDIC failed bank information.

## About the original repo

This folder is a fresh local build, not a copy of the original repo.
The original repo, github.com/jwavalosq/Analytics-on-Finance, is
described as containing Analysis_SVB.ipynb, AI-trading.py, and logs/
with MLTrader backtest outputs. No local copy of that repo was present
in this workspace, so none of those files were copied, deleted, or
overwritten here. This build follows the SVB theme of the original
notebook, but all SVB numbers were rechecked against the official
sources above. AI-trading.py is treated as a prior unverified
experiment and is not used as evidence. No backtest is claimed.

## License and use

This is a learning portfolio project. Use the code and charts with
attribution to the sources listed above. Do not present the
illustrative SVB bond math as SVB's actual portfolio, and do not
present past returns as a promise of future returns.


## Also in this repo, preserved unchanged

The original repo files sit alongside this project and were not touched: Analysis_SVB.ipynb (an earlier Silicon Valley Bank analysis), AI-trading.py, and the logs/ backtest outputs. This project builds on the SVB theme but does not replace those files.
