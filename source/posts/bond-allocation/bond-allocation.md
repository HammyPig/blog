---
icon: "{fas}`money-bill`"
date: "2024-11-13"
desc: "It is commonly preached that bonds are essential to a sustainable portfolio. But how true really is this statement? After all, bonds are commonly known to sacrifice performance, so to have a portfolio with the lowest amount necessary is optimal. To explore the effects of bonds, we will compare 5 different stock/bond allocations; a control 100% stock allocation, along with the 4 different allocations based approximately on the Vanguard ready-made portfolios."
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import datetime as dt

plt.style.use("grayscale")
plt.rc("figure", labelsize="x-small", autolayout=True, figsize=(4, 3), facecolor="white")
plt.rc("xtick", labelsize="x-small")
plt.rc("ytick", labelsize="x-small")
```

# Bond Allocation

It is commonly preached that bonds are essential to a sustainable portfolio. But how true really is this statement? After all, bonds are commonly known to sacrifice performance, so to have a portfolio with the lowest amount necessary is optimal. 

To explore the effects of bonds, we will compare 5 different stock/bond allocations; a control 100% stock allocation, along with the 4 different allocations based approximately on the Vanguard ready-made portfolios.[^passiveinvestingaustralia]

[^passiveinvestingaustralia]: https://passiveinvestingaustralia.com/vdhg-or-roll-your-own/

```{code-cell} ipython3
:tags: [remove-input]

table = [
    ["Fund", "Stock/Bond Allocation"],
    ["Control", "100 / 0"],
    ["VDHG (High Growth)", "90 / 10"],
    ["VDGR (Growth)", "70 / 30"],
    ["VDBA (Balanced)", "50 / 50"],
    ["VDCO (Conservative)", "30 / 70"]
]

pd.DataFrame(table[1:], columns=table[0]).style.hide(axis="index")
```

## Methodology

The most basic way to observe whether one allocation is better than the other is to look at the mean and standard deviation of performance over time. However, this approach is too abstract for my tastes, and misses a lot of nuance. Here I'll explain my approach.

First we need to define what a retirement fund is. A retirement fund is an investment portfolio where a regular living expense can be withdrawn perpetually. This is possible in theory when the amount gained from your portfolio performance is greater than the amount you withdraw each year. It is commonly advised that an investment portfolio worth 25x your annual living expenses is the lowest threshold for a retirement fund.[^trinitystudy]

[^trinitystudy]: https://en.wikipedia.org/wiki/Trinity_study

This regular withdrawals of a retirement fund is very important. If we did not intend on regularly withdrawing funds, and instead only cared about pure performance, we would not need to consider stability. After all, if we only cared about the long-term outlook, we would be indifferent to any sporadic short-term fluctuations.

In this case, looking at volatility is of great importance. Let's say you have an investment portfolio worth 25x your annual living expenses (as suggested previously). Imagine a major recession occurs, lowering your portfolio by 40% (as seen during the 2008 recession). Suddenly, your portfolio is only worth 15x your living cost, meaning that your returns will most likely be less than the amount you withdraw. If the market does not recover quick enough, your portfolio is at risk of reaching a threshold where it can no longer keep up. Instead it will continue to diminish in value over time, eventually reaching zero.

To properly consider this scenario, we will simulate purchasing a lump-sum amount of each allocation. Then, we will withdraw an annual living expense each year to see if our allocation can keep up perpetually. After a 40 year period, the final amount will be recorded. All values are also adjusted for inflation. This will be tested a number of times wich each allocation to see how likely our portfolio is still sustained, even after 40 years of constant withdrawals.

We can then check two metrics:

1. Sustainability: The probability that the allocation's final valuation is greater than or equal to its starting amount.
1. Performance: The distribution of the allocation's final valuation.

Of course, sustainability is the most important trait of a retirement portfolio, though we will still explore performance to see if anything interesting occurs.

```{code-cell} ipython3
:tags: [remove-input]

from openpyxl.reader.excel import ExcelReader
from openpyxl.xml import constants as openpyxl_xml_constants
from pandas import ExcelFile
from pandas.io.excel._openpyxl import OpenpyxlReader

class OpenpyxlReaderWOFormatting(OpenpyxlReader):
    """OpenpyxlReader without reading formatting
    - this will decrease number of errors and speedup process
    error example https://stackoverflow.com/q/66499849/1731460 """

    def load_workbook(self, filepath_or_buffer, *args, **kwargs):
        """Same as original but with custom archive reader"""
        reader = ExcelReader(filepath_or_buffer, read_only=True, data_only=True, keep_links=False)
        reader.archive.read = self.read_exclude_styles(reader.archive)
        reader.read()
        return reader.wb

    def read_exclude_styles(self, archive):
        """skips addings styles to xlsx workbook , like they were absent
        see logic in openpyxl.styles.stylesheet.apply_stylesheet """

        orig_read = archive.read

        def new_read(name, pwd=None):
            if name == openpyxl_xml_constants.ARC_STYLE:
                raise KeyError
            else:
                return orig_read(name, pwd=pwd)

        return new_read

ExcelFile._engines['openpyxl_wo_formatting'] = OpenpyxlReaderWOFormatting
```

```{code-cell} ipython3
:tags: [remove-input]

df_orig = pd.read_excel("data/Backtest-Portfolio-returns-rev23b.xlsx", engine="openpyxl_wo_formatting", sheet_name="Data_Series")
```

```{code-cell} ipython3
:tags: [remove-input]

df = df_orig.copy()

df = df.loc[:, ~df.columns.str.startswith("Unnamed: ")] # remove empty columns
df = df[165:318] # get inflation adjusted returns 1871-2023

df = df.rename(columns={"ER-adjusted spliced returns": "date"})
df["date"] = pd.to_datetime(df["date"], format="%Y")
df = df.set_index("date")

df = df.apply(pd.to_numeric)

df = df.map(lambda x: (x / 100) + 1 if x >= 0 else 1 + (x / 100)) # e.g. 20% is converted to 1.2, the + 1 makes cumprod easier
```

```{code-cell} ipython3
:tags: [remove-input]

allocations = {
    "100 / 0": {
        "TSM (US)": 1,
        "TBM (US)": 0
    },
    "90 / 10": {
        "TSM (US)": 0.9,
        "TBM (US)": 0.1
    },
    "70 / 30": {
        "TSM (US)": 0.7,
        "TBM (US)": 0.3
    },
    "50 / 50": {
        "TSM (US)": 0.5,
        "TBM (US)": 0.5
    },
    "30 / 70": {
        "TSM (US)": 0.3,
        "TBM (US)": 0.7
    }
}
```

```{code-cell} ipython3
:tags: [remove-input]

def test_allocation(allocation, yearly_expenses_ratio):
    starting_investment = 1_000_000
    yearly_expenses = starting_investment / yearly_expenses_ratio
    backtesting_duration_years = 40
    
    wrapped_df = df[["TSM (US)", "TBM (US)"]]
    wrapped_part = wrapped_df.iloc[:backtesting_duration_years].copy()
    wrapped_part.index += pd.DateOffset(years=wrapped_df.index.year[-1] - df.index.year[0] + 1)
    wrapped_df = pd.concat([wrapped_df, wrapped_part])
    backtesting_results = []
    
    for i in range(len(wrapped_df) - backtesting_duration_years):
        # define experiment period
        backtesting_period = wrapped_df[i: i + backtesting_duration_years]
        
        # portfolio starting conditions
        portfolio = {k: v * starting_investment for k, v in allocation.items()}
    
        # simulate each year
        backtesting_history = np.zeros(backtesting_duration_years)
        j = -1
        for index, row in backtesting_period.iterrows():
            j += 1
            
            # check if bankrupt
            if sum(portfolio.values()) < yearly_expenses:
                portfolio = {k: 0 for k in portfolio}
                break
    
            # deduct expenses and rebalance portfolio
            target_portfolio = {k: v * sum(portfolio.values()) for k, v in allocation.items()}
            rebalancing_required = {k: target_portfolio[k] - portfolio[k] for k in portfolio.keys()}
    
            sell_stock = min(rebalancing_required, key=rebalancing_required.get)
            portfolio[sell_stock] -= yearly_expenses
    
            # update portfolio based on performance
            for k in portfolio.keys():
                portfolio[k] *= row[k]

            backtesting_history[j] = sum(portfolio.values())
            
        # normalise results
        backtesting_history /= starting_investment
        
        # record experiment outcome
        backtesting_history = pd.Series(backtesting_history, index=backtesting_period.index)
        backtesting_results.append(backtesting_history)

    return backtesting_results
```

```{code-cell} ipython3
:tags: [remove-input]

allocation_result_distributions = {}

for k, v in allocations.items():
    allocation_result_distributions[k] = test_allocation(v, 25)
```

## Sustainability

```{code-cell} ipython3
:tags: [remove-input]

table = {}
for k, v in allocation_result_distributions.items():
    final_portfolio_values = np.array([x.iloc[-1] for x in v])
    table[k] = f"{(final_portfolio_values >= 1).sum() / final_portfolio_values.size * 100:.2f}%"

table = pd.DataFrame.from_dict(table, orient="index")
table = table.reset_index()
table.columns = ["Stock/Bond Allocation", "Sustainable Probability"]

table.style.hide(axis="index")
```

Here we can see that a higher bond allocation has a negative effect on the probability that our portfolio is sustainable.

On another note, it is interesting to see that a typical 25x retirement fund still has a 13% chance of unsustainability. Perhaps a higher initial investment amount is needed? Because of this finding, I repeated the experiment with a handful of different initial portfolio sizes for two reasons:

1. Is the negative trend of bonds apparent across all initial investment amounts?
1. Is it possible to achieve a 100% sustainability rate? And if so, when?

```{code-cell} ipython3
:tags: [remove-input]

starting_amounts = [15, 20, 25, 30, 35]
starting_amounts_allocation_result_distributions = {}

for k, v in allocations.items():
    starting_amounts_allocation_result_distributions[k] = []
    for x in starting_amounts:
        results = test_allocation(v, x)
        final_portfolio_values = np.array([x.iloc[-1] for x in results])
        sustainable_probability = (final_portfolio_values >= 1).sum() / final_portfolio_values.size * 100
        starting_amounts_allocation_result_distributions[k].append(sustainable_probability)
```

```{code-cell} ipython3
:tags: [remove-input]

# inspiration: https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

fig, ax = plt.subplots()

x = np.arange(len(starting_amounts))  # the label locations
width = 0.1  # the width of the bars
multiplier = 0

for k, v in starting_amounts_allocation_result_distributions.items():
    offset = width * multiplier
    plt.bar(x + offset, v, width, label=k)
    multiplier += 1

ax.set_xlabel("Initial Portfolio Amount (rel. Living Expenses)")
ax.set_xticks(x + 2 * width, [f"{x}x" for x in starting_amounts])

ax.set_ylabel("Sustainable Probability")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

plt.show()
```

To first explain the figure, each set of bars represents a different initial investment amount. The individual bars are the different stock/bond allocations, with the same 100, 90/10, 70/30, 50/50, and 30/70 allocations from left to right.

Here we can observe two things:

1. The previously discovered negative bond effect is apparent regardless of initial portfolio size.
1. A 100% sustainable probability is only reached at a 35x initial investment amount.

From these results, it seems that adding bonds to a retirement fund has only a negative effect on sustainability, and has no justification to be included. Additionally on another note, the commonly advised 25x initial investment amount is too low, and should instead be increased to 35x for a more robust portfolio.

+++

## Performance

+++

Because of the previous results, I have modified the experiment to now start with an initial 35x investment amount.

```{code-cell} ipython3
:tags: [remove-input]

allocation_result_distributions = {}

for k, v in allocations.items():
    allocation_result_distributions[k] = test_allocation(v, 35)
```

```{code-cell} ipython3
:tags: [remove-input]

data = []
xticklabels = []
for k, v in allocation_result_distributions.items():
    data.append([x.iloc[-1] for x in v])
    xticklabels.append(k)

fig, ax = plt.subplots()

plt.boxplot(data)

ax.set_xlabel("Stock/Bond Allocation")
ax.set_xticklabels(xticklabels)

ax.set_ylabel("Portfolio Performance")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x * 100}%"))

plt.show()
```

As expected, a higher bond allocation has a negative effect on our portfolio's performance.

I then theorised what other use case could bonds have? Why would Vanguard's highest risk pre-made portfolio still include bonds? Perhaps bonds would help in the absolute worst of circumstances, so I also looked at the bottom 5th percentile of results to see if any observation could be made.

```{code-cell} ipython3
:tags: [remove-input]

data = []
xticklabels = []
for k, v in allocation_result_distributions.items():
    data.append(sorted([x.iloc[-1] for x in v])[:len(v) // 20])
    xticklabels.append(k)

fig, ax = plt.subplots()

plt.boxplot(data)

ax.set_xlabel("Stock/Bond Allocation")
ax.set_xticklabels(xticklabels)

ax.set_ylabel("Portfolio Performance")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x * 100}%"))

plt.show()
```

Even in the bottom 5% of results, the negative effect of bonds is still visible.

I could not find any reason to include bonds at all in a portfolio.

+++

## Conclusion

A higher bond allocation has a negative effect on both the sustainability and performance of a portfolio, and therefore has no reason to be included in a portfolio. Additionally, the threshold for a retirement fund should be increased from the commonly known 25x figure, to 35x your living expenses, as such a change would improve the probability that your portfolio is sustainable from 87% to 100% based on past performance.
