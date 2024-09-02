# Adding Content to Pages

Now that we know how to create and view our pages, let's now explore how to add content to them. This page will show you how to create everything you may want to display on your pages.

## Subheadings

Subheadings are used to divide and group relevant content on a single page. They show up on the right sidebar and can be clicked on to navigate through a page.

```md
## Subheading 1

Text underneath a subheading.

## Subheading 2

Some additional text.
```

## Bold and italics

You can apply different text styles like bold and italics like so:

```md
This is **bold text**. This is *italic text*.
```

:::{dropdown} Result
This is **bold text**. This is *italic text*.
:::

## Images

You can add an image by referencing its relative file path:

```md
![text description of image](images/example.png)
```

:::{dropdown} Result
![text description of image](images/example.png)
:::

You may notice that the text description isn't shown in the result. This is because it's usually used by screen reader technology to describe the image to a reader.

## Links

This is how you add a link to some text.

```md
This is [a link](https://example.com) in a sentence.
```

:::{dropdown} Result
This is [a link](https://example.com) in a sentence.
:::

## Buttons

If you don't want to use a link, you can instead use a button.

```
:::{button} https://example.com
Button text
:::
```

::::{dropdown} Result
:::{button} https://example.com
Button text
:::
::::

## Referencing

You can add sources to your content by using footnote references.

```md
This is an example text with a reference[^reference-title] in it.

[^reference-title]: Reference description (usually a link).
```

:::{dropdown} Result
This is an example text with a reference[^reference-title] in it.

[^reference-title]: Reference description (usually a link).
:::

The reference description will be displayed in an auto-generated footnote at the bottom of your page.

## Lists

You can create a list of items:

```md
- Item 1
- Item 2
- Item 3
```

:::{dropdown} Result
- Item 1
- Item 2
- Item 3
:::

As well as a numbered variant:

```md
1. Item 1
1. Item 2
1. Item 3
```

:::{dropdown} Result
1. Item 1
1. Item 2
1. Item 3
:::

Notice that you don't need to specify specific numbers in the numbered variant, as the correct numbering will be auto-generated on your page.

## Dropdowns

Dropdowns are useful for hiding optional content.

```md
:::{dropdown} Dropdown title
This is a paragraph inside the dropdown.
:::
```

::::{dropdown} Result
:::{dropdown} Dropdown title
This is a paragraph inside the dropdown.
:::
::::

## Cards

Cards are useful for showing bite-sized information. You can add as many cards as you want. In this example, I added 3.

```md
::::{card-grid}

:::{grid-item-card} Card title
This is a paragraph inside a card.
:::

:::{grid-item-card} Card title 2
This is another paragraph.
:::

:::{grid-item-card} Card title 3
This is another paragraph.
:::

::::
```

:::::{dropdown} Result
::::{card-grid}

:::{grid-item-card} Card title
This is a paragraph inside a card.
:::

:::{grid-item-card} Card title 2
This is another paragraph.
:::

:::{grid-item-card} Card title 3
This is another paragraph.
:::

::::
:::::

## Notes

Add notes to highlight certain information that doesn't exactly fit into your paragraph.

```md
:::{note}
This is noteworthy!
:::
```

::::{dropdown} Result
:::{note}
This is noteworthy!
:::
::::
