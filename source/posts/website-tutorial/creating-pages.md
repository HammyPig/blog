# Creating New Pages

## Adding a new page

To add a new page beyond our home page, simply create a new `.md` file with some arbitrary name in the `source/` folder.

For example, I may want to create a page about creating a website, so I will add the file `website-tutorial.md` into the `source/` folder, which now looks like this:

```
source/
├── _images/
├── _templates/
├── index.md
└── website-tutorial.md
```

When running the previously mentioned `make clean && make build` command, a corresponding file named `website-tutorial.html` will be generated in the `build/html/` folder.

You can add as many `.md` files as you want to the `source`/ folder, which will all generate a corresponding `.html` file when running `make clean && make build`.

## Creating folders to organise your files

You can also add custom folders to better organise your files. For example, if I want to add images to my `website-tutorial.md` file and don't want to bloat my general `_images/` folder, I may do the following to better organise my folder:

```
source/
├── _images/
├── _templates/
├── website-tutorial/
│   ├── images/
│   │   └── example.png
│   └── website-tutorial.md
└── index.md
```

Of course this is all optional, and you are free to have a chaotic website folder if that suits you best.
