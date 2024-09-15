# Dev Containers Tutorial

The great thing about dev containers is that:

- You will never again run into compatibility issues, regardless of whether you are on Windows, Mac, or Linux.
- Your computer won't be bloated by software, as containers are completely independent from your computer.

## Prerequisites

Before starting, you will need to complete the following tasks:

- **VS Code**: Download and install from the [VS Code website](https://code.visualstudio.com).
- **Docker**: Download and install from the [Docker website](https://www.docker.com).
- **VS Code Dev Containers Extension**: Install from the [VS Code marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

Additionally, this tutorial will assume that you are familiar with the following topics:

:::::{grid} 1 2 3 3
:gutter: 4

::::{grid-item-card} {fas}`code` VS Code
A code editor with loads of functionality that makes programming as convenient and seamless as possible.
::::

:::::

## Creating a dev container in a project folder

Given a project folder, first create a folder named `.devcontainer/`. Inside the folder, create the files `devcontainer.json` and `Dockerfile`. Your project directory should now look like this:

```
.devcontainer/
├── devcontainer.json
└── Dockerfile
```

Inside `devcontainer.json`, enter the following:

```json
{
    "build": {
        "dockerfile": "Dockerfile"
    }
}
```

## Installing software and packages

Let's say in our project we'd like to use Python, along with the `numpy` and `matplotlib` packages.

First we need to find a 'base image' as a starting point. Base images are found on the [Docker Hub website](https://hub.docker.com/).

By searching 'python' on Docker Hub, we can find the [python](https://hub.docker.com/_/python) image, which is essentially a clean PC installation with only Python installed.

On the same page, it will show a 'Docker Pull Command', which in this case is `docker pull python`. We are only interested in the last part, which we will place into our `Dockerfile` like so:

```Dockerfile
FROM python
RUN pip install numpy
RUN pip install matplotlib
```

- The `FROM` keyword sets the base image, where `python` is from the previous Docker pull command.
- The `RUN` keyword allows us to run arbitrary terminal commands. You can add as many `RUN` commands as you'd like.

## Installing VS Code extensions

In my example, I want to install the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions. Gather the extension IDs and put them into a list:

```py
["ms-python.python", "ms-toolsai.jupyter"]
```

Then inside the `devcontainer.json` file, place the list like so:

```json
{
    "build": {
        "dockerfile": "Dockerfile"
    },
    "customizations": {
        "vscode": {
            "extensions": ["ms-python.python", "ms-toolsai.jupyter"]
        }
    }
}
```

## Opening a project in a dev container

Inside your project folder, open the command palette and select `Dev Containers: Reopen in Container`.

## Updating a dev container

Whenever you make changes to your dev container, make sure to open the command palette and run `Dev Containers: Rebuild Container` to reflect those changes.
