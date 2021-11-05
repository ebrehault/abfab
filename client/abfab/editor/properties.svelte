<script>
    import { getRealPath, Content } from '/~/abfab/core.js';
    import AFTextarea from '/~/abfab/ui/textarea.svelte';
    import AFIcon from '/~/abfab/ui/icon.svelte';
    import AFButton from '/~/abfab/ui/button.svelte';
    import AFDropdown from '/~/abfab/ui/dropdown.svelte';
    import { onMount } from 'svelte';

    export let componentPath;
    export let contentPath;
    let iframeSnippet = '';
    let elementSnippet = '';
    let link = '';
    let status;

    onMount(async () => {
        if (!!contentPath) {
            await getStatus();
        }
    });

    $: {
        if (componentPath) {
            link = location.origin + (contentPath ? getRealPath(contentPath) : getRealPath(componentPath));
        
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
        }
    }

    async function getStatus() {
        status = await Content.status(contentPath);
    }

    async function share(setting) {
        await Content.share(contentPath, setting);
        await getStatus();
    }
</script>
<section>
    <h3>Publish</h3>
    {#if status}
    <p>
        Status: {status.published ? 'Published' : 'Private'} {status.inherit ? '(inherited)' : ''}
        <AFDropdown label="Publish" icon="pencil">
            <div class="publish-buttons">
                <AFButton kind="primary" aspect="basic" on:click={() => share('Allow')}>Publish</AFButton>
                <AFButton kind="destructive" aspect="basic" on:click={() => share('Deny')}>Unpublish</AFButton>
                <AFButton kind="secondary" aspect="basic" on:click={() => share('Unset')}>Reset</AFButton>    
            </div>
        </AFDropdown>
    </p>
    {/if}
    {#if componentPath}
    <pre>{link}</pre>
    <p>
        <a target="_new" href={link}>Open in its own tab <AFIcon size="small" icon="external"></AFIcon></a>
    </p>
    <h3>Embed</h3>
    <AFTextarea label="Web component snippet" bind:value={elementSnippet} />
    <AFTextarea label="iframe snippet" bind:value={iframeSnippet} />
    {/if}
</section>
<style>
    section {
        margin-left: 1em;
        width: calc(50vw - 5em);
    }
    :global(textarea) {
        font-family: monospace;
    }
    .publish-buttons {
        display: flex;
        flex-direction: column;
        padding: 0.5em;
    }
</style>