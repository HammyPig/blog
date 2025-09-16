---
icon: "{fab}`react`"
date: "2025-09-16"
desc: "Covers the fundamental concepts of React."
tags: ["notes"]
---

# React Notes

## Components

React apps are made from modular chunks of HTML called **components**:

```jsx
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}
```

Components can then be used elsewhere:

```jsx
export default function MyApp() {
  return (
    <>
      <h1>Welcome to my app</h1>
      <MyButton />
    </>
  );
}
```

Components:

- follow PascalCase
- return only one tag (so if there is no natural parent tag, you wrap it with `<> </>`)

You also have to close all tags. E.g. instead of writing `<img>` and `<br>`, you write `<img />` and `<br />`.

The `export default` tag specifies the main component.

## Styling

When styling tags, you must use `className` instead of `class`. CSS rules are then written in a separate CSS file as normal:

```jsx
<img className="avatar" />
```

## Variables

You can use JavaScript variables. Note the interesting usage in the style section:

```jsx
const user = {
  name: 'Hedy Lamarr',
  imageUrl: 'https://i.imgur.com/yXOvdOSs.jpg',
  imageSize: 90,
};

export default function Profile() {
  return (
    <>
      <h1>{user.name}</h1>
      <img
        className="avatar"
        src={user.imageUrl}
        alt={'Photo of ' + user.name}
        style={{
          width: user.imageSize,
          height: user.imageSize
        }}
      />
    </>
  );
}
```

:::{note}
If you want variables to update after being rendered, this will be covered below.
:::

## Conditionals

Display different components based on a condition:

```jsx
let content;

if (isLoggedIn) {
    content = <AdminPanel />;
} else {
    content = <LoginForm />;
}

return (
  <div>
    {content}
  </div>
);
```

Which can be written more compactly as:

```jsx
<div>
  {isLoggedIn ? (
    <AdminPanel />
  ) : (
    <LoginForm />
  )}
</div>
```

Or even more so as:

```jsx
<div>
  {isLoggedIn && <AdminPanel />}
</div>
```

## Loops

Use for loops to display a list of content. It is important to assign a `key` attribute, which is typically the database ID of each item:

```jsx
const products = [
  { title: 'Cabbage', id: 1 },
  { title: 'Garlic', id: 2 },
  { title: 'Apple', id: 3 },
];

const listItems = products.map(product =>
  <li key={product.id}>
    {product.title}
  </li>
);

return (
  <ul>{listItems}</ul>
);
```

## Triggering Functions

You can write functions inside your components, which can then be triggered by some user action:

```jsx
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }

  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```

## Non-Static Variables

Variables will render static unless you use state. Each component instance has its own state:

```jsx
import { useState } from 'react';

function MyButton() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <button onClick={handleClick}>
      Clicked {count} times
    </button>
  );
}
```

If you want to share data between two components, have the parent component hold the variable, and then pass it down to the children. Variables passed down like this are called **props**:

```jsx
export default function MyApp() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <div>
      <h1>Counters that update together</h1>
      <MyButton count={count} onClick={handleClick} />
      <MyButton count={count} onClick={handleClick} />
    </div>
  );
}

function MyButton({ count, onClick }) {
  return (
    <button onClick={onClick}>
      Clicked {count} times
    </button>
  );
}
```
