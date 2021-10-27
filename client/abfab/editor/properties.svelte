<script>
    import { getRealPath } from '/~/abfab/core.js';
    import AFTextarea from '/~/abfab/ui/textarea.svelte';

    export let componentPath;
    export let contentPath;
    let iframeSnippet = '';
    let elementSnippet = '';
    const link = location.origin + (contentPath ? getRealPath(contentPath) : getRealPath(componentPath));

    const _componentPath = `${location.origin}${getRealPath(componentPath)}`;
    if (contentPath) {
        const _contentPath = `${location.origin}${getRealPath(contentPath)}`;
        iframeSnippet = `<iframe src="${_contentPath}" style="border: none; width: 100%; height: 500px;">`;
        elementSnippet = `<script type="module" src="${location.origin}/~/abfab/element.svelte.js">
<abfab-element contentpath="${_contentPath}" componentpath="${_componentPath}"></abfab-element>`;
    } else {
        iframeSnippet = `<iframe src="${_componentPath}" style="border: none; width: 100%; height: 500px;">`;
        elementSnippet = `<script type="module" src="${location.origin}/~/abfab/element.svelte.js">
<abfab-element componentpath="${_componentPath}"></abfab-element>`;
    }
</script>
<section>
    <h3>Publish</h3>
    <pre>{link}</pre>
    <p>
        <a target="_new" href={link}>Open in its own tab</a>
    </p>
    <h3>Embed</h3>
    <AFTextarea label="Web component snippet" bind:value={elementSnippet} />
    <AFTextarea label="Iframe snippet" bind:value={iframeSnippet} />
</section>
<style>
section {
    margin-left: 1em;
	width: calc(50vw - 5em);
}
</style>