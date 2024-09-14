# GitHub Pages Log

## 13/08/2024

### The dilemma of build files

Intuitively I knew that including build files into a git repository is bad practice. After all, the entire purpose of git is to track source code changes, so to bloat it with arbitrary build code changes isn't ideal.

Because of this choice, GitHub Pages' default behaviour to simply grab the raw web content straight from my repository was no longer possible. I did some research and instead found that I would need to use GitHub Actions.

GitHub Actions is a way to instruct GitHub to run 'jobs' (e.g. terminal commands) given some condition (e.g. when I push to main). This is done by creating `.yml` files in the specific folder named `.github/workflows`.[^github-actions] The idea is that I can instruct GitHub to automatically build the files using the `source` folder, which are then uploaded to GitHub pages.

[^github-actions]: https://docs.github.com/en/actions/writing-workflows/quickstart#creating-your-first-workflow

### Creating the workflow file

I created a file named `build-and-deploy-sphinx-site.yml` in `.github/workflows`. I chose this filename as I simply thought - much like a function name - it best summarised what I wanted the file to do.

Inside the file I had the following:

```yaml
name: Build and Deploy Sphinx Site to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: sphinxdoc/sphinx

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          pip install myst-nb
          pip install pydata-sphinx-theme

      - name: Make static files
        run: make html

      - name: Package and upload artifact of static files
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./build/html

  deploy:
    runs-on: ubuntu-latest
    needs: build
    permissions:
      pages: write
      id-token: write

    steps:
      - name: Deploy uploaded artifact to GitHub Pages
        uses: actions/deploy-pages@v4
```

As its quite a large file, I'll now describe the contents in chunks.

In a workflow, there a three main sections:[^github-actions-syntax]

[^github-actions-syntax]: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions

- **name**: the name of the workflow.
- **on**: used to automatically run the workflow based on some condition.
- **jobs**: what commands you want to be ran.

### Specifying the name of the workflow

```yaml
name: Build and Deploy Sphinx Site to GitHub Pages
```

Much like before, I simply chose this name as I thought it best represented what the file does. This name will show up in the GitHub interface whenever the workflow is being referenced.

### Setting the conditions for the workflow to be ran

```yaml
on:
  push:
    branches: [ main ]
```

Here I'm specifying that I want the workflow to be ran everytime I push to my main branch (which is the default branch of GitHub repositories). This is because I want any changes I make to the website to be realised immediately.

### Specifying the jobs to be ran

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: sphinxdoc/sphinx

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          pip install myst-nb
          pip install pydata-sphinx-theme

      - name: Make static files
        run: make html

      - name: Package and upload artifact of static files
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./build/html

  deploy:
    runs-on: ubuntu-latest
    needs: build
    permissions:
      pages: write
      id-token: write

    steps:
      - name: Deploy uploaded artifact to GitHub Pages
        uses: actions/deploy-pages@v4
```

Now onto the jobs section. This is by far the most complex section. So I'll first describe its layout.

Under `jobs:`, you can specify any number of arbitrary job names. Here I have two job names, which I named `build` and `deploy`. Again, these job names are similar to function names.

Under each individual job, you first specify an environment to run on using `runs-on`, which can be set to any arbitrary Docker image. Then you specify an arbitrary amount of `steps` to perform, which simply consist of commands, or even other entire pre-made GitHub workflows.

:::{note}
When referencing an existing workflow, you are simply using a shortened version of its repository url (e.g. `https://github.com/actions/checkout` becomes `actions/checkout`). Then you are required to reference a specific version (e.g. `actions/checkout` becomes `actions/checkout@v4`).

The version simply comes from looking at the previously mentioned url and checking for the latest release number. Although this may seem redundant, as you can specify to automatically use whatever the latest version is, it is important as it prevents a workflow causing errors after it has been updated with breaking changes.

For example, if a workflow updates from `v4` to `v5`, by version semantics it means it has been updated with breaking changes. This may mean existing flags which you have used will no longer work, and you will be forced to tediously update your workflow file. This process simply avoids all that to save you as much time and effort as possible.
:::

### Job 1: Building the site

```yaml
build:
  runs-on: ubuntu-latest
  container:
    image: sphinxdoc/sphinx

  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Install dependencies
      run: |
        pip install myst-nb
        pip install pydata-sphinx-theme

    - name: Make static files
      run: make html

    - name: Package and upload artifact of static files
      uses: actions/upload-pages-artifact@v3
      with:
        path: ./build/html
```

Under `build`, I'm using a pre-built sphinx Docker container as our environment.

In the `steps` section, there are 4 main actions:

- **Checkout**: a pre-made workflow that grabs the GitHub repository contents for our workflow to use.
- **Install dependencies**: running pip commands to install packages that we need to build our project.
- **Make static files**: runs the  command `make html`.
- **Package and upload artifact of static files**: uses an existing GitHub workflow specifically designed to compress the `build/html/` folder into a `.tar` (much like a `.zip`).

### Job 2: Uploading the site onto GitHub Pages

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: build
  permissions:
    pages: write
    id-token: write

  steps:
    - name: Deploy uploaded artifact to GitHub Pages
      uses: actions/deploy-pages@v4
```

Under `deploy`, I again specify an Ubuntu Docker container. I also specify some permissions as these were required by the next step.[^deploy-pages]

[^deploy-pages]: https://github.com/actions/deploy-pages

Theres only one step in this section:

- **Deploy uploaded artifact to GitHub Pages**: a pre-made workflow specifically designed to upload the previously created `.tar` onto GitHub pages.

## 30/08/2024

### Modifying the GitHub workflow

In the dev container log, I spoke about syncing a `requirements.txt` file between the dev container and github workflow.

In the build section of my workflow, I edited it to the following:

```yaml
build:
  runs-on: ubuntu-latest

  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Install Python packages
      run: pip install -r ./.devcontainer/requirements.txt

    - name: Make static files
      run: make html

    - name: Package and upload artifact of static files
      uses: actions/upload-pages-artifact@v3
      with:
        path: ./build/html
```

I removed using the sphinx Docker image as it was inconsistent with my Devcontainer, and then added the similar command as above into the Install Python packages section.

Now whenever I or others need to edit our packages, we can simply edit them in one place with no further work needed.
