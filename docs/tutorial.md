# Tutorial

## Quick Start

Follow the instructions to [deploy AbFab locally](./deploy.md#deploy-locally).

Go to http://localhost/my-abfab/abfab/index.html and click on the AbFab logo.

Login as root / root.

You are now in the AbFab online interface.

## Developing through the online interface

Select the root folder (named `~`) in the navigation pane, then click on the `+` button.

Select the `Folder` type, enter the name `fun`, and click on the `Add` button.

Now select the `fun` folder in the navigation pane, then click on the `+` button again.

This time, select the `File` type, enter the name `hello.svelte`, and click on the `Add` button.

Let's enter the following code in the editor:

```html
<script>
    let me = 'Patsy';
</script>
<h1>Hello {me}</h1>
```

## Developing locally with an IDE
