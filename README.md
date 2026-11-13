# Finance Analytics: Markets, Risk, and the SVB Lesson

Read the story version on the live site: https://jwavalosq.github.io/Analytics-on-Finance/

## The question I started with

I wanted to understand how the US stock market really behaves over a long stretch of time. Not just that it goes up, but how rough the ride is, what risk actually means for a portfolio, and what a real bank failure can teach us about that risk. I started with the failure of Silicon Valley Bank in March 2023, and I worked backward from there into fifty years of market history.

## Why it matters

Most people hear that stocks go up over time, and they do, on a price basis. What they do not hear is how far the market can fall along the way, how long it can take to come back, or how little comfort a mix of similar stock funds really gives you when everything falls together. If you are saving for a wedding, a baby, or retirement, those are the numbers that decide whether you can stay calm and stay invested. This project is my attempt to make those numbers plain, with sources you can check.

## What I did

I built the project in six notebooks, in order, using public data that needs no key and no sign in. Market and macro data came from the Yahoo Finance public chart API and from FRED, the Federal Reserve Bank of St. Louis. The Silicon Valley Bank facts came from official sources, not from headlines.

1. **00, setup and data check.** I checked what data I had and how far back it went.
2. **01, market history.** I charted the long rise, bull and bear periods, by decade.
3. **02, volatility and drawdowns.** I measured bumpiness, the largest falls, and the VIX.
4. **03, portfolio risk metrics.** I measured volatility, return per unit of risk, correlation, and diversification benefit, with every formula explained in plain words.
5. **04, the SVB case study.** I walked through duration risk, held to maturity accounting, and the bank run of March 2023.
6. **05, recovery score and era comparison.** I built my own metric, the Drawdown Recovery Score, and compared eras on a risk adjusted basis.

All 6 notebooks ran end to end with zero cell errors. The project has 17 charts. Charts live in `charts/`, processed tables live in `data/processed/`, and the story website version lives in `docs/index.html`, with chart copies in `docs/charts/`.

## What I found

All returns below are price returns, not total returns. Price returns do not include reinvested dividends, so they are slightly lower than total returns would be.

**The long rise was real, and it was not smooth.** The S and P 500 went from 93.0 on January 2, 1970 to 7,541.4 on November 2, 2026, price only, about 81.1 times the starting value. The Nasdaq Composite went from 100.0 on February 5, 1971 to 26,184.72 on October 29, 2026, about 261.8 times the starting value. The best calendar year for the S and P 500 in this file was 1995, plus 34.1 percent. The worst was 2008, minus 38.5 percent. The strongest full decade was the 1990s, growing about 15.1 percent per year. The weakest was the 2000s, about minus 2.6 percent per year, ending lower than it started on a price basis.

**Falls are part of the story, not exceptions to it.** There were 8 falls of 20 percent or more from a peak in the S and P 500 series, 1970 to 2026. The deepest was October 9, 2007 to March 9, 2009, down 56.78 percent, back to the old peak on March 28, 2013. The fastest deep fall was February 19, 2020 to March 23, 2020, down 33.92 percent in about a month, recovered by August 18, 2020. The highest VIX close in the file was 82.69 on March 16, 2020. In March 2023, during the SVB week, the VIX rose only to 26.52 on March 13, 2023. Broad market stress was real, but it was not at 2020 or 2008 panic levels.

**Mixing similar stock indexes smooths the ride only a little.** From November 2016 to October 2026, using the S and P 500, Nasdaq, and Dow, correlations of daily returns were high: S and P 500 with Nasdaq 0.949, S and P 500 with Dow 0.943, Nasdaq with Dow 0.819. Annualized return, price only, was Nasdaq 17.96 percent, S and P 500 14.03 percent, Dow 11.36 percent, and an equal mix 14.58 percent. The equal mix volatility was 18.67 percent, against an average single index volatility of 19.31 percent. That is a diversification benefit of only 0.64 percentage points. The three indexes move together most of the time, so mixing them helps less than people often assume.

**I built one original metric to compare falls fairly: the Drawdown Recovery Score.** The score runs 0 to 100, higher is better. It equals 100 times (1 minus depth as a fraction) divided by (1 plus recovery years from trough). It rewards shallow falls and fast recoveries, and it punishes deep falls that take years to heal. The highest major fall score was the 1980 to 1982 fall, 59.5. It fell 27.11 percent but recovered from trough in only about 2.7 months. The 2020 fall scored 46.9. The lowest scores were the 1973 to 1974 fall, 7.6, the 2007 to 2009 fall, 8.6, and the 2000 to 2002 fall, 9.0. All three were 48 to 57 percent deep and took 49 to 69 months from trough to recover. On risk adjusted eras, the 1990s scored 1.07 return per unit of risk, the highest of the full decades. The 1980s and 2010s scored 0.75 each. The 2000s scored minus 0.12, the only negative full decade. Raw growth alone hides the cost of getting there.

**The SVB lesson is about two risks meeting at once.** Silicon Valley Bank held about 91 billion dollars of held to maturity bonds at book value at year end 2022, worth about 76 billion dollars at market prices. The unrealized loss was about 15.2 billion dollars, against total equity of about 16.3 billion dollars. When rates rose, the 10 year Treasury yield in my FRED data went from a low of 0.52 percent in August 2020 to 3.98 percent on March 8, 2023, those long bonds lost value. On March 8, 2023, SVB sold about 21 billion dollars of available for sale bonds at a loss of about 1.8 billion dollars, and announced a capital raise of about 2.25 billion dollars. On March 9, 2023, depositors tried to withdraw about 42 billion dollars in one day, roughly one quarter of deposits. SVB was closed on March 10, 2023. On March 12, 2023, the Treasury, the Federal Reserve, and the FDIC announced that all SVB deposits, insured and uninsured, would be protected. The broad market told a different story from the bank itself: the S and P 500 fell from 100 on February 1, 2023 to about 93.7 on March 10, and was back to about 99.8 by March 31. A single bank can fail fast even while the broad market recovers.

## What it means, and who it helps

If you are learning investing, this project gives you the long view in plain language: growth is real, falls are normal, recovery times vary a lot, and diversification only helps when the things you mix actually behave differently. If you work in risk, banking, or analytics, the SVB chapter and the Recovery Score give you a concrete case and a simple way to compare falls across eras. Nothing here tells you what to buy. It tells you what happened, so you can ask better questions before you decide.

## How to run it yourself

You need Python 3, plus the packages in `requirements.txt`.

```bash
pip install -r requirements.txt
bash scripts/download_data.sh
python scripts/download_data.py
python scripts/process_data.py
python scripts/build_notebooks.py
python scripts/run_notebooks.py
```

Note: in the original build, direct curl in `scripts/download_data.sh` succeeded while Python requests intermittently timed out on FRED. If the Python download stalls for you, use the shell script for the FRED files and the Python script for the Yahoo file. See `BUILD_REPORT.md` for the full story, and `data/raw/PROVENANCE.md` for every file and URL.

## What the limits are, stated honestly

- Price only, no dividends. Total returns would be higher.
- The portfolio chapter uses only three US stock indexes, so its diversification result does not apply to bonds, cash, or non US assets. Those were not in the no key downloads used here.
- The SVB bond chart in notebook 04 is illustrative math, not SVB's actual portfolio. It shows how longer bonds fall more when yields rise. SVB's exact portfolio duration is not recovered from public summaries in this project.
- Uninsured deposit share for SVB is reported as a range, about 88 percent to about 94 percent, because sources differ by measure and date.
- Return per unit of risk in notebooks 03 and 05 is a Sharpe style measure, not a formal Sharpe ratio, because no safe rate is subtracted. The notebooks say this in plain words.
- In the era table, max drawdown means the deepest point below a prior peak that occurred during that era, even if the fall started in an earlier era. Example: the 2010s figure of minus 34.67 percent is the July 2010 low point of the fall that started in 2007, not a new fall that started in the 2010s. The drawdown episode table is the place to see each fall with its own peak, trough, and recovery dates.
- CPI was downloaded but is not used in the main charts. No inflation adjusted return is claimed in this project.
- Nothing here is investment advice, and no strategy is presented as profitable or validated.

## Sources

Market and macro data: Yahoo Finance public chart API and FRED, Federal Reserve Bank of St. Louis. Every file and URL is listed in `data/raw/PROVENANCE.md`. SVB facts: Federal Reserve review of SVB supervision, April 2023; SVB Financial Group 10-K for year end 2022; joint Treasury, Federal Reserve, and FDIC statement, March 12, 2023; FDIC failed bank information.

## Also in this repo, preserved unchanged

The original repo files sit alongside this project and were not touched: `Analysis_SVB.ipynb` (an earlier Silicon Valley Bank analysis), `AI-trading.py`, and the `logs/` backtest outputs. This project builds on the SVB theme but does not replace those files. `AI-trading.py` is treated as a prior unverified experiment and is not used as evidence. No backtest from `logs/` is reproduced or claimed.

## License and use

This is a learning portfolio project. Use the code and charts with attribution to the sources listed above. Do not present the illustrative SVB bond math as SVB's actual portfolio, and do not present past returns as a promise of future returns.
