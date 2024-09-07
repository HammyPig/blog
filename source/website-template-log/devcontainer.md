# Dev Container Log

## 12/08/2024

### Encountering discouraging environment issues

Almost immediately after I started this project, I ran into issues with my environment. Running `sphinx-quickstart` simply didn't work even after I followed the tutorial exactly. Since Sphinx is not commonly used, I didn't encounter anyone online talking about this issue either. I ended up needing to run `python -m sphinx sphinx-quickstart`, and I only knew the solution as I had previously run into a similar issue running `pip`, which required running `python -m pip`.

And yes, although you can say that I simply needed to configure my environment better, enough was enough. From this very moment, I intended to destroy the problem of environment setup once and for all.

### Discovering Docker and Dev Containers

I had previously heard about Docker and its promise of removing this issue. After researching how it worked, I noticed most information online only seemed to emphasise the use of Docker to package both software and environment into a single file. However, I instead simply wanted a way to containerise project environments away from each other, and from my personal computer.

I can't remember too much, but I recall having some issue where my Docker container did not have my project files and I needed to go through some process to do that. And then I had some issue with using VS Code extensions. I think I will come back to edit this part once I've gone through it again. But long story short I eventually discovered the Dev Containers extension, which made all these problems go away.

Dev containers uses the contents of the special folder named `/.devcontainer` to magically setup our environment along with VS Code extensions for our project.[^devcontainers] This folder usually contains two files:

- `devcontainer.json`: specifies VS Code extensions we want installed.
- `Dockerfile`: specifies our environment.

[^devcontainers]: <https://code.visualstudio.com/docs/devcontainers/tutorial#_how-it-works>

### Creating the Custom Sphinx Dockerfile

I created the `Dockerfile` inside the `/.devcontainer` directory so it can be used in our devcontainer. It will also later need to be mentioned in the `devcontainer.json` file.[^devcontainer-dockerfile]

[^devcontainer-dockerfile]: <https://code.visualstudio.com/docs/devcontainers/create-dev-container#_dockerfile>

Inside the `Dockerfile` file I put the following:

```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3
RUN pip install sphinx
RUN pip install myst-nb
RUN pip install pydata-sphinx-theme
RUN pip install sphinx-design
RUN pip install sphinx-copybutton
```

The first line describes the base image we want to use. Here I specified the pre-built image named [Python 3](https://github.com/devcontainers/images/tree/main/src/python) by Microsoft. You might wonder why I chose this specific image over other pre-built Python or even Sphinx images. I discovered this specific image when following the tutorial for creating a Devcontainer. The image is useful as it contains the latest version of Python 3, along with a suite of Python-related VS Code extensions. This simply saves me the trouble of knowing about and specifying those extensions.

The next lines then extend the image to include various specifically packages needed for the project:

- [sphinx](https://www.sphinx-doc.org/en/master/index.html): Converts a collection of easy-to-write markup files into a fully fledged website.
- [pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/): A modern and minimalist theme for our sphinx website.

The rest are Sphinx extensions, which you can find details on in the Sphinx site log.

### Configuring devcontainer.json

Next I created the file `devcontainer.json`, which is placed inside the same `.devcontainer` folder.[^devcontainer-devcontainer.json]

[^devcontainer-devcontainer.json]: <https://code.visualstudio.com/docs/devcontainers/create-dev-container#_create-a-devcontainerjson-file>

Inside the `devcontainer.json` file I put the following:

```json
{
    "build": {
        "dockerfile": "Dockerfile"
    },
    "postStartCommand": "git config --global --add safe.directory ${containerWorkspaceFolder}"
}
```

The first part simply tells the Dev Container extension to use our previously created custom Dockerfile as our image.[^devcontainer-dockerfile]

The second part enables us to use git commands in our Docker container, as I was coming across errors without it.[^devcontainer-git]

[^devcontainer-git]: <https://www.kenmuse.com/blog/avoiding-dubious-ownership-in-dev-containers/>

We can open the project using the devcontainer configuration by opening the command palette, and selecting `Dev Containers: Reopen in Container`. You will want to do this everytime you open the project.

## 30/08/2024

### Syncing packages between the dev container and github workflow

When adding additional packages, I noticed that I had forgot to add them to my GitHub workflow, which resulted in the workflows failing.

Because of this, I needed someway to sync any changes made to packages between both my Devcontainer and GitHub workflow.

The initial idea I always had was to use my Dockerfile as the image used by the workflow, however, when researching this possibility it seemed that you can only reference online hosted images, which is not very useful.

I had remembered seeing someone use a `requirements.txt` file in their `Dockerfile`, so then asked myself, what if I could use a common `requirements.txt` referenced both in my Devcontainer and workflow?

### Creating the requirements.txt file

The official Python website in their [installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/) page references a [pip documentation page](https://pip.pypa.io/en/latest/user_guide/#requirements-files) with a requirements file example.

Really its just a common `.txt` file with package names on each line. You can store this somewhere, and then reference while installing packages with the command:

```bash
pip install -r <path>
```

### Modifying the dev container

It felt natural to place the `requirements.txt` file in the `.devcontainer`, with my `Dockerfile` now being changed to:

```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3
COPY requirements.txt .
RUN pip install -r requirements.txt
```

`COPY` simply grabs the `requirements.txt` file from our directory into the Docker container such that it can be accessed. Then the next command simply installs all packages inside the file, as described previously.

### Modifying the github workflow

I then modified the github workflow. You can find more details in the github workflow log.

## 07/09/2024

### Editing devcontainer.json

Because I used jupyter notebooks for my own site, I needed to extend the dev container to accommodate for this functionality.

To add custom extensions, you simply add the following lines to `devcontainer.json` as below.[^custom-extensions]

[^custom-extensions]: https://code.visualstudio.com/docs/devcontainers/create-dev-container

```json
"customizations": {
    "vscode": {
        "extensions": ["extension-id1", "extension-id2"]
    }
}
```

The extension ID can be found by right clicking the extension on the VS Code UI, and selecting 'Copy Extension ID'.
