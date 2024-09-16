---
icon: "{fab}`python`"
date: "2024-09-11"
---

# The Quest for a Executable, Publishable, Git-Friendly Python Notebook

After looking at the git differences for my first `.ipynb` post, I realised how ugly jupyter notebooks are in plain text. Essentially they are just large `.json` files with large amounts of useless information.

For example, it was keeping track of cell metadata such as how many times I ran an individual cell. Additionally, it includes entire output results in the file. Git should only consist of source code. Because of this, I set out on a quest to improve this issue.

```{card} Objective: Find a Jupyter Notebook alternative which:
- **Can execute individual cells**: to make development easier.
- **Contains only meaningful data in files:** to make it git-friendly, plus more akin to markdown.
- **Can be converted to a web page by Sphinx:** to make publishing easier.
```

The first idea I had was why jupyter was a `.json` file at all? Because of my experience with RMarkdown, I knew a simple plain text format could achieve the same thing.

I then encountered [MyST Markdown](https://jupyterbook.org/en/stable/content/myst.html), which is stated to draw "heavy inspiration from the fantastic RMarkdown language from RStudio." Exactly what I was looking for then, right? Well, when attempting to integrate it into VS Code, I noticed there was no way to execute cells. And from my understanding, you are only execute code when you compile the entire document. Not great.

However, on the same website, I then saw a YouTube tutorial with executable code cells. It claimed that by running JupyterLab, it was possible! So I went out and setup a dev container, only to realise that the tutorial was only demonstrating - on a regular `.ipynb` file - the extra formatting powers enabled by MyST Markdown. Not very useful.

We then move onto Reddit. I found a [reddit thread](https://www.reddit.com/r/datascience/comments/14gra17/do_you_git_commit_jupyter_notebooks/) which suggested using a tool which clears the metadata and output results from notebooks. And although this doesn't help the hideous `.json` format, it was at least a step in the right direction. [nb-clean](https://pypi.org/project/nb-clean/) automatically cleans `.ipynb` files in commits. To do this, you need to simply install the package, and run the following command in the project folder:

```
nb-clean add-filter
```

In my case, keeping tag metadata was important (as it dictates what cells are hidden etc.), so I ran:

```
nb-clean add-filter --preserve-cell-metadata tags
```

The caveat is that you need to commit the entire file. And to most people this is not an issue. It is only because I am an insane person who commits files line-by-line, which means that I would need to commit the whole file, and then revert lines I didn't want to include in the commit - which is a bit backwards from simply selecting the lines I want to commit.

Another interesting package I came across was [jupytext](https://jupytext.readthedocs.io/en/latest/), which is exactly the plain-text notebook alternative I was looking for. And although my current Sphinx setup only supports .`ipynb` files, it even has a feature which pairs a `.ipynb` file, so that any changes you make to a jupytext file will be reflected in a proper notebook. But then I realised this isn't very helpful considering files need to be commited to the repo before being publishable, so I'd have the exact same problem but with extra fudge on top.

But wait! A random Google result calls for the fact that the [nbsphinx](https://pypi.org/project/nbsphinx/) package (an alternative to the more commonly stated [myst-nb](https://pypi.org/project/myst-nb/)) can in fact publish jupytext files.[^jupytext]

[^jupytext]: https://github.com/mwouts/jupytext/issues/119

But I then found out that `nbsphinx` sucks. It first requires `pandocs` (some random package) to run in the first place. And after that, the conversion is less pretty and also doesn't work with plotly. Another dead-end.
