---
icon: "{fas}`map`"
date: "2024-10-30"
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
    highlight.plot(ax=ax, color="yellow")

    plt.show()
```

## Earth

```{code-cell} ipython3
:tags: [remove-input]

url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/countries.geojson"
highlighted_locations = ["Australia", "United States of America"]
locations_column_name = "name"

geojson = geopandas.read_file(url)
geojson = geojson[geojson["name"] != "Antarctica"]
geojson = geojson.to_crs("EPSG:3857")

plot_map(geojson, highlighted_locations, locations_column_name)
```

## Australia

```{code-cell} ipython3
:tags: [remove-input]

url = "https://raw.githubusercontent.com/tonywr71/GeoJson-Data/refs/heads/master/australian-states.json"
highlighted_locations = ["Queensland", "New South Wales", "Victoria", "South Australia", "Tasmania"]
locations_column_name = "STATE_NAME"

geojson = geopandas.read_file(url)

plot_map(geojson, highlighted_locations, locations_column_name)
```

## United States

```{code-cell} ipython3
:tags: [remove-input]

url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/refs/heads/master/data/geojson/us-states.json"
highlighted_locations = ["Massachusetts", "Ohio"]
locations_column_name = "name"

geojson = geopandas.read_file(url)
geojson = geojson[geojson["name"] != "Alaska"]
geojson = geojson[geojson["name"] != "Hawaii"]
geojson = geojson[geojson["name"] != "Puerto Rico"]
    
plot_map(geojson, highlighted_locations, locations_column_name)
```
