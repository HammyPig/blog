---
icon: "{fas}`book`"
date: "2024-09-07"
---

# Web Scraping Notes

## Scraping static and dynamic sites

In web scraping there are two categories of sites:

- static
- dynamic

Static sites are simple HTML sites that can be scraped easily:

```py
from urllib.request import urlopen

def get_html_from_static_site(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    return html
```

But sometimes when attempting to scrape a site, the scraped html does not match what you see in your browser. Most likely it is because the site is dynamic, which means it uses JavaScript that only properly converts into HTML after being rendered by your browser. You can mimick this rendering step by using this slightly slower method:

```py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def get_html_from_dynamic_site(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    html = driver.page_source
    driver.quit()

    return html
```

## Extracting information from raw HTML

Once you have the raw HTML from either of these methods, you then pass it into `BeautifulSoup`, which transforms the raw html into a searchable object.

```py
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
```

Now begins the process of extracting information from the page. Usually there are three things that you commonly want to scrape from a web page:

- an element on the page
- multiple elements with the same format found across the page
- multiple elements of the same format contained inside a specific section

## Extracting information from a specific element

To extract content from a specific section of the page, locate the element on your browser and inspect its properties. The element may be wrapped in a tag that has unique properties such as a specific id or class. You can use these properties to locate the element in the `soup` object, and then extract its text:

```py
temperature = soup.find("div", {"class": "temperature-summary"})
print(temperature.get_text(strip=True))
```

You can also use more advanced arbitrary conditions:

```py
tables = soup.find_all("table", {"class": lambda x: x and x.startswith("Table ")})
```

## Extracting multiple elements with the same properties

If there are multiple elements of the same properties that you want to scrape, you can use the `find_all()` method:

```py
temperature_readings = soup.find_all("div", {"class": "temperature-summary"})

for temperature in temperature_readings:
    print(temperature.get_text(strip=True))
```

## Extracting multiple elements contained inside a specific section

Sometimes you only want to extract information from a certain section, and not the entire page. To do so, you use a combination of the above methods. First you need to locate the tag that wraps only the content you want. Then, using the parent tag, you can iterate through each child tag:

```py
shopping_list = soup.find("div", {"class": "shopping-list"})
shopping_list = shopping_list.find_all("div", {"class": "shopping-list-item"}, recursive=False)

for item in shopping_list:
    print(item.get_text(strip=True))
```

The `recursive=False` flag ensures that you only search for immediate child tags, as the default behaviour will recurse through the entire section.

## Comprehensive example of web scraping

To tie everything together, let's say you want to extract a table from a webpage:

```html
 <table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
</table> 
```

To parse it while keeping its structure would require something like the following:

```py
table = soup.find("table") # find the tag that wraps the entire section
table_rows = table.find_all("tr", recursive=False) # get all child tags

column_names = table_rows[0] # get the first row of the table
column_names = column_names.find_all("th", recursive=False) # get each column from the header row
column_names = [x.get_text(strip=True) for x in column_names] # extract the text of each column

rows = []
for row in table_rows[1:]: # iterate through each row, ignoring the header row
    row = row.find_all("td") # get each column
    row = [x.get_text(strip=True) for x in row] # extract the text from each column
    rows.append(row)
```

This could then be converted into something like a Pandas dataframe:

```py
df = pd.DataFrame(rows, columns=column_names)
```
