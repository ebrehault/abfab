<script>
    import CodeMirrorEditor from './codemirror.svelte';
    import Viewer from './viewer.svelte';
    import Add from './add.svelte';
    import AFButton from '../ui/button.svelte';
    import Toolbar from './toolbar.svelte';
    import Navigation from './navigation.svelte';
    import Properties from './properties.svelte';
    import { showNavigation, loadTree, saveFile } from './editor.js';
    import { AbFabStore, redirectToLogin } from '/~/abfab/core.js';
    import { onMount, onDestroy } from 'svelte';
    import { derived } from '/~/libs/svelte/store';

    export let content;

    let _content = '';
    let error;
    let warnings = [];
    let type;
    let viewComponent;
    let contentPath;
    let play = false;
    let properties = false;
    let viewer;
    let codemirror;
    let mode = 'edit';
    let hasGit = false;
    const subscriptions = [];
    subscriptions.push(derived(AbFabStore, (state) => state.query)
        .subscribe(query => mode = (new URLSearchParams(query)).get('mode') || 'edit'));
    subscriptions.push(derived(AbFabStore, (state) => state.path).subscribe(() => properties = false));
    
    $: {
        const currentPath = location.pathname.replace('/@edit', '');
        let obj;
        try {
            obj = JSON.parse(content);
            type = obj.type_name;
            viewComponent = obj.view;
        } catch (e) {
            type = 'File';
            contentPath = '';
        }
        if (type === 'File') {
            _content = content;
            viewComponent = currentPath;
        } else if (type === 'Content' || type === 'Directory') {
            _content = JSON.stringify(obj.data || {});
            contentPath = currentPath;
            hasGit = type === 'Directory' && obj.data && obj.data.hasGit;
        }
    }
    $: hasError = !!error || warnings.length > 0;
    $: if (hasError) {
        updateErrors();
    }

    function togglePlay() {
        play = !play;
        properties = false;
        window.dispatchEvent(new Event('resize'));
    }

    function toggleProperties() {
        properties = !properties;
        play = false;
        window.dispatchEvent(new Event('resize'));
    }

    function triggerSave() {
        if (codemirror) {
            codemirror.saveFile();
        }
    }
    
    async function save(event) {
        const source = event.detail;
        const pathname = location.pathname.replace('/~/', '/').replace('/@edit', '');
        const result = await saveFile(pathname, type, source);
        error = result.error;
        warnings = result.warnings;
        updateErrors();
        if (!error) {
            refreshViewer();
        }
    }

    function discardErrors() {
        error = undefined;
        warnings = [];
        updateErrors();
    }

    function updateErrors() {
        window.dispatchEvent(new Event('resize'));
    }

    function refreshViewer() {
        if (viewer) {
            viewer.refresh();
        }
    }

    onMount(() => {
        console.log(`Wheels on fire,\nRolling down the road.\nBest notify my next of kin\nThis wheel shall explode!\n\n`);
        loadTree();
    });

    subscriptions.push(derived(AbFabStore, (state) => state.logged).subscribe(isLogged => {
		if (!isLogged) {
            redirectToLogin();
        }
	}));

    onDestroy(() => subscriptions.map(unsubscribe => unsubscribe()));
</script>

<svelte:head>
    <link rel="stylesheet" href="/~/abfab/pastanaga/pastanaga.css">
</svelte:head>
<header>
    <img src="/~/abfab/abfab.svg" alt="AbFab logo" />
    <ul>
        <li>
            <AFButton kind="primary" aspect="basic" icon="check" size="small"
                on:click={triggerSave}>Save</AFButton>
        </li>
        {#if type !== 'Directory' && play}
            <li>
                <AFButton aspect="basic" icon="refresh" size="small"
                    on:click={refreshViewer}>Refresh</AFButton>
            </li>
        {/if}
        {#if type !== 'Directory'}
        <li>
            <AFButton kind="primary" aspect="basic" icon="play" size="small" active={play}
            on:click={togglePlay}>Play</AFButton>
        </li>
        {/if}
        <li>
            <AFButton kind="primary" aspect="basic" icon="info" size="small" active={properties}
            on:click={toggleProperties}>Play</AFButton>
        </li>
    </ul>
</header>
<main>
    <Toolbar></Toolbar>
    {#if $showNavigation}
    <Navigation></Navigation>
    {/if}
    <div class="editor-container {play || properties ? 'half' : ''}" class:with-nav={$showNavigation} class:has-error={hasError}>
        {#if type === 'Directory' && mode === 'add'}
            <div class="add-container">
                <Add></Add>
            </div>
        {/if}
        
        <div class="editor">
            <CodeMirrorEditor bind:this={codemirror} content={_content} on:save={save}></CodeMirrorEditor>
        </div>
        
        {#if hasError }
            <div class="errors-container">
                <span class="discard-button">
                    <AFButton aspect="solid" icon="cross" size="small"
                        on:click={discardErrors}>Discard</AFButton>
                </span>
                <div class="errors">
                    {#if error} <div class="error">{error.message}<code>{error.frame}</code></div>{/if}
                    {#each warnings as warning}
                    <div class="warning">
                        {warning.message}
                        <code>{warning.frame}</code>
                    </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
    {#if play}
    <Viewer bind:this={viewer} componentPath={viewComponent} {contentPath}></Viewer>
    {/if}
    {#if properties}
    <Properties componentPath={viewComponent} {contentPath} {hasGit}></Properties>
    {/if}
</main>
<style>
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        text-align: center;
    }
    header {
        height: 2em;
        display: flex;
        align-items: center;
    }
    header img {
        height: 2em;
        padding: 0.2em;
        margin-left: 0.2em;
    }
    header ul {
        margin-left: auto;
        margin-right: 1em;
        display: flex;
    }
    main {
        display: flex;
    }
    .editor-container {
        display: flex;
        flex-direction: column;
        height: calc(100vh - 2.5em);
        width: calc(100vw - 3.5em);
        margin: 0px;
        padding: 0px;
        overflow: hidden;
        position: relative;
    }
    .editor-container .editor {
        height: 100%;
    }
    .editor-container.has-error .editor {
        height: 80%;
    }
    .editor-container.half {
        width: 50vw;
    }
    .editor-container.with-nav {
        width: calc(100vw - 250px);
    }
    .editor-container.half.with-nav {
        width: calc(50vw - 10em);
    }
    .errors-container {
        overflow: auto;
        position: relative;
        z-index: 10;
    }
    .errors {
        height: 100%;
        overflow: auto;
        font-size: var(--font-size-xs);
    }
    .errors div {
        color: var(--color-accent-primary-lightest);
        padding: 0.25em;
    }
    .errors .error {
        background-color: var(--color-accent-secondary-dark);
    }
    .errors .warning {
        background-color: var(--color-accent-secondary-default);
    }
    .errors code {
        display: block;
        white-space: pre-wrap;
        padding: 0.25em;
        margin: 0.25em;
        color: var(--color-neutral-primary-lighter);
    }
    .discard-button {
        position: absolute;
        top: 0;
        right: 0;
        padding: 0.25em;
    }
    .add-container {
        position: absolute;
        width: 100%;
        height: 100%;
        z-index: 10;
        background-color: var(--color-neutral-primary-lightest);
    }
</style>