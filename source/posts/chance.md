---
icon: "{fas}`lightbulb`"
date: "2024-05-07"
---

# Turning Chance Into Certainty

Imagine a toin coss. We know that there is a 50% chance of getting heads. But what about if we toss the coin twice? What is the probability we can get heads then?

Let’s first phrase the question differently: what is the probability of not getting tails at every toss? This yields us the equation (1 – 0.5x) where x is the number of tosses. Graphing this out, we can see that the probability increases as the number of tosses goes up. But when do we reach ‘certainty’?

Nothing in life is certain. Because of this, we first need to define a benchmark of what is considered certain. As a young person, we seem to assume that we possess a certain immortality in our lives. So to be as morbid as possible, let’s use the probability that a 20 year old will die in the next year. You know what, perhaps a year isn’t urgent enough, let’s use the probability of dying today.

The probability that a 20 year old will die in the next year is 0.001373 when male, and 0.000507 when female. To give us the best possible odds, lets use the latter in our benchmark of ‘probabilistic certainty’. Using this, the probability that we will live to the next year is (1 – 0.000507). We can then create an estimate probability of living to the next day: (1 – 0.000507)1/365.

Now our problem simply becomes an equation to solve: (1 – 0.5x) > (1 – 0.000507)1/365. In english, it determines “how many tosses would it take for the probability of getting heads to be more likely than the probability of living to the next day as a 20 year old female.” This equation then derives to x = ⌈log0.5((1 – 0.000507)1/365)⌉, which gives us the result of 19.

By our definition, it is now a certainty that we will get heads given 19 coin tosses.
