---
icon: "{fas}`money-bill`"
date: "2024-09-25"
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Perpetual Retirement Fund

What is the end-goal of investing? The most noble goal is to achieve financial independence.

Financial independence is when you are no longer obligated to work to fund your lifestyle. One way to achieve this is to create an investment portfolio so large that its returns alone would cover your yearly expenses perpetually. But what should we invest in? And how much would we need to accumulate?

Let's consider the S&P 500 as our sole investment vehicle. The S&P 500 is a stock market index which tracks the stock performance of the top 500 largest US companies. It's known for two things: performance, and consistency.

In terms of performance, the index on average returns 10.9% per year - drastically outcompeting any standard savings/term deposit account:

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

cash_rate = pd.read_csv("data/aus-cash-rate-target.csv")

cash_rate = cash_rate.loc[:, ~cash_rate.columns.str.startswith("Unnamed: ")]
cash_rate.drop(columns=["Change%\xa0points", "Related Documents"], inplace=True)

cash_rate["Effective Date"] = pd.to_datetime(cash_rate["Effective Date"], format="%d %b %Y")

cash_rate["Cash rate target %"] = cash_rate["Cash rate target %"].replace({
    "15.00 to 15.50": "15.25",
    "16.50 to 17.00" : "16.75",
    "17.00 to 17.50" : "17.25"
})

cash_rate["Cash rate target %"] = pd.to_numeric(cash_rate["Cash rate target %"])

cash_rate["Year"] = cash_rate["Effective Date"].dt.year
cash_rate = cash_rate.sort_values("Effective Date").reset_index(drop=True)
cash_rate["Duration"] = (cash_rate["Effective Date"].shift(-1) - cash_rate["Effective Date"]).dt.days
cash_rate.at[df.index[-1], "Duration"] = (pd.Timestamp.today() - cash_rate.loc[cash_rate.index[-1], "Effective Date"]).days

cash_rate = cash_rate.groupby("Year")[["Cash rate target %", "Duration"]].apply(
    lambda g: (g["Cash rate target %"] * g["Duration"]).sum() / g["Duration"].sum()
).reset_index(name="Time-weighted Cash Rate %")

cash_rate["Year"] = pd.to_datetime(cash_rate["Year"], format="%Y")

cash_rate = cash_rate.set_index("Year")

cash_rate["Time-weighted Cash Rate %"] = 1 + (cash_rate["Time-weighted Cash Rate %"] / 100)
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plt.plot(10000 * df_nominal["S&P 500 TR"][-20:].cumprod())
plt.plot(10000 * cash_rate[-22:-2].cumprod(), linestyle="dotted")

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:.0f}"))

plt.title("Hypothetical Investment of $10,000")
plt.legend(["S&P 500", "Cash"])
plt.show()
```

In terms of consistency, it has been shown to produce solid growth over the last 140 years:

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plt.plot(df_nominal["S&P 500 TR"].cumprod())

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:.0f}"))
ax.set_yscale("log")

plt.title("S&P 500 Performance 1871-2023")
plt.show()
```

Because of its stellar performance, consistency, and simplicity, it will be used as our investment choice in this scenario.

Next, we move on to the second question: how much do we need to accumulate? As an example, let's assume we are the average Australian, who individually spends roughly \$4000 a month. This means our investment portfolio would need to generate at least \$48000 a year to cover our costs.

If we assume a continual portfolio return of 10.96% per year (8.6% post-inflation), we could then calculate our target investment amount as follows:

$$
x \times 8.6\% = 48\text{k} \\
x = 48\text{k} \div 8.6\% \\
x = ~\$560\text{k}
$$

Let's call this a '12x' portfolio, as the total is roughly 12x the cost of our yearly expenses. Once we reach 12x, we would then simply sell \$48k worth of stock at the start of each year, covering our expenses for the entire year. By the time we get to next year, our investment theoretically will have outgrown this deduction; a process which should repeat itself indefinitely.

```{code-cell} ipython3
:tags: [remove-input]

t = np.linspace(0, 3, 1000)
y = t % 1
y = np.roll(y, 2)
y = y * 48000 + 576000 - 48000

fig, ax = plt.subplots()

plt.plot(t, y)

plt.scatter(0, 600000, s=5, c="k")
plt.annotate(
    "Sell to pay for living expenses",
    xy=(0, 600000),
    xytext=(0.5, 600000 + 25000),
    arrowprops=dict(arrowstyle="-", relpos=(0, 0.5)),
    fontsize=8
)

plt.scatter(0.5, 525000, s=5, c="k")
plt.annotate(
    "Portfolio gains returns over the year",
    xy=(0.5, 525000),
    xytext=(1, 525000 - 25000),
    arrowprops=dict(arrowstyle="-", relpos=(0, 0.5)),
    fontsize=8
)


# plt.annotate(
#     "Drop Point",  # Text
#     xy=(0, 1700000),  # Point to annotate
#     xytext=(0 + 1, 1700000 + 0.2),  # Offset text position
#     arrowprops=dict(arrowstyle="->", color="grey"),  # Line style
#     fontsize=12,
#     color="grey"
# )

plt.ylim([450000, 650000])

ax.set_xticks([0, 1, 2, 3])
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"Year {(x + 1):.0f}"))

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))

plt.show()
```

However, the real-world is not so kind, and stock performance can vary greatly year-to-year. Perhaps the worst time to invest would have been in the year 1999. The world would soon go through two back-to-back recessions, one in 2001 and the other in 2008. Let's see how our 12x portfolio fares against real data from that time period:

```{code-cell} ipython3
:tags: [remove-input]

threshold_factor_balance_history = {
    12: []
}

for k in threshold_factor_balance_history.keys():
    yearly_expenses = 48000
    starting_investment = yearly_expenses * k
    investment_balance_history = []
    
    experiment_period = df["S&P 500 TR"].dropna()[-25:-10]
    investment_balance = starting_investment
    
    for year_pct_change in experiment_period:
        if investment_balance < yearly_expenses:
            investment_balance = 0
        else:
            investment_balance -= yearly_expenses
            investment_balance *= year_pct_change
    
        threshold_factor_balance_history[k].append(investment_balance)

fig, ax = plt.subplots()

plt.plot(experiment_period.index, threshold_factor_balance_history[12])

plt.scatter(dt.datetime(2000, 1, 1), 100000, s=5, c="k")
plt.text(dt.datetime(2000, 1, 1), 150000, "dot-com\nbubble", ha="center", va="bottom", fontsize=8)

plt.scatter(dt.datetime(2008, 1, 1), 100000, s=5, c="k")
plt.text(dt.datetime(2008, 1, 1), 150000, "GFC", ha="center", va="bottom", fontsize=8)

plt.title(f"Simulated Portfolio {experiment_period.index[0].year}-{experiment_period.index[-1].year}")

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))

plt.show()
```

In the face of overwhelming downturn, our portfolio can no longer keep up with our yearly expenses. The deduction continually outsizes the portfolio's returns, which slowly exhausts our capital to zero. So how do we get around this problem? How can we ensure that luck is on our side? Rather than rely on chance, we establish certainty through sheer brute force.

Instead of aiming for a 12x portfolio, let's increase that all the way to 35x. A 35x portfolio would equal $\$48\text{k} \times 35 = ~\$1.7\text{M}$. And although that seems like a lot compared to before, let's see how our 35x portfolio fairs against the same scenario:

```{code-cell} ipython3
:tags: [remove-input]

threshold_factor_balance_history = {
    12: [],
    35: []
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

plt.plot(experiment_period.index, threshold_factor_balance_history[35])
plt.plot(experiment_period.index, threshold_factor_balance_history[12], linestyle="dotted")

plt.scatter(dt.datetime(2000, 1, 1), 100000, s=5, c="k")
plt.text(dt.datetime(2000, 1, 1), 150000, "dot-com\nbubble", ha="center", va="bottom", fontsize=8)

plt.scatter(dt.datetime(2008, 1, 1), 100000, s=5, c="k")
plt.text(dt.datetime(2008, 1, 1), 150000, "GFC", ha="center", va="bottom", fontsize=8)

plt.scatter(dt.datetime(2020, 1, 1), 100000, s=5, c="k")
plt.text(dt.datetime(2020, 1, 1), 150000, "COVID", ha="center", va="bottom", fontsize=8)

plt.title(f"Simulated Portfolio {experiment_period.index[0].year}-{experiment_period.index[-1].year}")
plt.legend(["35x", "12x"])

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000000:.1f}M"))

plt.show()
```

The increased size of the 35x portfolio provides leeway in face of economic downturn, allowing it in this timeline to survive through three major recessions. Tested on 100 years of historical data, a 35x portfolio is the minimum sized portfolio to have a 100% perpetual rate - surviving through events such as WW2, the Cold War, and all [US recessions throughout history](https://www.investopedia.com/articles/economics/08/past-recessions.asp).

For such a strategy to fail, a catastrophic event - quite literally never before seen in history - would need to occur. This would be akin to something like nuclear war, which at such a point, would make money, society, along with the fate of your investment strategy, irrelevant.

I hope this information provides you with solid grounds to pursue a 35x portfolio as a retirement investment. It is a strategy that relies neither on luck nor expertise, but only the assumption of continuing century-long economic trends.
