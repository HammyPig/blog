---
icon: "{fas}`money-bill`"
date: "2025-07-29"
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

# Modelling Historical Data for a new All-In-One ETF

VDAL is a new all-in-one fund ETF created by Vanguard. Essentially this ETF was brought out by popular demand for a VDHG ETF minus the bonds. Although this new ETF is very promising, its historical data is limited as it was only recently released. Through analysis of its underlying holdings, we can extend this data decades further.

```{code-cell} ipython3
:tags: [remove-input]

import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde
from sklearn.metrics import r2_score
import yfinance as yf

plt.rc("figure", labelsize="x-large", autolayout=True, figsize=(4, 3))
```

```{code-cell} ipython3
:tags: [remove-input]

def normalise_stock_performance(df, rebase_stock=None):
    df = df.copy()
    
    for stock in df.columns:
        # convert to relative cumulative product
        df[stock] = df[stock].pct_change(fill_method=None)
        df[stock] = (df[stock] + 1).cumprod()
    
        # set initial value of cumulative product to 1
        first_valid_index = df[stock].first_valid_index()
        iloc_before_first_valid_index = df[stock].index.get_loc(first_valid_index) - 1
        df.loc[df.index[iloc_before_first_valid_index], stock] = 1

    # get rebase date
    if rebase_stock == None:
         # default to earliest common date
        rebase_date = df.apply(lambda x: x.first_valid_index()).sort_values(ascending=False).iloc[0]
    else:
        rebase_date = df[rebase_stock].first_valid_index()
        
    # scale from rebase date
    for stock in df.columns:
        rebase_value = df[stock].loc[rebase_date]
        df[stock] = df[stock] / rebase_value

    return df

def set_offset_from_first_valid_index(df, col, offset, y):
    first_valid_index = df[col].first_valid_index()
    offset_from_first_valid_index = df[col].index.get_loc(first_valid_index) + offset
    df.loc[df.index[offset_from_first_valid_index], col] = y

def plot_correlation(df, actual, predicted, actual_label, predicted_label):
    fig, axs = plt.subplots(1, 2, figsize=(8, 3))
    
    plot_df = df[[actual, predicted]]
    plot_df = plot_df.dropna()
    plot_df = normalise_stock_performance(plot_df)
    
    axs[0].plot(plot_df[actual])
    axs[0].plot(plot_df[predicted])
    axs[0].set_title("Historical Performance")
    axs[0].legend([actual_label, predicted_label])

    y = plot_df.pct_change(fill_method=None).dropna()
    y_true = y[actual]
    y_pred = y[predicted]
    r2 = r2_score(y_true, y_pred)
    
    axs[1].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()])
    axs[1].scatter(y_true, y_pred, s=1, color=mcolors.TABLEAU_COLORS["tab:orange"], zorder=2)
    axs[1].text(0.1, 0.9, f"R2: {r2:.2f}", transform=axs[1].transAxes)
    axs[1].set_title(f"{actual_label} vs {predicted_label}")

    fig.autofmt_xdate()
    
    plt.show()
```

```{code-cell} ipython3
:tags: [remove-cell]

stocks = ["VDAL.AX", "VDHG.AX"]
stocks += ["VAS.AX", "VGS.AX", "VGAD.AX", "VISM.AX", "VGE.AX"]
stocks += ["IOO.AX", "STW.AX", "IEM.AX"]
df_orig = yf.download(stocks, period="max", group_by="ticker", auto_adjust=False)
```

```{code-cell} ipython3
:tags: [remove-input]

df = df_orig.copy()
df = df.xs("Adj Close", axis=1, level=1)
```

From VDAL's [fact sheet](https://fund-docs.vanguard.com/ETF-Vanguard_Diversified_All_Growth_Index_ETF_F100_FS_VDAL.pdf), we can see its target asset allocation:

| Asset | Target (%) |
|---|---|
| Australian Shares | 40 |
| International Shares | 29.5 |
| International Shares (Hedged) | 18 |
| International Small Companies | 7 |
| Emerging Markets Shares | 5.5 |

Specifically, these assets correspond to five Vanguard ETFs: VAS, VGS, VGAD, VISM, and VGE. All five of these ETFs are much older than VDAL, giving us the data to model VDAL prior to its inception date.

## Model A: Combining Subcomponents

Model A will be created by combining the performance of the five ETFs, weighted accordingly by their target allocations:

```{code-cell} ipython3
:tags: [remove-input]

df["model_a"] = (
    0.40 * df["VAS.AX"].pct_change(fill_method=None) +
    0.295 * df["VGS.AX"].pct_change(fill_method=None) +
    0.18 * df["VGAD.AX"].pct_change(fill_method=None) +
    0.07 * df["VISM.AX"].pct_change(fill_method=None) +
    0.055 * df["VGE.AX"].pct_change(fill_method=None)
)

df["model_a"] = (df["model_a"] + 1).cumprod()
set_offset_from_first_valid_index(df, "model_a", -1, 1)
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plot_df = df[["model_a"]]
plot_df = normalise_stock_performance(plot_df)

ax.plot(plot_df["model_a"])

ax.set_title("Model A Historical Performance")
fig.autofmt_xdate()

plt.show()
```

Let's then verify how accurate our model is by comparing it to the available data from VDAL:

```{code-cell} ipython3
:tags: [remove-input]

plot_correlation(df, "VDAL.AX", "model_a", "Actual", "Model A")
```

The strong correlation gives us confidence that the rest of the predicted data past VDAL's inception date is reliable.

## Model B: Actual + Model A

We wouldn't want to waste the original data, so to give us the most accurate model, we instead combine the two sets by first using the available VDAL data, and then filling in the rest with the predicted values. We then call this new combination model B.

```{code-cell} ipython3
:tags: [remove-input]

df["model_b"] = (
    df["VDAL.AX"].pct_change(fill_method=None)
    .fillna(df["model_a"].pct_change(fill_method=None))
)

df["model_b"] = (df["model_b"] + 1).cumprod()
set_offset_from_first_valid_index(df, "model_b", -1, 1)
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plot_df = df[["model_b"]]
plot_df = normalise_stock_performance(plot_df)

ax.plot(plot_df["model_b"][df["VDAL.AX"].first_valid_index():])
ax.plot(plot_df["model_b"][:df["VDAL.AX"].first_valid_index()])

ax.set_title("Model B Historical Performance")
ax.legend(["Actual Component", "Model A Component"])
fig.autofmt_xdate()

plt.show()
```

We now have a confident prediction of VDAL's historical data stretching more than six years further into the past.

## Model C: Absorbing VISM into VGS

When looking at the five subcomponent ETFs, I noticed that VISM's inception date is significantly later than the rest.

I chose to absorb VISM into VGS, justifying that VISM (International Small Cap) should perform similarly to VGS (International Large/Mid Cap) due to its similar regional exposure. Additionally, because VISM only makes up a small fraction of VDAL, any minor difference caused by this substitution should turn negligible. By creating this new model, the available data would stretch back a further four years.

Let's first test our assumptions by comparing the VISM and VGS:

```{code-cell} ipython3
:tags: [remove-input]

plot_correlation(df, "VISM.AX", "VGS.AX", "VISM", "VGS")
```

As thought, VISM and VGS share a moderate correlation. This difference should then diminish further when placed into our new overall allocation:

**Model C Allocation**

| Asset | Allocation (%) |
|---|---|
| Australian Shares | 40 |
| International Shares | 36.5 |
| International Shares (Hedged) | 18 |
| Emerging Markets Shares | 5.5 |

```{code-cell} ipython3
:tags: [remove-input]

df["model_c"] = (
    0.40 * df["VAS.AX"].pct_change(fill_method=None) +
    (0.295 + 0.07) * df["VGS.AX"].pct_change(fill_method=None) +
    0.18 * df["VGAD.AX"].pct_change(fill_method=None) +
    0.055 * df["VGE.AX"].pct_change(fill_method=None)
)

df["model_c"] = (df["model_c"] + 1).cumprod()
set_offset_from_first_valid_index(df, "model_c", -1, 1)
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plot_df = df[["model_c"]]
plot_df = normalise_stock_performance(plot_df)

ax.plot(plot_df["model_c"])

ax.set_title("Model C Historical Performance")
fig.autofmt_xdate()

plt.show()
```

Now let's compare the difference between VDAL and model C:

```{code-cell} ipython3
:tags: [remove-input]

plot_correlation(df, "VDAL.AX", "model_c", "Actual", "Model C")
```

We can see that our assumptions were correct. No significant change in correlation was observed from this substitution.

## Model D: Model B + Model C

Similarly to before, we reuse the previous model B and fill in the missing values with model C to retain the most accurate predictions:

```{code-cell} ipython3
:tags: [remove-input]

df["model_d"] = (
    df["model_b"].pct_change(fill_method=None)
    .fillna(df["model_c"].pct_change(fill_method=None))
)

df["model_d"] = (df["model_d"] + 1).cumprod()
set_offset_from_first_valid_index(df, "model_d", -1, 1)
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plot_df = df[["model_d"]]
plot_df = normalise_stock_performance(plot_df)

ax.plot(plot_df["model_d"][df["model_b"].first_valid_index():])
ax.plot(plot_df["model_d"][:df["model_b"].first_valid_index()])

ax.set_title("Model D Historical Performance")
ax.legend(["Model B Component", "Model C Component"])
fig.autofmt_xdate()

plt.show()
```

## Model E: Substituting Older ETFs

Further data can be obtained by substituting components with older alternatives that have similar regional exposure:

- VGS (International Large/Mid Cap) and VGAD (International Large/Mid Cap Hedged) can be combined and substituted with IOO (International Top 100).
- VAS (Australian Shares) with STW (Australian Top 200)
- VGE (Emerging Markets Shares) with IEM (Emerging MarketsShares)

Let's first look at how similar these substitutions are:

```{code-cell} ipython3
:tags: [remove-input]

plot_correlation(df, "VGS.AX", "IOO.AX", "VGS", "IOO")
plot_correlation(df, "VGAD.AX", "IOO.AX", "VGAD", "IOO")
plot_correlation(df, "VAS.AX", "STW.AX", "VAS", "STW")
plot_correlation(df, "VGE.AX", "IEM.AX", "VGE", "IEM")
```

All substitutes have moderate to strong correlations with their original. Let's then construct model E using the new substituted allocation:

| Asset | Allocation (%) |
|---|---|
| STW | 40 |
| IOO | 54.5 |
| IEM | 5.5 |

```{code-cell} ipython3
:tags: [remove-input]

df["model_e"] = (
    0.40 * df["STW.AX"].pct_change(fill_method=None) +
    (0.295 + 0.07 + 0.18) * df["IOO.AX"].pct_change(fill_method=None) +
    0.055 * df["IEM.AX"].pct_change(fill_method=None)
)

df["model_e"] = (df["model_e"] + 1).cumprod()
set_offset_from_first_valid_index(df, "model_e", -1, 1)
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plot_df = df[["model_e"]]
plot_df = normalise_stock_performance(plot_df)

ax.plot(plot_df["model_e"])

ax.set_title("Model E Historical Performance")
fig.autofmt_xdate()

plt.show()
```

Now we again compare model E to the VDAL:

```{code-cell} ipython3
:tags: [remove-input]

plot_correlation(df, "VDAL.AX", "model_e", "Actual", "Model E")
```

Model E shows strong correlation to the actual data.

## Model F: The Amalgamation of Four Models

Once again, to retain the most accurate results, we construct model F by combining model D and E. What's left is then an amalgamation of four different models that slightly wane with accuracy the further into the past they go.

```{code-cell} ipython3
:tags: [remove-input]

df["model_f"] = (
    df["model_d"].pct_change(fill_method=None)
    .fillna(df["model_e"].pct_change(fill_method=None))
)

df["model_f"] = (df["model_f"] + 1).cumprod()
set_offset_from_first_valid_index(df, "model_f", -1, 1)
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plot_df = df[["model_f"]]
plot_df = normalise_stock_performance(plot_df)

ax.plot(plot_df["model_f"][df["model_d"].first_valid_index():])
ax.plot(plot_df["model_f"][:df["model_d"].first_valid_index()])

ax.set_title("Model F Historical Performance")
ax.legend(["Model D Component", "Model E Component"])
fig.autofmt_xdate()

plt.show()
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots()

plot_df = df[["model_f"]]
plot_df = normalise_stock_performance(plot_df)

ax.plot(plot_df["model_f"][df["VDAL.AX"].first_valid_index():])
ax.plot(plot_df["model_f"][df["model_a"].first_valid_index():df["VDAL.AX"].first_valid_index()])
ax.plot(plot_df["model_f"][df["model_c"].first_valid_index():df["model_a"].first_valid_index()])
ax.plot(plot_df["model_f"][df["model_e"].first_valid_index():df["model_c"].first_valid_index()])

ax.set_title("Model F: The Amalgamation")
ax.legend(["Actual Component", "Model A Component", "Model C Component", "Model E Component"])
fig.autofmt_xdate()

plt.show()
```

We have turned what originally was less than a year of data into something decades long.
