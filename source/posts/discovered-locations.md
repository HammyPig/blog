---
icon: "{fas}`map`"
date: "2024-10-30"
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

# Discovered Locations

```{code-cell} ipython3
:tags: [remove-input]

import geopandas
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
:tags: [remove-input]

def plot_map(geojson, highlighted_locations, locations_column_name):
    fig, ax = plt.subplots()
    plt.axis("off")
    fig.set_facecolor("#aad3df")

    geojson.plot(ax=ax, color="#f2efe9")
    geojson.boundary.plot(ax=ax, linewidth=0.5, color="black")

    highlight = geojson[geojson[locations_column_name].isin(highlighted_locations)]
    highlight.plot(ax=ax, color="orange")

    plt.show()
```

## Earth

```{code-cell} ipython3
:tags: [remove-input]

url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/countries.geojson"
locations_column_name = "name"
highlighted_locations = [
    "Australia",
    "United Arab Emirates",
    "Finland",
    "Sweden",
    "Norway",
    "Denmark",
    "Germany",
    "Poland",
    "Czech Republic",
    "Hungary",
    "Austria",
    "Italy",
    "Switzerland",
    "Luxembourg",
    "Netherlands",
    "Belgium",
    "United Kingdom",
    "Ireland",
    "France",
    "Spain",
    "United States of America",
    "Canada"
]

geojson = geopandas.read_file(url)
geojson = geojson.to_crs("ESRI:53030") # Display map using Robinson projection (https://epsg.io/53030).

# Remove regions which distort the map positioning.
removed_regions = ["Antarctica", "Fiji"]
geojson = geojson[~geojson[locations_column_name].isin(removed_regions)]

plot_map(geojson, highlighted_locations, locations_column_name)
```

## Europe

```{code-cell} ipython3
:tags: [remove-input]

url = "https://raw.githubusercontent.com/leakyMirror/map-of-europe/refs/heads/master/GeoJSON/europe.geojson"
locations_column_name = "NAME"
highlighted_locations = [
    "Finland",
    "Sweden",
    "Norway",
    "Denmark",
    "Germany",
    "Poland",
    "Czech Republic",
    "Hungary",
    "Austria",
    "Italy",
    "Switzerland",
    "Luxembourg",
    "Netherlands",
    "Belgium",
    "United Kingdom",
    "Ireland",
    "France",
    "Spain"
]

geojson = geopandas.read_file(url)
geojson = geojson.to_crs("EPSG:3035") # Set map projection (https://epsg.io/3035).

# Remove regions not part of Europe (https://en.wikipedia.org/wiki/Europe#List_of_states_and_territories)
removed_regions = ["Azerbaijan", "Armenia", "Cyprus", "Georgia", "Israel", "Turkey"]
geojson = geojson[~geojson[locations_column_name].isin(removed_regions)]

plot_map(geojson, highlighted_locations, locations_column_name)
```

## Australia

```{code-cell} ipython3
:tags: [remove-input]

url = "https://raw.githubusercontent.com/tonywr71/GeoJson-Data/refs/heads/master/australian-states.json"
highlighted_locations = [
    "Queensland",
    "New South Wales",
    "Victoria",
    "South Australia",
    "Tasmania"
]
locations_column_name = "STATE_NAME"

geojson = geopandas.read_file(url)

plot_map(geojson, highlighted_locations, locations_column_name)
```

## United States

```{code-cell} ipython3
:tags: [remove-input]

url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/refs/heads/master/data/geojson/us-states.json"
highlighted_locations = [
    "Ohio",
    "Illinois"
]
locations_column_name = "name"

geojson = geopandas.read_file(url)

# Remove non-mainland states
removed_regions = ["Alaska", "Hawaii", "Puerto Rico"]
geojson = geojson[~geojson[locations_column_name].isin(removed_regions)]
    
plot_map(geojson, highlighted_locations, locations_column_name)
```

```{code-cell} ipython3

```
