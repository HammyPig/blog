---
icon: "{fas}`lightbulb`"
date: "2024-09-08"
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

# Chasing Summers

:::{note}
This post does not consist of any formal research effort and is more of a fun exploration of a random topic.
:::

After living through Melbourne's winter, I now have a greater appreciation of the sun. This lead me thinking. I love living in the sun, which means that ideally I would live in two cities: one in the northern hemisphere and one in the south. I could then live an endless summer by switching cities whenever winter loomed. But here is the question, what two cities would I select?

```{code-cell} ipython3
:tags: [remove-input]

from urllib.request import urlopen
from bs4 import BeautifulSoup
from unidecode import unidecode
from IPython.display import display, Markdown
from cycler import cycler
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as patches

plt.style.use("default")
plt.rc("figure", labelsize="x-small", autolayout=True, figsize=(4, 3), facecolor="white")
plt.rc("xtick", labelsize="x-small")
plt.rc("ytick", labelsize="x-small")

custom_colors = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
    "#FF97FF",
    "#FECB52"
]

plt.rc('axes', prop_cycle=cycler('color', custom_colors))
```

```{code-cell} ipython3
:tags: [remove-input]

def scrape_static_site(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    return html

def get_wiki_city_climate_df(city):
    html = scrape_static_site("https://en.wikipedia.org/wiki/" + city)

    # get html table
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    climate_table = None
    for table in tables:
        th = table.find("th")
        if "Climate data for " in th.text:
            climate_table = table
            break

    # convert html table into df
    climate_table_rows = climate_table.find_all("tr")
    
    header = [x.text.strip() for x in climate_table_rows[1].find_all("th")]

    rows = []
    for row in climate_table_rows[2:]:
        rows.append([x.text.strip() for x in row.find_all(["th", "td"])])

    df = pd.DataFrame(rows, columns=header)

    # format df
    df = df.transpose()

    df.columns = df.iloc[0]
    df = df[1:]

    df.drop

    for col in df.columns:
        if "°C (°F)" in col:
            df[col] = df[col].str.split("(").str[0]
            df.rename(columns={col: col.replace("°C (°F)", "°C")}, inplace=True)
        elif "°F (°C)" in col:
            df[col] = df[col].str.split("(").str[1].str.replace(")", "")
            df.rename(columns={col: col.replace("°F (°C)", "°C")}, inplace=True)
        elif "mm (inches)" or "cm (inches)" in col:
            df[col] = df[col].str.split("(").str[0]
            df.rename(columns={col: col.replace(" (inches)", "")}, inplace=True)

    df.drop(columns=[col for col in df.columns if col.startswith("Source")], inplace=True)
    df = df[:-1]

    df = df.apply(lambda x: x.str.replace(",", ""))
    df = df.apply(lambda x: x.str.replace("−", "-"))
    df = df.apply(pd.to_numeric)

    return df

def get_wiki_livable_cities_df():
    html = scrape_static_site("https://en.wikipedia.org/wiki/Global_Liveability_Ranking")

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    table_rows = table.find_all("tr")

    header = [x.text.strip() for x in table_rows[0].find_all("th")]
    rows = []
    for row in table_rows[1:]:
        parsed_row = [x.text.strip() for x in row.find_all("td")]
        if len(parsed_row) == 2:
            parsed_row.insert(0, None)
            parsed_row.insert(2, None)

        rows.append(parsed_row)

    df = pd.DataFrame(rows, columns=header)
    df.ffill(inplace=True)

    return df
```

To narrow down my search, I limited my selection to the top 10 most livable cities as chosen by the EIU.[^most-livable-cities-wiki] These consist of the following:

[^most-livable-cities-wiki]: https://en.wikipedia.org/wiki/Global_Liveability_Ranking

```{code-cell} ipython3
:tags: [remove-input]

df = get_wiki_livable_cities_df()
cities_of_interest = [unidecode(x) for x in df["City"]]
markdown = ""
for city in cities_of_interest:
    markdown += f"- {city}\n"

display(Markdown(markdown))
```

After being traumatised by Melbourne's perpetual winters, the next questions became obvious: how warm and sunny are these cities?

## Monthly temperature of different cities

Let's first start with temperature. I found online that the ideal temperature for humans to live in is between 20°C and 25°C, otherwise known by its fancy term: the 'thermalneutral' zone.[^ideal-temperature]

[^ideal-temperature]: http://www.atmo.arizona.edu/students/courselinks/fall12/atmo336/lectures/sec1/comfort.html

Because of my summer bias, however, I opted to extend this 'optimal' range all the way to 30°C.

Below I then graphed out the monthly temperatures of our candidate cities, with our warm 20°C to 30°C goldilocks zone highlighted in green.

```{code-cell} ipython3
:tags: [remove-input]

city_climates = {}

for city in cities_of_interest:
    city_climates[city] = get_wiki_city_climate_df(city.replace(" ", "_"))
```

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots(figsize=(6, 3))

for city in cities_of_interest:
    plt.plot(city_climates[city]["Mean daily maximum °C"], marker=".")

ax.add_patch(patches.Rectangle((0, 20), 11, 10, color="#a6cda6"))

ax.set_title("City Temperature Cycles")
ax.set_ylabel("Mean daily maximum")
ax.legend(cities_of_interest, bbox_to_anchor=(1, 1))
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.0f}°C"))

plt.show()
```

When looking at Sydney and Vienna, you can see that their temperatures exactly align when winter approaches for either city. It seems we have our best candidates.

## Daily sunshine of different cities

Next, we move onto sunshine. This metric is measured in 'sunshine hours', which as the name suggests, simply means how many hours are spent in sunshine per day. Here we simply prefer higher results over lower ones.

```{code-cell} ipython3
:tags: [remove-input]

fig, ax = plt.subplots(figsize=(6, 3))

for city in cities_of_interest:
    plt.plot(city_climates[city]["Mean monthly sunshine hours"] / (365/12), marker=".")

ax.set_title("Daily Sunshine of Different Cities")
ax.set_ylabel("Mean Daily Sunshine Hours")
ax.legend(cities_of_interest, bbox_to_anchor=(1, 1))
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.0f}h"))

plt.show()
```

As we can see, our previous candidates of Vienna and Sydney still hold up. Although Sydney is already quite consistent with sunshine, the objective improvement of Vienna's summer sunshine over Sydney's fairer winter is still appreciated.

Anyway, so in conclusion, Vienna and Sydney seem good. Again, to reiterate, this research is nothing formal and was just something I found fun, so hope it was interesting!
