# Tutorial

## Quick Start

Follow the instructions to [deploy AbFab locally](./deploy.md#deploy-locally).

Go to http://localhost/my-abfab/abfab/index.html and click on the AbFab logo.

Login as root / root.

You are now in the AbFab online interface.

The online interface allows to develop components and create data in the AbFab server entirely from a browser.

That is not the only way to use AbFab (you can also use an IDE and deploy your code to the server), but that is the best way to start and discover AbFab.

## A first component

Select the root folder (named `~`) in the navigation pane, then click on the `+` button.

Select the `Folder` type, enter the name `tutorial`, and click on the `Add` button.

Now select the `tutorial` folder in the navigation pane, then click on the `+` button again.

This time, select the `File` type, enter the name `hello.svelte`, and click on the `Add` button.

Let's enter the following code in the editor:

```html
<script>
    let me = 'Patsy';
</script>
<h1>Hello {me}</h1>
```

You can save it by pressing Ctrl/Cmd+S, or by clicking the checkmarck on the top right corner.

When saving it, the AbFab online interface saves in the AbFab server the source code you have entered, but it also compiles it and saves the compiled version alongside.

You can now preview the component in the online interface by clicking on the `Play` icon on the top right corner.

Or you can click on the `Info` icon, where you get a link to open the component in a new tab: http://localhost/my-abfab/tutorial/hello.svelte

Let's dig a bit into the code.

AbFab uses [Svelte](https://svelte.dev/) to implement its components. Svelte offers a very simple syntax, as you can see in this example, a Svelte component is done like a regular HTML page: the content is structured using HTML tags and the JavaScript is done into a `<script>` tag (and similarly, CSS is done in a `<style>` tag).

With `let me = 'Patsy';`, you have declared a variable.

And, thanks to Svelte, you can inject this variable anywhere in your HTML markup by enclosing it between curly brackets. That's what you did with `<h1>Hello {me}</h1>`.

You can also call some functions from the markup. Let's change the code like this:

```html
<script>
    let name = 'Patsy';

    function changeName() {
        name = 'Eddy';
    }
</script>
<h1>Hello {name}</h1>
<button on:click="{changeName}">Change</button>
```

With `on:click={changeName}`, you are calling the `changeName` function when someone clicks on the button.

And you can also notice the variable changes are immediately reflected in the markup: as the function is changing the `name` value to 'Eddy', the page now shows "Hello Eddy". The change has been detected by Svelte and the markup has been updated automatically.

Note: even though many important Svelte features are explained here, this is _not_ a Svelte tutorial. You are encouraged to have a look to the excellent [Svelte tutorial](https://svelte.dev/tutorial/basics) if you want to learn more about it.

## Rendering content

It is absolutely fine to use a component in standalone mode like the previous example.
But in some cases, the same component must be used to render different contents.

Let's say you want to display contact information in a contact card.

Select the `tutorial` folder in the leftClick the `+` button in the navigation pane and click the `+` button.

This time, you will select the `Content` type, enter the name `eddy` and click `Add`.

Enter the following data in the editor:

```json
{
    "firstname": "Eddy",
    "lastname": "Monsoon",
    "email": "eddy@abfab.dev"
}
```

(Note: make sure to put double-quotes everywhere and no trailing comma, this is JSON, not JavaScript)

Then save (Ctrl/Cmd+S or check mark button on the top right corner).

And create another content named `patsy` containing:

```json
{
    "firstname": "Patsy",
    "lastname": "Stone",
    "email": "patsy@abfab.dev"
}
```

We have 2 different contacts, and we want to display them using the same component.

Let's create a component (`File` type) named `card.svelte`, with the following code:

```html
<script>
    export let content;
</script>
<dl>
    <dt>Firstname</dt>
    <dd>{content.firstname}</dd>
    <dt>Lastname</dt>
    <dd>{content.lastname}</dd>
    <dt>Email</dt>
    <dd>{content.email}</dd>
</dl>
```

Here, you can notice something special:

```js
export let content;
```

That is how Svelte declares properties for a component. It means this `card` component can receive a `content` value as input properties.

Actually, when a component is meant to display AbFab content, it must always have a `content` properties declared that way.

So now, when previewing the component, you see all the values are undefined, but if you put `/tutorial/eddy` and then click the refresh button in the top right corner, then you see the Eddy contact information displayed in the preview pane.

## Using a component as view for a content

Okay it is nice to see your contact as the preview, but unfortunately, if you go to http://localhost/my-abfab/tutorial/eddy, all you see is a sad JSON content.

It would be better to see this content rendered with your `card` component.

To do so, you have to tell AbFab you want `card` to be the default view for any content in the `tutorial` folder.

Click on the `tutorial` folder in the navigation pane. In the editor, you see just `{}`.

Folder properties can be defined here, so let's go with:

```json
{
    "views": {
        "view": "./card.svelte"
    }
}
```

And save.

`view` is the default view name, it indicates which component AbFab should use to render any content in the folder when no special view is explicitly requested.

So now, if you visit http://localhost/my-abfab/tutorial/eddy again, you will see your contact card.

Let's change the folder properties to:

```json
{
    "views": {
        "card": "./card.svelte"
    }
}
```

There is no default view anymore, to display the card, you need to pass the view name as parameter in the URL:
http://localhost/my-abfab/tutorial/eddy?view=card

Note: defining view is handier as it makes URL shorter, but it is not mandatory, you can pass directly the component's full path: http://localhost/my-abfab/tutorial/eddy?viewpath=/tutorial/card.svelte

Before continuing, let's go back to the initial setup:

```json
{
    "views": {
        "view": "./card.svelte"
    }
}
```

## Using a component in another component

The main point in making components is to be able to breakdown a complex application into small elements focusing on simple tasks, that can be assembled to achieve more complex features until it covers all the expected features of the application.

It implies a component can be re-used in another one.

Let's create a `menu.svelte` component with the following code:

```html
<div>Menu placeholder</div>
```

It is meant to be your menu to go from one contact to another, but for now, it is just a placeholder, you will add the actual links in the next step.

Let's come back in the `card` component, and change it as follow:

```html
<script>
    import CardMenu from './menu.svelte';
    export let content;
</script>
<dl>
    <dt>Firstname</dt>
    <dd>{content.firstname}</dd>
    <dt>Lastname</dt>
    <dd>{content.lastname}</dd>
    <dt>Email</dt>
    <dd>{content.email}</dd>
</dl>
<CardMenu></CardMenu>
```

You will notice first you are importing the `menu.svelte` component as `CardMenu`. Actually, the name here can be anything you want, it just lets Svelte knows you want to reference this component as `CardMenu`, so when you can insert it in your markup as `<CardMenu></CardMenu>`, it is properly processed.

The only constraint is to choose a name starting with an uppercase letter (so `Menu` is correct, `cardMenu` is not).

## Links and navigation

Now, let's fix the links in the `menu` component:

```html
<a href="./eddy">Eddy</a> <a href="./patsy">Patsy</a>
```

The links are done exactly as they would be done in classical HTML.

Nevertheless, they will not behave exactly the same. If you go to http://localhost/my-abfab/tutorial/eddy, the full page is loaded in your browser, but now when using the menu and clicking on the "Patsy" link, the displayed URL is updated but the page does not reload, it is dynamically updated. AbFab will only load the data for the `patsy` content, and re-render it using the existing component. That is client-side navigation, making the application faster

In this example, you have used a relative link, `./patsy`, but it is definitely possible to use an absolute one. In that case the link would be `/~/tutorial/patsy`. Why not `/my-abfab/tutorial/patsy`? Because your code is probably meant to be deployed to a production server where the app root path might be different, like `https://my-server.net/tutorial/patsy`. To avoid mentionning the real app root path in components code, AbFab uses `/~/` as an alias that is dynamically replaced by the proper value.

Note: That is also how AbFab inject its cache keys, you have maybe noticed the url something like http://localhost/my-abfab/1634570913/tutorial/patsy, `1634570913` here is a cache key which changes when a component is updated, making sure previously cached versions of components in the user browser are not reused.

## Reactivity

Reactivity is about making sure the rendering is always consistent with the data changes. Whenever a data changes, we expect the UI reflects this change accordingly.

Reactivity may seem difficult to understand, so let's use a simple example: consider an Excel spreadsheet, if cell A3 is `=A1+A2`, you know that whenever you will change the values in A1 or A2, A3 will be automatically updated so it displays the sum of the 2 other cells. That's reactivity, you have implemented the A3 value once, and then the application makes sure it is always true.

Thanks to Svelte, using reactivity in AbFab will just as simple as in Excel.

Let's try it with a new component named `favorite.svelte`:

```html
<script>
    let favorite = false;

    function toggleFavorite() {
        favorite = !favorite;
    }
</script>
<div>
    Is favorite: {favorite}
    <button on:click="{toggleFavorite}">Favorite</button>
</div>
```

Add this component in `card.svelte` the same way you have added the menu:

```html
<script>
    …
    import Favorite from './favorite.svelte';
    …
</script>
…
<Favorite></Favorite>
…
```

Now you have a "Favorite" button, and when you click on it, you see the `favorite` variable is toggling from `true` to `false`.

That's already reactive, because you see the mention `Is favorite? true` changing accordingly. So whenever a variable is re-assigned, Svelte updates the markup automatically.

But this component is not good enough, you would prefer the button label to be "Favorite" or "Unfavorite" depending on the case.

So let's change a bit the code:

```html
<script>
    let favorite = false;

    let label = favorite ? 'Unfavorite' : 'Favorite';

    function toggleFavorite() {
        favorite = !favorite;
    }
</script>
<div>
    Is favorite: {favorite}
    <button on:click="{toggleFavorite}">{label}</button>
</div>
```

You have now a `label` variable which value depends on the `favorite` value.

But it is assigned only once, when the component is rendered the first time, so when you click on the button, the button label is not updated.

Of course, one option could be to update the label value in the `toggleFavorite()` function as you did with the `favorite` variable:

```js
function toggleFavorite() {
    favorite = !favorite;
    label = favorite ? 'Unfavorite' : 'Favorite';
}
```

But that is exactly what you want to avoid. Imagine a more complex component, if you have to explicitly re-assign all the variables impacted by a given change, that is painful and error prone. Reactivity is about focusing on the essential change (in this case, toggling the `favorite` value), and anything depending on it will be handled automatically.

Here is how you do it:

```html
<script>
    let favorite = false;

    $: label = favorite ? 'Unfavorite' : 'Favorite';

    function toggleFavorite() {
        favorite = !favorite;
    }
</script>
<div>
    Is favorite: {favorite}
    <button on:click="{toggleFavorite}">{label}</button>
</div>
```

The only difference with the first attempt is you used this `$:` prefix instead of `let`.

`$:` is in Svelte what `=` is in an Excel cell: whatever is entered after this prefix will be always true, always re-executed on any change.

Note: `$:` can prefix a single line but it can also prefix an entire block:

```js
$: {
    label = favorite ? 'Unfavorite' : 'Favorite';
    console.log('Hey, favorite has changed!');
}
```

It can also prefix a function call:

```js
$: updateAllTheThings();
```

## Sharing code and resources

The `File` type is not just for components. If the name ends with `.svelte`, it will be considered as a component by AbFab and it will be compiled.
But you can create any kind of text files like `.js`, `.css`, `.svg`, etc.

Note: binaries cannot be upload from the AbFab online interface at the moment but you can use the syncing utility (see below in [Developing locally with an IDE](#developing-locally-with-an-ide)).

Let's go to https://commons.wikimedia.org/wiki/Category:Firefox_OS_Emoji#/media/File:Fxemoji_u1F394.svg, download the original file and rename it as `icon.svg` (just to make it easier).

Click on the `tutorial` folder in the navigation pane, and just drag&drop the SVG file in the bottom part.

Now your `icon.svg` has been uploaded, you can use it in your `card` component:

```html
<script>
    …
</script>
<img src="./icon.svg" />
<dl>…</dl>
```

And save. Ok, you have two problems here:

-   the compiler sends you an a11y warning, because there is no alt attribute on the image
-   the icon is too big

Let's fix it that way:

```html
<script>
    …
</script>
<img src="./icon.svg" alt="Card icon" />
<dl>…</dl>
<style>
    img {
        width: 50px;
    }
</style>
```

You have added a `<style>` tag to set the image width. You might think it is a bit brutal to use `img` as a CSS selector here, could it impact other `<img>` tags in the rest of the application?

That is actually totally safe, because component styles are encapsulated, they applies only to the current component.

## Using the Pastanaga UI library

AbFab comes with a (minimal) UI library, based on the Pastanaga design system.

It is used to build the AbFab online interface and, if you wish, you can use it to build your own app.

First, you have to add the Pastanaga style in `card.svelte`:

```html
<svelte:head>
    <link rel="stylesheet" href="/~/abfab/pastanaga/pastanaga.css">
</svelte:head>
```

The `<svelte:head>` allows to add code in your DOM head section.

The style will be loaded globally, doing it only once in your highest level component (in your case that's `card.svelte`) is fine, no need to do it again in any sub-components.

Now you can use the UI components, for example, let's modify `favorite.svelte` as follow:

```html
<script>
    import AFButton from '/~/abfab/ui/button.svelte';
    …
</script>
<div>
    Is favorite: {favorite}
    <AFButton size="small" kind="primary" label="{label}" on:click="{toggleFavorite}"></AFButton>
</div>
```

Now you have a Pastanaga button instead of the default button.

Note: you are free to use any other UI library in AbFab (see below [Using external libraries](#using-external-libraries)).

## Implementing a full app

Up to now, you have created contents manually using the AbFab online interface, and your components were allows working on their own.

AbFab can be used to build entire applications providing different views and allowing to manage data.

Let's create a typical CRUD (Create-Read-Update-Delete) application: a contact manager.

First, create a folder named `crud`.

Add a sub-folder named `contacts`, that is where contacts will be stored.

In the `crud` folder, let's create a `edit.svelte` component providing a form to edit or create a contact:

```html
<script>
    import { Content, navigateTo } from '/~/abfab/core.js';

    export let content;
    let { name, email } = content;

    async function save() {
        if (!email) return;
        if (!content.email) {
            await Content.create('/~/crud/contacts', email, { name, email });
        } else {
            await Content.update('', { name, email });
        }
        navigateTo(`/~/crud/list.svelte`);
    }
</script>
<main>
    <div>
        <label>
            <input bind:value="{name}" label="Name" placeholder="Enter the contact name" />
            Name</label
        >
    </div>
    <div>
        <label>
            <input bind:value="{email}" label="Email" placeholder="someone@mail.org" />
            Email</label
        >
    </div>

    <button on:click="{save}">Save</button>
</main>
```

Let's go step by step:

-   you use `core.js` which is the AbFab core library, in this case, it provides `Content`, the Content API to manipulate contents, and `navigateTo` which allows to go to a given path.
-   you extract `name` and `email` from the current content (which will exist or not depending on you are editing an existing contact or just creating a new one)
-   you implement the `save()` function, and that is where you use the `Content` API: if the current content already had an email, you do `Content.update` and if not, you do `Content.create` (the new content is created in the `/~/crud/contacts` folder and you use the email as an id for it)
-   after saving, you redirect to the `list` component (see below)
-   and then you have the actual HTML form, where you use `bind:value` to bind the input value to the corresponding variable.

You can notice the `save` function is marked as `async`. That is because you are using the `Content` API which is making HTTP calls to the server. All the `Content` API calls are prefixed with `await`. It means the browser will wait until the call is done to continue with the rest of the code.

Go to the folder properties and define `./edit.svelte` as default view (not: it can be done on `/~/crud/contacts` but it can also be done on `/~/crud` because view definitions are inherited).

Ok now you need to create the `list` component, which will display all the existing contacts:

```html
<script>
    import { onMount } from 'svelte';
    import { Content, navigateTo } from '/~/abfab/core.js';

    let contacts = [];
    onMount(async () => {
        contacts = await Content.folderContents('/~/crud/contacts');
    })

    async function deleteContact(path) {
        await Content.delete(path);
        contacts = contacts.filter(c => c.path !== path);
    }
</script>
<table>
    <tr>
        <th>Name</th><th>Email</th>
        <th><button on:click={() => navigateTo('/~/crud/edit.svelte')}>+</button></th>
    </tr>
    {#each contacts as contact}
    <tr>
        <td>{contact.data.name}</td>
        <td>{contact.data.email}</td>
        <td>
            <button on:click={() => navigateTo(contact.path)}>Edit</button>
            <button on:click={() => deleteContact(contact.path)}>Delete</button>
        </td>
    </tr>
    {/each}
</table>
```

Here you use the Svelte function `onMount`, it allows to run some code at the time the component is created. In thsi case, you make a call to the `Content` API to collect all the existing contacts stored in `/~/crud/contacts`.

And you implement the `deleteContact` function which uses `Content.delete` to remove the contact, and then remove the corresponding entry from the displayed list.

Actually, that's maybe not that smart, if any action meant to change the data is also responsible to update the UI, it will get messy pretty fast.

Let's create a `refresh` function that will be called everytime you need:

```js
onMount(async () => await refresh());

async function refresh() {
    contacts = await Content.folderContents('/~/crud/contacts');
}

async function deleteContact(path) {
    await Content.delete(path);
    await refresh();
}
```

Note: in the `edit` component, you have implement the Save button click with `on:click={save}`, but here the Delete button for example uses `on:click={() => deleteContact(contact.path)}`.
An event handler needs a function (not a function call), so passing `on:click={deleteContact(contact.path)}` would not work, that's why you have to create a function that will make the call to `deleteContact` (and the arrow syntax `() => {}` is very handy in that case).

## Using external libraries

External libraries can be used in any AbFab component. You need to import their ESM version.

Here is an example using Chart.js:

```html
<script>
    import { onMount } from 'svelte';
    import { Chart, registerables } from 'https://unpkg.com/chart.js@3.6.0/dist/chart.esm.js';
    Chart.register(...registerables);

    const labels = ['January', 'February', 'March', 'April', 'May', 'June'];
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Extra weight caused by lockdown',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: [0, 10, 5, 2, 20, 30, 45],
            },
        ],
    };
    const config = {
        type: 'line',
        data: data,
        options: {},
    };
    let myChart;
    onMount(() => new Chart(myChart, config));
</script>
<div>
    <canvas bind:this="{myChart}"></canvas>
</div>
<style>
    canvas {
        max-height: 100vh;
        max-width: 100vw;
    }
</style>
```

Note: as you can see, Chart.js has been directly imported from a remote location (https://unpkg.com), but in some cases (intranets with internet access restriction for example), you might prefer to serve them directly from AbFab. AbFab contains a `lib` folder dedicated to librairies, by default it only contains the Svelte library, but you are free to create a new folder named `chart.js` and upload the `chart.esm.js` file in this folder. Then you can import it as follow:

```js
import { Chart, registerables } from '/~/chart.js/chart.esm.js';
```

## Publishing components

## The Data API

## Developing locally with an IDE

TBD

```sh
docker run --rm -v /<absolute_path>/tutorial:/app/tutorial ebrehault/abfab-utils python utils/sync.py down tutorial --auth root:<password> --host https://demo.abfab.dev/somepath --root . --contents
```

```sh
docker run --rm -v /<absolute_path>/tutorial:/app/tutorial ebrehault/abfab-utils python utils/sync.py up tutorial --auth root:<password> --host https://demo.abfab.dev/somepath/ --root . --contents
```
