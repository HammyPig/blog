---
icon: "{fas}`money-bill`"
date: "2025-07-10"
---

# Stock Market Analysis Using Python

## Downloading stock market data into Python

To first import stock market data, you can use `yfinance`:

```py
import yfinance as yf

stocks = ["VGS.AX", "VAS.AX"]
df = yf.download(stocks, period="max", group_by="ticker", auto_adjust=False)
```

Doing so will create a dataframe object that contains attributes (downloaded from Yahoo Finance) from every trading day of each stock's lifetime:

```py
print(df["VGS.AX"]["Open"]) # list daily open prices
print(df["VGS.AX"]["Close"]) # list daily close prices
print(df["VGS.AX"]["Volume"]) # list daily volume
print(df["VAS.AX"]["Adj Close"]) # list close prices, accounting for dividends reinvested
```

## Normalising stock performance

One simple analysis is to compare the performance of one stock to another. Most likely, you will first want to normalise the stock price so you can directly view stock growth as a percentage, rather than compare its raw dollar amount:

```py
for stock in df.columns:
    # change to cumulative product
    df[stock]["normalised_performance"] = df[stock].pct_change(fill_method=None)
    df[stock]["normalised_performance"] = (df[stock]["normalised_performance"] + 1).cumprod()

    # set initial value
    first_valid_index = df[stock]["normalised_performance"].first_valid_index()
    iloc_before_first_valid_index = df[stock]["normalised_performance"].index.get_loc(first_valid_index) - 1
    df.loc[df.index[iloc_before_first_valid_index], stock] = 1
```

One issue is that because different stocks have different starting dates, the normalised values are unproportionate. For example, if two stocks had the same annual growth, but one started 10 years prior, the normalised value of the older stock will be much larger than the newer stock.

To solve this, you can rebase the normalised value so that each stock starts at 1 at the same time, where you can set the rebase date to be the youngest stock's first date.

```py
rebase_date = df.apply(lambda x: x.first_valid_index()).sort_values().iloc[-1]
for stock in df.columns:
    rebase_value = df[stock]["normalised_performance"].loc[rebase_date]
    df[stock]["normalised_performance"] = df[stock]["normalised_performance"] / rebase_value
```

## Creating visualisations of stock performance

Finally, you can visualise a simple analysis using `matplotlib`:

```py
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for stock in stocks:
    ax.plot(df[stock]["normalised_performance"])

ax.set_title("Historical Performance")
ax.legend(stocks.columns)

plt.show()
```

## Backtesting trading strategies

To simulate a trading strategy, you can iterate through each day and simulate trades based on certain conditions:

```py
cash = 10000
portfolio = {
    "VGS.AX": 0
    "VAS.AX": 0
}

# Iterate through everyday
for row in df.itertuples():
    if stock["VGS.AX"]["Close"] > 50:
        # do something
```
