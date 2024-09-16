---
icon: "{fas}`book`"
date: "2024-09-07"
---

# Web Scraping Notes

In web scraping there are two categories of sites:

- static
- dynamic

To scrape static sites, I use the following:

```py
from urllib.request import urlopen

def scrape_static_site(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    return html
```

To scrape dynamic sites, I use the following:

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

Once you have the raw HTML from either of these methods, you then need to scan for the content you are looking for. For example, if you wanted to find all tables on a page, you would use the following:

```py
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")
```

You can go further by specifying specific details of the elements. For example, if you know the table has a certain class, you can filter for it:

```py
tables = soup.find_all("table", {"class": "my-class"})

# a more complex variant
tables = soup.find_all("table", {"class": lambda x: x and x.startswith("example-")})
```

Parsing something like a paragraph is easy, as you can simply extract the text using the following:

```py
paragraphs = soup.find_all("p")

for p in paragraphs:
    print(p.text)
```

But for something more complex like a table, you need to be more creative. Given a table such as the following:

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
table = soup.find("table")
table_rows = table.find_all("tr")

header = [x.text for x in table_rows[0].find_all("th")]

rows = []
for row in table_rows[1:]:
    rows.append([x.text for x in row.find_all(["td"])])
```

This could then be converted into something like a Pandas dataframe:

```py
df = pd.DataFrame(rows, columns=header)
```
