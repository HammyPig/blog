---
icon: "{fas}`money-bill`"
date: "2024-11-01"
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

We will simulate purchasing a lump-sum amount of each allocation, and record the final portfolio value after a 40 year period, taking into account both inflation and yearly withdrawals.

We can then check two metrics:

1. Sustainability: The probability that the allocation's final valuation is greater than or equal to its starting amount.
1. Performance: The distribution of the allocation's final valuation.

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
            portfolio_sum = sum(portfolio.values())
            
            # check if bankrupt
            if portfolio_sum < yearly_expenses:
                portfolio = {k: 0 for k in portfolio}
                break
    
            # deduct expenses and rebalance portfolio
            target_portfolio = {k: v * portfolio_sum for k, v in allocation.items()}
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

A higher bond allocation has a negative effect on the probability that our portfolio is sustainable.

+++

## Performance

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

A higher bond allocation has a negative effect on our portolfio's performance.

+++

## Conclusion

A higher bond allocation has a negative effect on both the sustainability and performance of a portfolio.
