# Viewing Pages Locally

Before learning how to create and edit pages, let's first learn how to view our pages locally.

Locally simply means we are viewing the pages on our local computer without making changes to the website online.

## Generating web pages

In the project folder, you will notice there is aa `source/` folder. This is where we will put all our `.md` files.

To convert our `.md` files into web pages, run the command:

```sh
make clean && make html
```

This will create a new folder named `build/`.

## Viewing web pages

The template comes with a single page named `index.md` located inside the `source/` folder. Running the above command will generate a corresponding file named `index.html` inside the `build/html/` folder.

To see the web page, navigate to the file and open it up in your browser.

## Making changes to a page

Whenever you make changes to a page and want to see how it looks like, you will need to run the above command again, and then refresh the browser page.
