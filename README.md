# AbFab

[![Build Status](https://github.com/ebrehault/abfab/workflows/CI/badge.svg)](https://github.com/ebrehault/abfab/actions?query=workflow%3ACI)

A web application publication environment

# Why? What for?

The main objective behind AbFab is to provide a way to make frontend easy, fun, and pleasant.

Client-side technics do improve the user experience, nevertheless they should not damage the developer experience. Bundling is not scalable, adding a new page to an existing app should not involve to re-deploy the entire thing.

AbFab is not meant to be a gigantic framework covering thousands of use cases. It targets small features that could probably be implemented in more classical ways, but you just do not want to deploy too many things (like a database, a bunch of backend endpoints, a security layer, a frontend app, etc.), or maybe you do not want to pollute your existing stack with extra dependencies just to achieve a small widget in one given page of your entire app.

AbFab is an all-in-one platform allowing to develop simple frontend components that can be published anywhere.

## Description

AbFab is a web application publication environment. It provides the essential services any web application needs:

-   a secured and fast backend storage,
-   a minimalistic yet powerful frontend component framework (Svelte),
-   a light JavaScript runtime offering routing and backend connectivity.

Components are written in Svelte, they are compiled in the browser (you do not need a local NPM), stored in the AbFab server, and can be published to any web page as a web component.

## Simple things must be simple

**No bundle and no static files**: You will not have to use NPM, you will not need to bundle your code. All the components and data are on the server, there is no need to generate and deploy static files.

**Code-splitting**: Each component is compiled automatically and independently, and each page of your app will load only the needed components.

**Client-side navigation**: Navigation from one page to another is performed by loading only the missing data and the application renders it on the client-side, so the application is always fast. It behaves as a Single-Page-App, but it's not.

**Component approach**: Components are an efficient way to structure an app (HTML is built that way actually). You should be able use them outside the SPA pattern.

## Do you need to learn a new technology? NO :)

**LOW CODE**: To develop an AbFab app, you will just need HTML, CSS and (simple) JavaScript. Svelte could be considered as a templating layer, it is very simple to learn and to use and will not be a blocker.

**LOW DEPLOYMENT**: AbFab is not just a frontend solution, it comes with a backend and all the elements needed to move everything to production, including a proper Nginx configuration. Deployment and setup is entirely performed using Docker. No Docker knowledge is needed.

**LOW BUILD**: Components can be developed directly from the AbFab online interface, or locally with your favorite IDE and deployed to the AbFab server by pushing the code to GitHub. (Vice-versa, changes done through the online interface can be pushed to your repository whenever needed). No NPM, no bundling.

## Quickstart

-   [Deploy a local instance](./docs/deploy.md#deploy-locally)
-   [Tutorial](./docs/tutorial.md)

## License

AbFab is released under the BSD-2 license.
