<script>
    import { getRealPath, getCorePath, Content } from '/~/abfab/core.js';
    import AFTextarea from '/~/abfab/ui/textarea.svelte';
    import AFIcon from '/~/abfab/ui/icon.svelte';
    import AFButton from '/~/abfab/ui/button.svelte';
    import AFDropdown from '/~/abfab/ui/dropdown.svelte';
    import AFInput from '/~/abfab/ui/input.svelte';
    import { onMount } from 'svelte';

    export let componentPath;
    export let contentPath;
    export let hasGit;
    let iframeSnippet = '';
    let elementSnippet = '';
    let link = '';
    let status;
    let branch = '';
    let commit = '';
    const isLib = getCorePath(contentPath) === '/libs';
    let lib = '';
    let installing = false;

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

    async function push() {
        const id = contentPath.split('/').pop();
        await fetch(`/_utils/push/${id}/${branch}`, {
            method: 'POST',
            body: JSON.stringify({ commit }),
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        });
    }
    async function pull() {
        const id = contentPath.split('/').pop();
        await fetch(`/_utils/pull/${id}/${branch}`, { method: 'POST' });
    }
    async function install() {
        installing = true;
        await fetch(`/_utils/install/${lib}`, { method: 'POST' });
        installing = false;
    }
</script>

<section>
    <h3>Publish</h3>
    {#if status}
        <p>
            Status: {status.published ? 'Published' : 'Private'}
            {status.inherit ? '(inherited)' : ''}
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
            <a target="_new" href={link}>Open in its own tab <AFIcon size="small" icon="external" /></a>
        </p>
        <h3>Embed</h3>
        <AFTextarea label="Web component snippet" bind:value={elementSnippet} />
        <AFTextarea label="iframe snippet" bind:value={iframeSnippet} />
    {/if}
    {#if hasGit}
        <h3>Git sync</h3>
        <AFInput bind:value={branch} label="Branch" placeholder="my-branch" />
        <div class="sync-action">
            <div>
                <h4>Push</h4>
                <p>
                    All the changes made in this directory will be pushed to the <code>{branch}</code> branch on your Git
                    repository.
                </p>
                <AFInput
                    bind:value={commit}
                    label="Commit message"
                    placeholder="Short description of the changes"
                    disabled={!branch}
                />
            </div>
            <div>
                <AFButton kind="primary" icon="arrow-up" on:click={push} disabled={!branch}>Push</AFButton>
            </div>
        </div>
        <div class="action-container">
            <div>
                <h4>Pull</h4>
                <p>
                    The current code from <code>{branch}</code> branch on your Git repository will be deployed here. If
                    some changes have been made through this online inerface since the last syncing, they will be pushed
                    to the <code>abfab-online-backup</code> branch before any code is deployed, so nothing gets lost by mistake.
                </p>
            </div>
            <div>
                <AFButton kind="primary" icon="arrow-down" on:click={pull} disabled={!branch}>Pull</AFButton>
            </div>
        </div>
    {/if}
    {#if isLib}
        <h3>Install libraries</h3>
        <p>
            Allows to install a library and all its dependencies in the <code>/libs</code> directory.
        </p>
        <div class="action-container install-section">
            <AFInput bind:value={lib} label="Library" placeholder="svelte-cubed" />
            <AFButton kind="primary" icon="arrow-down" on:click={install} disabled={!lib || installing}
                >Install</AFButton
            >
        </div>
        {#if installing}<p>Installing…</p>{/if}
    {/if}
</section>

<style>
    section {
        margin: 0 1em;
        width: calc(50vw - 7em);
    }
    :global(textarea) {
        font-family: monospace;
    }
    .publish-buttons {
        display: flex;
        flex-direction: column;
        padding: 0.5em;
    }
    .action-container {
        display: flex;
    }
    :global(.install-section .pa-field) {
        width: 100%;
    }
    :global(.install-section .pa-button) {
        height: 48px;
    }
</style>
