# AbFab

[![Build Status](https://github.com/ebrehault/abfab/workflows/CI/badge.svg)](https://github.com/ebrehault/abfab/actions?query=workflow%3ACI)

A web application publication environment

# Why? What for?

The main objective behind AbFab is to provide a way to make frontend easy, fun, and pleasant.

It is not meant to be a gigantic framework covering thousands of use cases. It targets small features that could probably be implemented in more classical ways, but you just do not want to deploy too many things (like a database, a bunch of backend endpoints, a security layer, a frontend app, etc.), or maybe you do not want to pollute your existing stack with extra dependencies just to achieve a small widget in one given page of your entire app.

AbFab is an all-in-one platform allowing to develop simple frontend components that can be published anywhere.

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

## License

AbFab is released under the BSD-2 license.
