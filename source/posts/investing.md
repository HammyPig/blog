---
date: "2024-04-17"
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

# Investing

The goal of investing is to reach an early retirement. A typical retirement takes 40 years to achieve. Investing can allow the average person to retire more than an entire decade earlier, potentially multiple decades depending on individual circumstance.

Think of an investment as an amount of money which generates its own wealth. The more money you put in, the more it will generate. A basic example is a high-interest savings account, which generates a percentage of interest per year. However, far better investments exist.

Historically, stocks have provided the best return as an investment, averaging a 9% return per year. But how do we choose which stock to invest in? Rather than gamble on any individual stock, we can instead invest in the stock market as a whole through what is known as an ETF. Think of an ETF as a group of stocks. VGS is an international ETF made up of around a thousand different companies from across the world.

To start we need to setup a Stake account and sign-up to the AUS market. This is known as a brokerage account and is where we can purchase our VGS ETF. Each month, we then set aside as much money as we can and invest in VGS. Depending on your retirement living costs, as well as how much you’re able to invest each month, we can calculate how long it will take to reach retirement.

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import plotly.graph_objects as go
```

```{code-cell} ipython3
:tags: [remove-input]

def years_to_retirement(living_cost, monthly_investments):
    INVESTMENT_PERFORMANCE = 0.04
    INITIAL_INVESTMENT_AMOUNT = 0

    target_investment_amount = living_cost / INVESTMENT_PERFORMANCE
    investment_amount = np.full_like(monthly_investments, INITIAL_INVESTMENT_AMOUNT)
    months = np.zeros_like(monthly_investments)

    MAX_MONTHS = 1000
    for i in range(MAX_MONTHS):
        reached_target = investment_amount >= target_investment_amount
        investment_amount[~reached_target] = investment_amount[~reached_target] * (1 + INVESTMENT_PERFORMANCE / 12) + monthly_investments[~reached_target]
        months[~reached_target] += 1

        if np.all(reached_target): break

    years = np.round(months / 12, 1)
    years[~reached_target] = np.inf

    return years
```

```{code-cell} ipython3
:tags: [remove-input]

living_costs = np.arange(50000, 200001, 10000)
monthly_investments = np.arange(1000, 20001, 100)

fig = go.Figure()
for step in living_costs:
    fig.add_trace(go.Scatter(visible=False, x=monthly_investments, y=years_to_retirement(step, monthly_investments), name=""))

fig.data[0].visible = True

steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)}],
        label=str(living_costs[i])
    )
    step["args"][0]["visible"][i] = True
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Retirement Living Cost: $"},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    title="Retirement Plan",
    xaxis=dict(
        title="Monthly Investment",
        tickprefix="$"
    ),
    yaxis=dict(
        title="Years To Retirement"
    ),
    sliders=sliders
)

fig.update_yaxes(range=[0, 40])

fig.show()
```

By consistenly investing in VGS you can build enough wealth to sustain a lifetime.
