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

# Chasing Summers

:::{note}
This post does not consist of any formal research effort and is more of a fun exploration of a random topic.
:::

After living through Melbourne's winter, I now have a greater appreciation of the sun. This lead me thinking. I love living in the sun, which means that ideally I would live in two cities: one in the northern hemisphere and one in the south. I could then live an endless summer by switching cities whenever winter loomed. But here is the question, what two cities would I select?

```{code-cell} ipython3
:tags: [remove-input]

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "ggplot2"
from unidecode import unidecode
from IPython.display import display, Markdown
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

```{code-cell} ipython3
:tags: [remove-input]

city_climates = {}

for city in cities_of_interest:
    city_climates[city] = get_wiki_city_climate_df(city.replace(" ", "_"))
```

```{code-cell} ipython3
:tags: [remove-input]

fig = go.Figure()
for city in cities_of_interest:
    fig.add_trace(go.Scatter(x=city_climates[city].index, y=city_climates[city]["Mean daily maximum °C"], name=city))

fig.add_hrect(y0=20, y1=30, fillcolor="green")

fig.update_layout(
    title="Monthly Temperature of Different Cities",
    legend_title="City",
    xaxis_title="Month",
    yaxis_title="Mean Daily Maximum",
    yaxis_ticksuffix="°C"
)

fig.show()
```

If you select only Sydney and Vienna **(by double clicking Sydney in the legend and then enabling Vienna)**, you can see that their temperatures exactly align when winter approaches for either city. It seems we have our best candidates.

## Daily sunshine of different cities

Next, we move onto sunshine. This metric is measured in 'sunshine hours', which as the name suggests, simply means how many hours are spent in sunshine per day. Here we simply prefer higher results over lower ones.

```{code-cell} ipython3
:tags: [remove-input]

fig = go.Figure()
for city in cities_of_interest:
    fig.add_trace(go.Scatter(
        x=city_climates[city].index,
        y=city_climates[city]["Mean monthly sunshine hours"] / (365 / 12),
        name=city,
        hovertemplate="%{y:.2f}"
    ))

fig.update_layout(
    title="Daily Sunshine of Different Cities",
    legend_title="City",
    xaxis_title="Month",
    yaxis_title="Mean Daily Sunshine Hours"
)

fig.show()
```

As we can see, our previous candidates of Vienna and Sydney still hold up. Although Sydney is already quite consistent with sunshine, the objective improvement of Vienna's summer sunshine over Sydney's fairer winter is still appreciated.

Anyway, so in conclusion, Vienna and Sydney seem good. Again, to reiterate, this research is nothing formal and was just something I found fun, so hope it was interesting!
