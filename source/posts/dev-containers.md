# Dev Containers

Given a project folder, simply create a folder named `.devcontainer`.

Inside, create the file `devcontainer.json`, and enter the following:

```json
{
    "image": "python"
}
```

Where the image value is the end of the Docker Hub URL (e.g. <https://hub.docker.com/_/python>).

And, if you want to extend the image (e.g. to include additional packages), you can do so by editing the file to:

```json
{
    "build": {
        "dockerfile": "Dockerfile"
    }
}
```

And then creating the file named `Dockerfile` inside the `.devcontainer` folder. Here, you put your base image, along with any additional commands you want to run like so:

```Dockerfile
FROM python
RUN pip install numpy
```
