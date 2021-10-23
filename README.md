# AbFab

A web application publication environment

## Principles

-   Client-side technics do improve the user experience, nevertheless they should not damage the developer experience.
-   Generic client-side features should not be bundled in any new web app, they should be provided by a generic and reusable runtime.
-   Bundling is not scalable, adding a new page to an existing app should not involve to re-deploy the entire thing.

## Description

AbFab is a web application publication environment. It provides the essential services any web application need in a generic, simple, and light JavaScript runtime.

We could consider AbFab is actually extending the web browsers native capabilities, so they are not restricted anymore to static HTML pages publication. With AbFab, they can run client-side dynamic applications.

When using AbFab, you can focus on the app "content" and forget about routing, navigation, authentication, state management, backend connectivity, etc., because all of that is provided by AbFab.

The "content" we are talking about here can be very various things:

-   It can be static HTML if that's good enough for us.
-   It can be JSON data. In that case, you will use a component to render the JSON content properly.
-   It can be advanced components (the default approach is to create Svelte components, but other frameworks could be considered)

## Do you need to learn a new technology?

To develop an AbFab app, you will just need HTML, CSS and (simple) JavaScript.

Svelte could be considered as a templating layer, it is very simple to learn and to use and will not be a blocker.

Regarding backend, deployment and setup is entirely performed using Docker. No Docker knowledge is needed.

## Quickstart

-   [Deploy a local instance](./docs/deploy.md#deploy-locally)
-   [Tutorial](./docs/tutorial.md)

## Simple things must be simple

**No bundle and no static files**: You will not have to use NPM, you will not need to bundle your code. All the components and data are on the server, there is no need to generate and deploy static files.

**Code-splitting**: Each component is compiled automatically and independently, and each page of your app will load only the needed components.

**Client-side navigation**: Navigation from one page to another is performed by loading only the missing data and the application renders it on the client-side, so the application is always fast.

## Complex things must be possible
