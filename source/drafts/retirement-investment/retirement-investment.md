---
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

# The Minimum Retirement Investment

By investing 35x your current yearly living expenses into a common S&P 500 index fund, you could perpetually use your investment returns to pay your future expenses without ever diminishing your investment.

For example, the average single person living in Australia spends roughly \$4000 a month. To fund this lifestyle indefinitely would require an investment of $4000 \times 12 \times 35 = \$1.68\text{M}$. After accumulating this amount, each year they would sell \$48000 worth of stock to pay for their expenses, knowing that in a years time, the return of the remaining \$1.63M investment will outgrow this deduction.

You may question how tax efficient this strategy is. When considering the current tax brackets and capital gains discount, the amount of tax they would pay on this yearly withdrawal is minimal, varying from 0-$1000. This is because the highly liquid nature of stocks allows an individual to sell only what they need, minimising taxable income. This is in contrast to an asset like real-estate, which forces you to trigger extremely high CGT events all at once.

The 35x figure comes from an assumed investment return of 2.85%. Since stock markets are commonly quoted to perform much higher, this assumption may first seem a bit conversative.

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import datetime as dt
import plotly.graph_objects as go

plt.style.use("grayscale")
plt.rc("figure", labelsize="x-small", autolayout=True, figsize=(4, 3), facecolor="white")
plt.rc("xtick", labelsize="x-small")
plt.rc("ytick", labelsize="x-small")
```

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

df_nominal = df_orig.copy()
df_nominal = df_nominal.loc[:, ~df_nominal.columns.str.startswith("Unnamed: ")]
df_nominal = df_nominal[6:159]
df_nominal = df_nominal.rename(columns={"ER-adjusted spliced returns": "date"})
df_nominal["date"] = pd.to_datetime(df_nominal["date"], format="%Y")
df_nominal = df_nominal.set_index("date")
df_nominal = df_nominal.apply(pd.to_numeric)
df_nominal = df_nominal.map(lambda x: (x / 100) + 1 if x >= 0 else 1 + (x / 100))
```

```{code-cell} ipython3
:tags: [remove-input]

df = df_orig.copy()
df = df.loc[:, ~df.columns.str.startswith("Unnamed: ")]
df = df[165:318]
df = df.rename(columns={"ER-adjusted spliced returns": "date"})
df["date"] = pd.to_datetime(df["date"], format="%Y")
df = df.set_index("date")
df = df.apply(pd.to_numeric)
df = df.map(lambda x: (x / 100) + 1 if x >= 0 else 1 + (x / 100))
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plt.plot(10000 * df_nominal["S&P 500 TR"][-20:].cumprod())
plt.plot(10000 * df["S&P 500 TR"][-20:].cumprod(), linestyle="dotted")

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:.0f}"))

plt.title("Hypothetical Investment of $10,000")
plt.legend(["S&P 500", "Inflation Adjusted"])
plt.show()
```

The S&P 500, for example, returns 10.9% p.a. on average. However, this doesn't take into account inflation. In reality, it returns 8.6% when inflation-adjusted. This amount is still impressive though, and would imply that we could invest a much lower 12x our yearly expenses to be kept afloat, while simultaneously keeping up with inflation.

However, if by chance we begin this strategy at an unlucky time, we fall prone to unexpected recessions. See below how even a 20x strategy would quickly exhaust its investment balance during the dot-com bubble (which caused the S&P 500 to drop 40%), whereas a 35x strategy would hold strong enough to recover.

```{code-cell} ipython3
:tags: [remove-input]

threshold_factor_balance_history = {
    20: [],
    30: []
}

for k in threshold_factor_balance_history.keys():
    yearly_expenses = 48000
    starting_investment = yearly_expenses * k
    investment_balance_history = []
    
    experiment_period = df["S&P 500 TR"].dropna()[-25:]
    investment_balance = starting_investment
    
    for year_pct_change in experiment_period:
        if investment_balance < yearly_expenses:
            investment_balance = 0
        else:
            investment_balance -= yearly_expenses
            investment_balance *= year_pct_change
    
        threshold_factor_balance_history[k].append(investment_balance)

fig, ax = plt.subplots()

plt.plot(experiment_period.index, threshold_factor_balance_history[30])
plt.plot(experiment_period.index, threshold_factor_balance_history[20], linestyle="dotted")

plt.scatter(dt.datetime(2000, 3, 1), 50000, s=5)
plt.text(dt.datetime(2000, 12, 1), 0, "dot-com bubble")

plt.title(f"Simulated Investment Balance {experiment_period.index[0].year}-{experiment_period.index[-1].year}")
plt.legend(["35x", "20x"])

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000000:.1f}M"))

plt.show()
```

Based on 100 years of historical data, a 35x strategy would successfully bridge the gap of events such as WW2, the Cold War, and Black Monday.

For the strategy to fail, a catastrophic event never before seen in history would need to occur. This would be akin to something like nuclear war, which at such a point, would make money, society, and law irrelevant regardless.

Therefore, if not using your excess funds to build nuclear shelters, a 35x investment in index funds is the next best thing.
