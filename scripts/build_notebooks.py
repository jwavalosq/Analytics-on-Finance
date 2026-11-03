"""Build the six notebooks in notebooks/ from the processed tables.

Run from the project root:
    python scripts/build_notebooks.py

Each notebook starts with a pip install cell, as required, and then
loads only files from data/processed/. No notebook downloads data live,
so a rerun is reproducible from the saved tables.
"""
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks"
NB.mkdir(parents=True, exist_ok=True)

PIP = "%pip install -q pandas numpy matplotlib"
SETUP = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.grid"] = True
ROOT = Path("..").resolve()
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)
PROC = ROOT / "data" / "processed"
print("Charts will be saved to:", CHARTS)
"""


def nb(cells):
    out = nbf.v4.new_notebook()
    out.cells = cells
    out.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    }
    return out


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def save(name, cells):
    path = NB / name
    nbf.write(nb(cells), str(path))
    print("Wrote", name, "with", len(cells), "cells")


# ---------------------------------------------------------------- 00
save(
    "00_setup_and_data_check.ipynb",
    [
        code(PIP),
        md(
            """
# 00. Setup and data check

Welcome. This project is about markets, risk, and one famous bank failure.
We start slow. First we check that the data is really here, and we learn
what each series means, before we draw any conclusions.

## Words we will use

A price index is a number that tracks a group of stocks. When the index
goes up, the group as a whole went up. The S and P 500 tracks 500 large
US companies. The Nasdaq Composite tracks companies listed on the Nasdaq
exchange, with a heavy weight in technology.

A return is a change in percent. If a price moves from 100 to 110, the
return is 10 percent. In this project, returns are price returns only.
They do not include dividends, which are cash payments companies make
to shareholders. So our returns are slightly lower than a total return
that reinvests dividends. We say this plainly so nobody overstates the result.

## What this notebook does

It loads every processed table, prints the first and last date of each
series, counts the rows, and saves one small chart that shows how long
each series runs. If a series were missing, we would see it here, not
three notebooks later.
"""
        ),
        code(SETUP),
        code(
            """
import os
files = sorted((PROC).glob("*.csv"))
rows = []
for f in files:
    df = pd.read_csv(f)
    date_col = "date" if "date" in df.columns else None
    first = str(df[date_col].iloc[0]) if date_col else ""
    last = str(df[date_col].iloc[-1]) if date_col else ""
    rows.append({"file": f.name, "rows": len(df), "first": first, "last": last})
check = pd.DataFrame(rows)
print(check.to_string(index=False))
print()
print("Files checked:", len(check))
"""
        ),
        code(
            """
sp = pd.read_csv(PROC / "sp500_daily.csv", parse_dates=["date"])
nasdaq = pd.read_csv(PROC / "sp500_nasdaq_daily.csv", parse_dates=["date"])
print("S and P 500: from", sp["date"].min().date(), "to", sp["date"].max().date())
print("S and P 500 first close:", sp["sp500"].iloc[0], " last close:", round(sp["sp500"].iloc[-1], 2))
print("Nasdaq first value in the joint file:", nasdaq["nasdaq"].iloc[0], " last:", nasdaq["nasdaq"].iloc[-1])
print("Total growth, S and P 500 price only:", round(sp["sp500"].iloc[-1] / sp["sp500"].iloc[0], 2), "times the starting value")
print("Total growth, Nasdaq price only:", round(nasdaq["nasdaq"].iloc[-1] / nasdaq["nasdaq"].iloc[0], 2), "times the starting value")
"""
        ),
        code(
            """
fig, ax = plt.subplots(figsize=(10, 4))
labels = ["S and P 500 daily", "Nasdaq daily", "VIX daily", "10 year yield daily", "Fed funds monthly"]
starts = [1970, 1971, 1990, 1962, 1954]
ends = [2026, 2026, 2026, 2026, 2026]
for i, (lab, s, e) in enumerate(zip(labels, starts, ends)):
    ax.barh(lab, e - s, left=s, height=0.5)
ax.set_xlabel("Year")
ax.set_title("How far back each main series goes")
plt.tight_layout()
plt.savefig(CHARTS / "00_data_coverage.png", dpi=150)
plt.show()
print("Saved charts/00_data_coverage.png")
"""
        ),
        md(
            """
## What we learned

The S and P 500 daily series starts in 1970 and the Nasdaq series starts
in 1971, so the long history chapter can cover more than 50 years. The
VIX, which measures expected market swings, starts in 1990. The 10 year
Treasury yield starts in 1962. Nothing here is a forecast. We are only
describing what already happened.
"""
        ),
    ],
)

# ---------------------------------------------------------------- 01
save(
    "01_market_history.ipynb",
    [
        code(PIP),
        md(
            """
# 01. Market history: bull and bear periods

A bull market is a long rise. A bear market is a long fall, usually
defined as a fall of 20 percent or more from a peak. Neither word is a
promise. They are labels we put on the past after we see the shape.

In this notebook we plot the S and P 500 on a log scale. A log scale is
a chart where equal distances mean equal percent changes, not equal
dollar changes. That matters because the index went from about 93 in
1970 to over 7,500 in 2026. On a normal scale, the early years would look
flat even when they moved a lot in percent terms. On a log scale, a 10
percent move looks the same size in 1975 and in 2025.

We also rebase two indexes to 100 at the start. Rebasing means dividing
every value by the first value and multiplying by 100. Both series then
start at 100, so we can compare their growth even though their starting
levels are very different.
"""
        ),
        code(SETUP),
        code(
            """
sp = pd.read_csv(PROC / "sp500_daily.csv", parse_dates=["date"])
both = pd.read_csv(PROC / "sp500_nasdaq_daily.csv", parse_dates=["date"])
annual = pd.read_csv(PROC / "sp500_annual.csv")
era = pd.read_csv(PROC / "sp500_by_era.csv")
print(era.to_string(index=False))
print()
print("Best calendar year in the file:")
print(annual.loc[annual["annual_return_pct"].idxmax()].to_string())
print()
print("Worst calendar year in the file:")
print(annual.loc[annual["annual_return_pct"].idxmin()].to_string())
"""
        ),
        code(
            """
fig, ax = plt.subplots()
ax.plot(sp["date"], sp["sp500"])
ax.set_yscale("log")
ax.set_ylabel("S and P 500 close (log scale)")
ax.set_title("S and P 500, 1970 to 2026, log scale, price only")
plt.tight_layout()
plt.savefig(CHARTS / "01_sp500_log.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
fig, ax = plt.subplots()
ax.plot(both["date"], both["sp500_rebased"], label="S and P 500")
ax.plot(both["date"], both["nasdaq_rebased"], label="Nasdaq Composite")
ax.set_ylabel("Rebased value (start = 100)")
ax.set_title("S and P 500 vs Nasdaq, rebased to 100, price only")
ax.legend()
plt.tight_layout()
plt.savefig(CHARTS / "01_sp500_vs_nasdaq.png", dpi=150)
plt.show()
print("Nasdaq rebased end:", round(both["nasdaq_rebased"].iloc[-1], 1))
print("S and P 500 rebased end:", round(both["sp500_rebased"].iloc[-1], 1))
"""
        ),
        code(
            """
plot_era = era[~era["era"].str.contains("partial")]
fig, ax = plt.subplots()
ax.bar(plot_era["era"], plot_era["cagr_pct"])
ax.set_ylabel("Compound annual growth, percent per year")
ax.set_title("S and P 500 growth by full decade, price only")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(CHARTS / "01_decade_cagr.png", dpi=150)
plt.show()
"""
        ),
        md(
            """
## What we learned, in plain words

The long rise is real, but it was not smooth. The 2000s ended lower than
they started on a price basis, with a compound annual growth rate of
about minus 2.6 percent per year. The 1990s were the strongest full
decade in this file, at about 15.1 percent per year. The worst single
calendar year was 2008, at about minus 38.5 percent. The best was 1995,
at about plus 34.1 percent.

A beginner takeaway: a long chart that goes up does not mean every year
goes up. It means the up years, over a very long time, outweighed the
down years. That is why the next notebook looks at how rough the ride
was along the way.
"""
        ),
    ],
)

# ---------------------------------------------------------------- 02
save(
    "02_volatility_and_drawdowns.ipynb",
    [
        code(PIP),
        md(
            """
# 02. Volatility and drawdowns: how rough was the ride?

Volatility is a measure of how much prices jump around. Think of it as
bumpiness. A calm road has low volatility. A road full of potholes has
high volatility. In this notebook we use rolling volatility. Rolling
means we look at a moving window, here 30 trading days, and we measure
the spread of daily returns inside that window. We then annualize it,
which means we scale it up to a yearly number so years are comparable.
The scaling uses the square root of 252, because there are about 252
trading days in a year.

A drawdown is a fall from a previous peak. If the index peaked at 100
and later fell to 80, the drawdown is minus 20 percent. An underwater
chart plots that drawdown over time. When the line is at zero, the
market is at a new peak. When it is below zero, the market is still
under water, meaning it has not yet recovered its old peak.

The VIX is a separate index, published by Cboe, that reflects what
options traders expect for swings in the next 30 days. It is not a
prediction of direction. A high VIX means traders expect big moves, up
or down. A low VIX means they expect calm.
"""
        ),
        code(SETUP),
        code(
            """
sp = pd.read_csv(PROC / "sp500_daily.csv", parse_dates=["date"])
major = pd.read_csv(PROC / "sp500_major_drawdowns.csv")
vix = pd.read_csv(PROC / "vix_daily.csv", parse_dates=["date"])
print("Major drawdowns, falls of 20 percent or more:")
print(major.to_string(index=False))
print()
print("Highest 30 day rolling volatility in the file:")
row = sp.loc[sp["rolling_vol_30d"].idxmax()]
print(row["date"].date(), round(row["rolling_vol_30d"] * 100, 1), "percent annualized")
print("Highest VIX close in the file:")
row = vix.loc[vix["vix"].idxmax()]
print(row["date"].date(), row["vix"])
"""
        ),
        code(
            """
fig, ax = plt.subplots()
ax.plot(sp["date"], sp["rolling_vol_30d"] * 100)
ax.set_ylabel("30 day rolling volatility, percent annualized")
ax.set_title("S and P 500 rolling volatility, 1970 to 2026")
plt.tight_layout()
plt.savefig(CHARTS / "02_rolling_vol.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
fig, ax = plt.subplots()
ax.fill_between(sp["date"], sp["drawdown"] * 100, 0)
ax.set_ylabel("Drawdown from prior peak, percent")
ax.set_title("S and P 500 underwater chart: how far below the old peak?")
plt.tight_layout()
plt.savefig(CHARTS / "02_drawdown_underwater.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
plot_major = major.sort_values("depth_pct")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(plot_major["peak_date"] + " to " + plot_major["trough_date"], plot_major["depth_pct"])
ax.set_xlabel("Depth, percent")
ax.set_title("Largest S and P 500 drawdowns, peak to trough")
plt.tight_layout()
plt.savefig(CHARTS / "02_major_drawdowns.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
fig, ax = plt.subplots()
ax.plot(vix["date"], vix["vix"])
ax.set_ylabel("VIX close")
ax.set_title("VIX, 1990 to 2026: expected swings, not direction")
plt.tight_layout()
plt.savefig(CHARTS / "02_vix.png", dpi=150)
plt.show()
"""
        ),
        md(
            """
## What we learned, in plain words

The deepest fall in this file was the 2007 to 2009 episode, down about
56.8 percent from peak to trough, and it took until March 2013 to get
back to the old peak. The fastest deep fall was in early 2020, down
about 33.9 percent in about a month, then recovered in about 5 months.
Those two facts together are the lesson: some falls are deep and slow
to heal, others are sharp and fast to heal, and you cannot tell which
kind you are in while it is happening.

Volatility also clusters. Calm years tend to follow calm years, and
rough months tend to follow rough months. The highest VIX close in the
file was 82.69 on March 16, 2020. In March 2023, during the SVB week, the
VIX rose only to about 26.5. That contrast matters for the SVB chapter:
the broad market was stressed in March 2023, but it was not at 2020 or
2008 levels of panic.
"""
        ),
    ],
)

# ---------------------------------------------------------------- 03
save(
    "03_portfolio_risk_metrics.ipynb",
    [
        code(PIP),
        md(
            """
# 03. Portfolio risk metrics: return, risk, and diversification

A portfolio is just a mix of investments held together. Three ideas
carry this whole notebook.

First, volatility. We already met it in notebook 02. It is the spread
of returns, annualized. Higher volatility means a bumpier ride.

Second, return per unit of risk. Take the average yearly return and
divide it by volatility. If two mixes earn the same return, the one with
lower volatility has a higher return per unit of risk, which means it
earned that return with less bumpiness. This is a Sharpe style idea.
A true Sharpe ratio subtracts a safe rate, like a Treasury bill yield,
before dividing. Here we report return per unit of risk in plain form
and we say so, so nobody mistakes it for a formal Sharpe ratio.

Third, diversification benefit. Diversification means holding things
that do not always move together. If you average the volatility of each
holding on its own, and then measure the volatility of the mix, the mix
is usually less bumpy than the average holding. The gap between those
two numbers is the diversification benefit. It is small when holdings
move together, and larger when they move differently.

Important limit: this notebook uses three US stock indexes only, the
S and P 500, the Nasdaq Composite, and the Dow Jones Industrial
Average, from November 2016 to October 2026, because that is the window
where the FRED downloads for all three overlap. Three stock indexes
that track the same US market will move together a lot, so we expect
only a small diversification benefit here. That is a finding, not a
failure. It shows why real diversification usually needs different
kinds of assets, not just different stock indexes.

Nothing here is investment advice, and nothing here is a recommended
portfolio. We are describing past bumpiness, not predicting future returns.
"""
        ),
        code(SETUP),
        code(
            """
port = pd.read_csv(PROC / "portfolio_inputs_daily.csv", parse_dates=["date"])
ret_cols = ["fred_sp500_ret", "nasdaq_ret", "fred_dow_ret"]
rets = port[ret_cols].dropna()
print("Window:", port["date"].min().date(), "to", port["date"].max().date(), "with", len(rets), "daily returns")
corr = rets.corr()
print()
print("Correlation of daily returns (1 means they move together perfectly):")
print(corr.round(3).to_string())
"""
        ),
        code(
            """
import numpy as np
stats = []
labels = {"fred_sp500_ret": "S and P 500", "nasdaq_ret": "Nasdaq", "fred_dow_ret": "Dow"}
for col in ret_cols:
    r = rets[col]
    ann_ret = (1 + r).prod() ** (252 / len(r)) - 1
    ann_vol = r.std() * np.sqrt(252)
    stats.append({"asset": labels[col], "ann_return_pct": ann_ret * 100, "ann_vol_pct": ann_vol * 100,
                  "return_per_unit_risk": ann_ret / ann_vol})
equal = rets.mean(axis=1)
ann_ret_eq = (1 + equal).prod() ** (252 / len(equal)) - 1
ann_vol_eq = equal.std() * np.sqrt(252)
stats.append({"asset": "Equal mix of the three", "ann_return_pct": ann_ret_eq * 100,
              "ann_vol_pct": ann_vol_eq * 100, "return_per_unit_risk": ann_ret_eq / ann_vol_eq})
stats_df = pd.DataFrame(stats)
print(stats_df.round(2).to_string(index=False))
avg_single_vol = stats_df.iloc[:3]["ann_vol_pct"].mean()
print()
print("Average single index volatility:", round(avg_single_vol, 2), "percent")
print("Equal mix volatility:", round(ann_vol_eq * 100, 2), "percent")
print("Diversification benefit:", round(avg_single_vol - ann_vol_eq * 100, 2), "percentage points")
"""
        ),
        code(
            """
fig, ax = plt.subplots()
for _, row in stats_df.iterrows():
    ax.scatter(row["ann_vol_pct"], row["ann_return_pct"], s=120)
    ax.annotate(row["asset"], (row["ann_vol_pct"], row["ann_return_pct"]), xytext=(5, 5), textcoords="offset points")
ax.set_xlabel("Annualized volatility, percent (bumpiness)")
ax.set_ylabel("Annualized return, percent (price only)")
ax.set_title("Return vs risk, Nov 2016 to Oct 2026, price only")
plt.tight_layout()
plt.savefig(CHARTS / "03_risk_return.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
fig, ax = plt.subplots()
im = ax.imshow(corr.values, vmin=0.7, vmax=1.0)
ax.set_xticks(range(len(ret_cols)))
ax.set_yticks(range(len(ret_cols)))
ax.set_xticklabels(["S and P 500", "Nasdaq", "Dow"])
ax.set_yticklabels(["S and P 500", "Nasdaq", "Dow"])
for i in range(len(ret_cols)):
    for j in range(len(ret_cols)):
        ax.text(j, i, round(corr.values[i, j], 3), ha="center", va="center")
ax.set_title("Correlation of daily returns: all three move together a lot")
plt.tight_layout()
plt.savefig(CHARTS / "03_correlation.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
fig, ax = plt.subplots()
ax.bar(["Average single index", "Equal mix of three"], [avg_single_vol, ann_vol_eq * 100])
ax.set_ylabel("Annualized volatility, percent")
ax.set_title("Diversification benefit is small among US stock indexes")
plt.tight_layout()
plt.savefig(CHARTS / "03_diversification.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
cum = (1 + rets).cumprod() * 100
cum_eq = (1 + equal).cumprod() * 100
fig, ax = plt.subplots()
ax.plot(port["date"].iloc[1:], cum["fred_sp500_ret"], label="S and P 500")
ax.plot(port["date"].iloc[1:], cum["nasdaq_ret"], label="Nasdaq")
ax.plot(port["date"].iloc[1:], cum["fred_dow_ret"], label="Dow")
ax.plot(port["date"].iloc[1:], cum_eq, label="Equal mix", linewidth=2)
ax.set_ylabel("Growth of 100, price only")
ax.set_title("Cumulative growth, Nov 2016 to Oct 2026, price only")
ax.legend()
plt.tight_layout()
plt.savefig(CHARTS / "03_portfolio_cumulative.png", dpi=150)
plt.show()
"""
        ),
        md(
            """
## What we learned, in plain words

Over this window, the Nasdaq had the highest return and the highest
volatility, the Dow had the lowest return and the lowest volatility,
and the equal mix sat in the middle on both. Correlations were high,
from 0.82 to 0.95, so the diversification benefit was only about 0.6
percentage points of volatility. That is the honest result: mixing three
US stock indexes smooths the ride only a little, because they mostly
rise and fall together.

If someone promises a big diversification benefit from holding three
similar stock funds, ask what is actually different about them. Real
diversification needs assets that behave differently in stress, and
that claim needs to be tested with data, not assumed.
"""
        ),
    ],
)

# ---------------------------------------------------------------- 04
save(
    "04_svb_case_study.ipynb",
    [
        code(PIP),
        md(
            """
# 04. SVB case study: what happened in March 2023

Silicon Valley Bank, called SVB, was a US bank that served mainly
technology companies and venture capital firms. It failed on March 10,
2023. This notebook explains the mechanics in plain words, then checks
the market context with our own data. It does not use the old
AI-trading.py script from the original repo as evidence, because that
script was never verified. It also does not claim a trading strategy
would have predicted or profited from the failure.

## Three ideas you need first

Duration risk. A bond is a loan to a borrower, like the US government,
that pays interest and returns the principal later. When interest rates
rise, old bonds that pay low interest become less attractive, so their
market price falls. The longer the bond has left to run, the more its
price falls for the same rate rise. That sensitivity is called duration.
A bank that buys long bonds at low rates is taking duration risk.

Held to maturity accounting. A bank can label some bonds as held to
maturity, meaning it plans to keep them until they repay. Those bonds
are carried on the books at their original cost, not at their current
market price. The gap between book value and market value is called an
unrealized loss. It is real in economic terms, but it does not show up
in headline profit until the bank sells. If the bank is forced to sell
to meet withdrawals, the unrealized loss becomes a realized loss at once.

A bank run. Banks lend out most deposits, so they do not hold enough
cash to repay every depositor on the same day. That works fine when
withdrawals are spread out. It breaks when many depositors ask for
their money at once, especially depositors with very large balances
above the FDIC insurance limit of 250,000 dollars. Those depositors
have the most reason to run first, because only the insured part is
guaranteed in a normal failure.

## Timeline, from official sources

The Federal Reserve published a review of its supervision of SVB in
April 2023. The FDIC and the California regulator closed the bank on
March 10, 2023. On March 12, 2023, the Treasury, the Federal Reserve,
and the FDIC announced that all deposits at SVB, insured and
uninsured, would be protected under a systemic risk exception, and the
Federal Reserve created a lending program for banks. Those are official
actions, and we report them as such. Where sources disagree on a detail,
for example the exact share of uninsured deposits, we give a range and
say so in the notes below.
"""
        ),
        code(SETUP),
        code(
            """
# SVB facts table, sourced, not computed from market data.
# Sources: Federal Reserve review of SVB supervision, April 2023;
# SVB Financial Group 10-K for year end 2022, via the Federal Reserve
# and FASB comment letter summaries; FDIC and joint agency statements.
svb = pd.DataFrame([
    {"item": "Total assets at failure, about", "value": "209 billion dollars"},
    {"item": "Held to maturity bonds, book value, year end 2022", "value": "91 billion dollars"},
    {"item": "Held to maturity bonds, fair value, year end 2022", "value": "76 billion dollars"},
    {"item": "Unrealized loss on held to maturity bonds", "value": "about 15.2 billion dollars"},
    {"item": "Total equity at year end 2022", "value": "about 16.3 billion dollars"},
    {"item": "Available for sale bonds sold on March 8, 2023", "value": "about 21 billion dollars"},
    {"item": "Loss realized on that sale", "value": "about 1.8 billion dollars"},
    {"item": "Capital raise announced March 8, 2023", "value": "about 2.25 billion dollars"},
    {"item": "Withdrawals attempted on March 9, 2023", "value": "about 42 billion dollars"},
    {"item": "Bank closed", "value": "March 10, 2023"},
    {"item": "All deposits protected, joint announcement", "value": "March 12, 2023"},
])
print(svb.to_string(index=False))
print()
print("Check: 91 minus 76 is 15, which matches the reported unrealized loss of about 15.2 billion, allowing for rounding.")
print("Check: 42 billion is about one quarter of total deposits, consistent with reports that it was roughly 25 percent.")
print("Uninsured share: reports range from about 88 percent to about 94 percent depending on the measure and date. We report the range, not a single exact figure.")
"""
        ),
        code(
            """
rates = pd.read_csv(PROC / "svb_window_rates.csv", parse_dates=["date"])
print("10 year yield, Aug 2020 low in our data:", rates.loc[rates["yield_10y"].idxmin(), ["date", "yield_10y"]].to_dict())
window = rates[(rates["date"] >= "2021-01-01") & (rates["date"] <= "2023-03-31")]
print(window.iloc[0].to_dict())
print(window.iloc[-1].to_dict())
fig, ax = plt.subplots()
ax.plot(window["date"], window["yield_10y"], label="10 year Treasury yield")
ax.plot(window["date"], window["yield_2y"], label="2 year Treasury yield")
ax.axvline(pd.Timestamp("2023-03-10"), color="red", linestyle="--", label="SVB closed, Mar 10 2023")
ax.set_ylabel("Yield, percent")
ax.set_title("Yields rose fast in 2022, before SVB failed in March 2023")
ax.legend()
plt.tight_layout()
plt.savefig(CHARTS / "04_rates_2020_2023.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
# Illustrative bond math only. This is NOT SVB's actual portfolio.
# Formula in plain words: price change in percent is about minus duration
# times the change in yield in percentage points.
# Example: a bond with duration 8, if yields rise 3 points, price falls about 24 percent.
# SVB's reported loss was about 15.2 on 91, or about 16.7 percent, which is
# in the same ballpark as this kind of long bond math, but the exact
# duration of SVB's portfolio is not recovered here from public summaries.
durations = [2, 5, 8, 12]
yield_rise = 3.0
losses = [-d * yield_rise for d in durations]
fig, ax = plt.subplots()
ax.bar([f"Duration {d} years" for d in durations], losses)
ax.set_ylabel("Illustrative price change, percent")
ax.set_title("Illustrative: longer bonds fall more when yields rise 3 points")
plt.tight_layout()
plt.savefig(CHARTS / "04_illustrative_bond.png", dpi=150)
plt.show()
for d, loss in zip(durations, losses):
    print(f"Duration {d}: about {loss} percent")
print("SVB reported held to maturity loss share: about", round(15.2 / 91 * 100, 1), "percent")
"""
        ),
        code(
            """
mkt = pd.read_csv(PROC / "svb_window_markets.csv", parse_dates=["date"])
vix = pd.read_csv(PROC / "vix_daily.csv", parse_dates=["date"])
vix_mar = vix[(vix["date"] >= "2023-03-01") & (vix["date"] <= "2023-03-20")]
print("VIX in March 2023, around the failure:")
print(vix_mar.to_string(index=False))
fig, ax = plt.subplots()
ax.plot(mkt["date"], mkt["sp500_rebased_feb1"], label="S and P 500")
ax.plot(mkt["date"], mkt["nasdaq_rebased_feb1"], label="Nasdaq")
ax.axvline(pd.Timestamp("2023-03-10"), color="red", linestyle="--", label="SVB closed, Mar 10 2023")
ax.set_ylabel("Rebased value (Feb 1, 2023 = 100)")
ax.set_title("Broad markets fell in the SVB week, then recovered by end of March")
ax.legend()
plt.tight_layout()
plt.savefig(CHARTS / "04_market_svb_window.png", dpi=150)
plt.show()
"""
        ),
        md(
            """
## Lessons, stated carefully

First, duration risk is not a footnote. When yields rose from about
0.5 percent on the 10 year Treasury in August 2020 to about 4.0 percent
in early March 2023 in our FRED data, long bonds lost a large share of
their market value. A bank that funded those bonds with deposits that
could leave quickly was exposed on both sides: asset values down,
funding able to run.

Second, concentration matters. A deposit base dominated by a small
number of large, connected, uninsured depositors can move together.
On March 9, 2023, about 42 billion dollars was withdrawn in one day.
That speed, not just the size of the loss, is what closed the bank.

Third, accounting labels do not change economics. Held to maturity
accounting kept the unrealized loss off headline profit, but the loss
was disclosed in footnotes, and it became real the moment the bank had
to sell. Anyone reading only the headline equity number, about 16.3
billion dollars, without the footnote loss of about 15.2 billion
dollars, would have missed how thin the cushion really was.

Fourth, the broad market did not collapse. The S and P 500 fell from
100 on February 1, 2023 to about 93.7 on March 10, and was back to about
99.8 by March 31. The Nasdaq was above its February 1 level by March 31.
The lesson is not that every bank failure causes a market crash. It is
that a single bank can fail fast from liquidity and interest rate risk
even while the broad market recovers.
"""
        ),
    ],
)

# ---------------------------------------------------------------- 05
save(
    "05_recovery_score_and_era_comparison.ipynb",
    [
        code(PIP),
        md(
            """
# 05. Original metric: the Drawdown Recovery Score, and risk adjusted eras

This is the original contribution of this project. It is simple on
purpose, so a beginner can compute it by hand from a peak, a trough,
and a recovery date.

## The Drawdown Recovery Score, in plain words

Take one major fall, a fall of 20 percent or more from a peak.

Step 1, depth factor: if the fall was 20 percent, the depth factor is
0.80, because 80 percent of the value remained. If the fall was 50
percent, the depth factor is 0.50.

Step 2, speed factor: take the time from trough to recovery, in years,
add 1, and take the reciprocal. A recovery in 6 months is 0.5 years,
so the speed factor is 1 divided by 1.5, which is about 0.67. A
recovery in 5 years gives 1 divided by 6, which is about 0.17.

Step 3, score: multiply depth factor by speed factor, then multiply
by 100. The score runs from 0 to 100. Higher is better, meaning the
fall was shallower, or faster to heal, or both.

Example: a 20 percent fall recovered in 6 months scores about 53.
A 50 percent fall recovered in 60 months scores about 8.

Limits, stated honestly: the score does not measure what caused the
fall, it does not measure dividends, and it treats a fast shallow fall
as better than a slow deep fall even if the slow fall was caused by a
worse crisis. It is a descriptive summary, not a ranking of how bad a
crisis was for people. Use it to compare recovery shapes, not to judge
history.

## Risk adjusted era comparison

We also compare decades by return per unit of risk, which we defined
in notebook 03: compound annual growth divided by annualized
volatility. This answers a different question from raw growth: which
era gave the most growth for each unit of bumpiness?
"""
        ),
        code(SETUP),
        code(
            """
major = pd.read_csv(PROC / "sp500_major_drawdowns.csv")
era = pd.read_csv(PROC / "sp500_by_era.csv")
print("Major drawdowns with Recovery Score:")
print(major[["peak_date", "trough_date", "recovery_date", "depth_pct", "decline_months", "recovery_months", "recovery_score"]].to_string(index=False))
print()
print("Era comparison:")
print(era.to_string(index=False))
"""
        ),
        code(
            """
plot_major = major.sort_values("recovery_score", ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(plot_major["peak_date"] + " fall", plot_major["recovery_score"])
ax.set_xlabel("Drawdown Recovery Score, 0 to 100, higher is faster and shallower")
ax.set_title("Drawdown Recovery Score for major S and P 500 falls")
plt.tight_layout()
plt.savefig(CHARTS / "05_recovery_score.png", dpi=150)
plt.show()
"""
        ),
        code(
            """
plot_era = era[~era["era"].str.contains("partial")]
fig, ax = plt.subplots()
ax.bar(plot_era["era"], plot_era["return_per_unit_risk"])
ax.set_ylabel("Return per unit of risk (growth divided by volatility)")
ax.set_title("Risk adjusted era comparison, full decades, price only")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(CHARTS / "05_era_risk_adjusted.png", dpi=150)
plt.show()
"""
        ),
        md(
            """
## What we learned, in plain words

The highest Recovery Score among major falls was the 1980 to 1982
episode, at 59.5. That fall was about 27.1 percent deep, but it
recovered from trough in only about 2.7 months, so it scores high
despite a long decline. The 2020 fall scored 46.9, because it was
deep, about 33.9 percent, but very fast to heal, about 4.9 months from
trough. The lowest scores were the three deepest falls: 1973 to 1974
at 7.6, 2007 to 2009 at 8.6, and 2000 to 2002 at 9.0. All three were
about 48 to 57 percent deep and took about 49 to 69 months from trough
to recover.

On the era comparison, the 1990s had the highest return per unit of
risk, at 1.07, followed by the 1980s and 2010s at 0.75 each. The 2000s
were the only full decade with a negative score, at minus 0.12, because
growth was negative while volatility was the highest of any full
decade, at about 22.2 percent.

The story angle is simple: raw growth alone hides the cost of getting
there. The 1990s did not just grow fast, they grew fast with moderate
bumpiness. The 2000s did not just grow slowly, they fell hard and took
years to heal. A portfolio story that only shows the end value, without
the drawdowns and the recovery times, is missing half the story.
"""
        ),
    ],
)

print("All notebooks built.")
