---
icon: "{fab}`python`"
date: "2024-09-16"
---

# Fixing the cutecharts Python Package

## A mild inconvenience emerges

When my partner in crime was writing their post on [finding fulfillment](https://thecosmogirl.com/general/fulfillment/finding-fulfillment/), they wanted to use this cute data visualisation library named [cutecharts](https://github.com/cutecharts/cutecharts.py). However, to their disappointment, they were unable to get legends to show when rendering the graphs.

## Investigating the issue

They requested my assistance and we both investigated the issue. Going on the library repo, I could see in their documentation that a legend was indeed possible, and this was corroborated by other old blog posts demonstrating the same thing.

I inspected the HTML in hopes of spotting some hidden legend setting that was accidentally set to invisible, but didn't find anything. The only thing I did find was that the render includes a script which references an npm URL (more on this later).

For some context, cutecharts is a python wrapper of the [chart.xkcd](https://www.npmjs.com/package/chart.xkcd) npm package, and we found that even the original library was not rendering the legend, meaning the issue originated from there.

On the [chart.xkcd repo](https://github.com/timqian/chart.xkcd), I then saw that there were a few recent git commits which referenced fixes related to the legend.

Going to the [npm version history](https://www.npmjs.com/package/chart.xkcd?activeTab=versions), I could see that these most recent commits coincide with a version update. I also noted that a previous version had the majority of downloads. Therefore, I concluded that the previous evidence of a legend showing up surely must have been rendered on this older version.

## Solving the problem

Now, remember when I discovered that the HTML references an npm script? Well it looks like this:

```
https://cdn.jsdelivr.net/npm/chart.xkcd@1.1/dist/chart.xkcd.min.js
```

Note the semantic versioning referencing 1.1 (which means 1.1.*), meaning the version we were using was different to what previous people documented.

I knew this URL must have been generated by the Python wrapper, so by searching for the URL in the cutecharts repo source code, I found the file and tweaked the version on my local machine, by editing the `1.1` to `1.1.13`. Lo and behold, the legend showed up once more.
