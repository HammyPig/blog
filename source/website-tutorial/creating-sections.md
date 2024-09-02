# Grouping Pages into Sections

Sections are larger parts of your website which consist of a group of related pages.

The page you are currently on is an example of a page inside a section. This is because you can see a left sidebar, where you can quickly navigate to related pages - as opposed to a standalone page like our home page.

## Creating a Section folder

Inside your `source/` folder, create a section folder (e.g. `website-tutorial/`).

Now drag whatever pages you want to group into the folder. In this example, I have 3 pages I wanted to group:

```
website-tutorial/
├── example-page1.md
├── example-page2.md
└── example-page3.md
```

## Creating a `_toc.md` section file

Inside the same section folder, create a file named `_toc.md`. This is where you specify which pages are part of the section.

```
:::{toctree}
example-page1
example-page2
example-page3
:::
```

The order you specify these pages in will determine how they are ordered on your website.

## Adding the section into `_sections.md`

Finally, you'll need to navigate to the `_sections.md` file located in the `source/` folder. Then add the `_toc.md` file path into this files `toctree`:

```
:::{toctree}
website-tutorial/_toc
:::
```
