# Sphinx Site Log

## 12/08/2024

### Running the Sphinx quickstart command

When researching the documentation online, I found that Sphinx comes with a command to quickly setup our project folder.[^sphinx-quickstart]

[^sphinx-quickstart]: <https://www.sphinx-doc.org/en/master/usage/quickstart.html>

I noticed that the command by default asks you some prompts in the setup process. I found this a bit clunky. And because I originally was going to include this section in the main tutorial, I wanted to know if I could instead somehow specify flags to disable this functionality to make it more seamless. I then found that this was indeed possible.[^sphinx-quickstart-flags]

[^sphinx-quickstart-flags]: <https://www.sphinx-doc.org/en/master/man/sphinx-quickstart.html>

I then ran the modified command which included the new flags in the project folder:

```
sphinx-quickstart -q --sep -p=PROJECT -a=AUTHOR
```

To explain the flags:
- `-q` skips the interactive prompts.
- `--sep` better organises the project by creating separate source and build folders.
- `-p` and `-a` are required flags when using `-q`, and are used to set the project name and author variables in the generated `conf.py` file.

Running the command created a bunch of files and folders that looked like this:

```
build/
source/
├── _static
├── _template
├── conf.py
└── index.rst
make.bat
Makefile
```

### Deleting unnecessary files

I noticed that the `_static/` and `_template/` folders were empty, so I deleted them to reduce the clutter as I wanted to provide anyone who used this template as clean of a setup as possible. I also deleted the default `index.rst` since I wanted to use `.md` files over `.rst`, and keeping `.rst` around seemed unintuitive. The folder now looked like this:

```
build/
source/
└── conf.py
make.bat
Makefile
```

To explain the current state of the folder:
- `source/` will contain all the `.md` and `.ipynb` files we wish to upload to our website.
- `make.bat` and `Makefile` will be used to convert the files in `source/` into web pages.
- `build/` is where the converted files (now written in HTML etc.) are stored.
- `source/conf.py` is where we can configure the Sphinx site (e.g. set a theme).

### Adding extensions

Earlier I installed a bunch of Sphinx extensions in my Dockerfile. We can now finally enable them on the site through the `conf.py` file.

Inside the file, you will find the line: `extensions = []`. To add our extensions, I edited the line to the following:

```python
extensions = ["myst_nb", "sphinx_design", "sphinx_copybutton"]
```

- [myst-nb](https://myst-nb.readthedocs.io/en/latest/): Makes `.md` and `.ipynb` files compatible with Sphinx.
- [sphinx-design](https://sphinx-design.readthedocs.io/en/latest/): Allows the creation of more complex web components such as cards.
- [sphinx-copybutton](https://sphinx-copybutton.readthedocs.io/en/latest/): Adds a copy button to code snippets that website viewers can use to easily copy code.

### Setting the theme

Inside the same `conf.py` file, I set the theme by locating the line: `html_theme = 'alabaster'` and editing it to the following:

```python
html_theme = "pydata_sphinx_theme"
```

The Sphinx site has now been configured with its theme and all necessary extensions.

## 07/09/2024

### Inconsistencies in local preview

When adding buttons to my site, I omit the `.html` as the live site does not include it in URLs, however, when I view the website locally, I would need to add the `.html`, otherwise the file of course is not present on my computer.

There are also other funny issues with Sphinx. For instance, if you edit a page title which is in a section, you will find that when navigating to other pages in the same section, the page title remains old.

### Discovering the `sphinx-autobuild` extension

When browsing broadly online for helpful Sphinx extensions[^best-sphinx-extensions], I came across `sphinx-autobuild`.

[^best-sphinx-extensions]: https://sphinx-extensions.readthedocs.io/en/latest/

Much like how React works, it creates a local server which mimics a live one. Because of this, I would no longer need to edit the URL just to find the correct file.

Additionally, it fixed the second problem. The primary feature of this extension was that it would detect changes and update the preview live - even those which indirectly altered other pages.

I first installed the `sphinx-autobuild` package by editing my `Dockerfile`. I should note that I didn't need to add the extension to my site for it to work.

Then to make it actually work, you need to run the following command:

```
sphinx-autobuild -a -b dirhtml source build
```

- **-a**: Detect changes which indirectly alter pages.
- **-b dirhtml**: Removes the `.html` postfix from URLs.
- **source build**: Specifies source and build folder names.

### Running `sphinx-autobuild` automatically

To go further, I added the above command to the `postStartCommand` field in the `devcontainer.json` file. This means that whenever the project is ran, the local server is automatically launched without any command from the user.

And with that, one more problem had been fixed.
