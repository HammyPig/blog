---
icon: "{fab}`html5`"
date: "2025-09-12"
desc: "Building a modern and responsive webpage layout with a modular approach."
tags: ["notes"]
---

# HTML/CSS Notes

## Boilerplate

A webpage is made from the following boilerplate code.[^mozilla-boilerplate] All of the website's content is then placed in the `body` tag.

[^mozilla-boilerplate]: https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website/Creating_the_content#creating_your_first_html_document

```html
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Title Shown in Browser Tab</title>
  </head>
  <body>
    <p>Hello, World!</p>
  </body>
</html>
```

## Page Layout

You will notice that almost every website is made up of three primary sections, which typically show:

1. header: site-wide logo and navigation bar
1. main: page-unique content
1. footer: site-wide additional information and links

These three sections are reflected in the `body` tag:

```html
<body>
  <header></header>
  <main></main>
  <footer></footer>
</body>
```

## Sections

The main section will also be typically made up of smaller sub-sections of content:

```html
<main>
  <section></section>
  <section></section>
  <section></section>
</main>
```

## Containers

Each section contains an additional `div` with a fixed width applied. This is the maximum width content will fill, and is arbitrarily determined by the website designer, e.g. a smaller paper-sized page width makes paragraphs more comfortable to read:

```css
.container {
    width: 1100px;
}
```

```html
<section style="background-color: whitesmoke;"> /* colour stretches to full width of the page */
  <div class="container"></div> /* limits content to a fixed maximum width */
</section>
```

:::{note}
The reason why this is applied to the internal `div` rather than the parent section is so the section can still have full-width styling, e.g. a background colour which stretches the whole width of the screen.
:::

## Flexbox

Another feature you want is for the website to act responsively when resized, rather than maintain a fixed width that can be cut-off. To do this, you want to set `display` to flex to both the section and container.

For the section, we also horizontally align the containers to the centre of the screen by setting `justify-content` in the parent section. For the container, we set `flex-direction` to column such that when we place items into the container, they stack vertically, rather than being placed together horizontally. We also specify a `gap` which automatically provides a uniform space between all items in the container:

```css
.section {
    display: flex; /* enables flexbox */
    justify-content: center; /* horizontally aligns containers */
}

.container {
    width: 1100px; /* arbitrary maximum width of content */
    display: flex;
    flex-direction: column; /* items are placed vertically by default */
    gap: 10px; /* leave a gap between items */
}
```

## Blocks

Sometimes you will want more structured content. Rather than simply having each item one after the other, you may want to split the content into columns, e.g. a heading and text on the left, and an image on the right. To do this, we set the parent container's `flex-direction` to row. Instead of the parent container placing items vertically, it now places items horizontally.

However, we don't want the heading, text, and image to be on the same line. We want to first group the heading and text together, and then have the image next to the group. To solve this, we can split the container into two smaller sub-containers by creating a block.

A block has the same properties as a container, with the only difference being its `width` is set to 100%. By filling the parent container with these blocks (which all have the same width value), the container evenly splits itself horizontally.

Now we have the ability to place an arbitrary amount of sub-containers that can stack items in however way we want. This gives us both a modular and sort of recursive framework that can create many different layouts.

```css
.block {
    width: 100%; /* such that filling a container with only blocks will split it evenly */
    display: flex;
    flex-direction: column;
    gap: 10px;
}
```

```html
<section style="background-color: whitesmoke;">
  <div class="container" style="flex-direction: column;">
    <div class="block">
      <h1>Heading</h1>
      <p>Paragraph</p>
    </div>
    <div class="block">
      <img src="image.jpg">
    </div>
  </div>
</section>
```

## Spacing

Before we set uniform spacing using `gap`, but if we need to edit the individual spacing of an item, there are two ways to do so:

- `margin`: creates a specified spacing around an item
- `padding`: the item grows its background to the specified spacing

:::{note}
Both `margin` and `padding` are very similar, but with a subtle key difference. If for example a container has a background colour, using `padding` will fill the additional space created with the same background colour, where `margin` would not. Try out both to see which gives you the desired result.
:::

## Alignment

We may also want to align items either horizontally or vertically inside a block. Because we previously set our block to a flexbox, we can easily do so by using `align-items` and `justify-content`.

It is not very intuitive, but `justify-content` sets the primary axis alignment, while `align-items` aligns the secondary axis. The primary axis is whatever `flex-direction` is set to (either row or column). But in any case, you can simply try each keyword to see which gives you the desired result:

```html
<div class="container" style="flex-direction: column;">
  <div class="block" style="align-items: center; justify-content: center;">
    <h1>Heading</h1>
    <p>Paragraph</p>
  </div>
  <div class="block" style="align-items: center">
    <img src="image.jpg">
  </div>
</div>
```

## Responsiveness

Some designs may suit different devices. For example, containers with multiple columns can become unreadable on mobile devices as the items get squished. To get around this, we can override properties when a screen width is detected below a certain threshold.

In the below example, we override the `flex-wrap` property in our container, such that on mobile screens, columns stack vertically rather than horizontally.

```css
@media (max-width: 767px) {
    .container {
        flex-wrap: wrap;
    }
}
```

:::{note}
You can view common screen sizes on the [Tailwind Responsive Design](https://tailwindcss.com/docs/responsive-design) page.
:::
