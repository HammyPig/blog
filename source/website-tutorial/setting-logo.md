# Setting the Logo, Socials, and Footer

Finally, let's first learn how to personalise our site's logo, social icons, and footer text.

## Setting the Logo

To set the logo, open `conf.py` and find the following lines:

```python
"logo": {
    "text": "Title",
    "image_light": "_images/example.png"
},
```

Here you can replace both the logo text and image.

For example, if I had an image file named `logo.png`, I would navigate to the `_images/` folder, place the file, and then edit the line to the following:

```python
"logo": {
    "text": "Title",
    "image_light": "_images/logo.png"
},
```

## Setting Socials

In the same `conf.py` file, find the following lines:

```python
"icon_links": [
    {
        "name": "GitHub",
        "url": "https://github.com/HammyPig/website-template",
        "icon": "fa-brands fa-github",
        "type": "fontawesome"
    },
],
```

This is an example of a social icon, where each icon has the following fields:

- **name**: The text that appears when a user hovers over the button.
- **url**: Destination URL.
- **icon**: Any free [Font Awesome 6](https://fontawesome.com/search?q=github&o=r&m=free) icon class name.

For example, if I wanted to add a Facebook page, I would look on [Font Awesome 6](https://fontawesome.com/search?q=github&o=r&m=free) to find the Facebook icon. Clicking on the icon gives me this code snippet:

```
<i class="fa-brands fa-facebook"></i>
```

All I'm interested in is the `fa-brands fa-facebook` part, which I will then add to my `conf.py` file like so:

```python
"icon_links": [
    {
        "name": "GitHub",
        "url": "https://github.com/HammyPig/website-template",
        "icon": "fa-brands fa-github"
    },
    {
        "name": "Facebook",
        "url": "https://facebook.com/example",
        "icon": "fa-brands fa-facebook"
    },
],
```

I simply copied and pasted the first icon example, and used that as a template for my next icon.

You can add as many social icons as needed.

## Setting the footer

In the same `conf.py` file, find the following lines:

```python
html_context = {
   "default_mode": "light",
   "footer_text": "Made with love by James."
}
```

You can edit the `footer_text` value to edit the footer text.
