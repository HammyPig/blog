---
icon: "{fas}`money-bill`"
date: "2024-04-18"
---

# Retirement

To begin investing, we first need to understand what we are working towards. We know that the ultimate end-goal is an early retirement. But what does retirement mean? And when does it occur?

The most common consensus is that at 65, you would have saved enough money which will last until you die. Quite literally, the article I sourced this from stated that “the amount to save depends on how long you expect to live”, then quoting the fact that “on average, most people live 15 to 20 years after turning 65.” A great plan to be able to afford a retirement home to spend your last days in.

While this sounds like terrible advice, this is the reality planned for most people. The Australian government, for example, has arbitrarily chosen that only after you reach 65 are you able to gain access to your super (retirement) fund. The government does not trust you to create your own retirement plan, and has instead forced this reality upon you. This is not ideal.

The alternative then is to plan one yourself. First we should discard the fixed age. It’s nonsensical to set a fixed age if our individual circumstance could help us retire earlier. If age is now variable, we then cannot simply rely on a fixed amount to save, but rather, we need to create a type of investment which will cover our yearly living costs indefinitely.

Our ‘years to retirement’ question now becomes a function of 4 variables: retirement living costs, monthly investment amount, investment performance, and initial investment amount.

If our investment will cover our yearly living costs indefinitely, it means that the interest alone is greater than or equal to our living cost. We can then calculate our target investment amount as follows:

```py
targetInvestment = livingCost / investmentPerformance
```

After which, we can then simulate how long it would take to reach this target by consistently adding our monthly investment amount, in addition to the compounding effect of the investment performance over time. Our overall function then takes the following form:

```py
def years_to_retirement(living_cost, monthly_investment, investment_performance, initial_investment_amount):

    target_investment_amount = living_cost / investment_performance
    investment_amount = initial_investment_amount
    months = 0

    while investment_amount < target_investment_amount:
        investment_amount = investment_amount * (1 + investment_performance / 12) + monthly_investment
        months += 1

    years = months / 12
    return years
```

Now we have a definite way to determine when we retire.
