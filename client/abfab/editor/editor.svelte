<script>
    import VimEditor from './vim.svelte';
    import CodeMirrorEditor from './codemirror.svelte';
    import Viewer from './viewer.svelte';
    import Add from './add.svelte';
    import AFButton from '../ui/button.svelte';
    import Toolbar from './toolbar.svelte';
    import Navigation from './navigation.svelte';
    import { showNavigation, loadTree, saveFile } from './editor.js';
    import { AbFabStore } from '/~/abfab/core.js';
    import { onMount } from 'svelte';
    import { compile } from 'svelte/compiler.mjs';
    import { derived } from '/~/libs/svelte/store';

    export let context;

    let _context = '';
    let error;
    let warnings = [];
    let type;
    let useVim = localStorage.getItem('useVim') ? true : false;
    const RE = new RegExp(/from "(.+\/svelte(\/\w+){0,1})";/g);        
    let play = false;
    let componentPath;
    let viewer;
    let codemirror;
    let mode = 'edit';
    derived(AbFabStore, (state) => state.query)
        .subscribe(query => mode = (new URLSearchParams(query)).get('mode') || 'edit');

    $: {
        let obj;
        try {
            obj = JSON.parse(context);
            type = obj.type_name;
        } catch (e) {
            type = 'File';
        }
        if (type === 'File') {
            _context = context;
        } else if (type === 'Content' || type === 'Directory') {
            _context = JSON.stringify(obj.data || {});
        }
    }
    $: hasError = !!error || warnings.length > 0;
    $: if (hasError) {
        updateErrors();
    }

    function togglePlay() {
        componentPath = location.pathname.replace('/@edit', '');
        play = !play;
        window.dispatchEvent(new Event('resize'));
    }

    function triggerSave() {
        if (codemirror) {
            codemirror.saveFile();
        }
    }
    
    async function save(event) {
        const source = event.detail;
        const ABFAB_ROOT = '/~';
        let js = '';
        const pathname = location.pathname.replace('/~/', '/').replace('/@edit', '');
        const isSvelte = pathname.endsWith('.svelte');
        if (isSvelte) {
            try {
                const result = compile(source, {
                    sveltePath: ABFAB_ROOT + '/libs/svelte',
                });
                error = undefined;
                js = result.js;
                const warningsFixed = result.warnings.length === 0 && warnings.length > 0;
                warnings = result.warnings;
                if (warningsFixed) {
                    updateErrors();
                }
            } catch (e) {
                error = e;
            }
        }
        if (!error) {
            await saveFile(pathname, type, source)
            if (isSvelte) {
                const jsFilePath = pathname + '.js';
                await saveFile(jsFilePath, 'File', js.code.replace(RE, 'from "$1/index.mjs";'))
            }
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
</script>

<svelte:head>
    <link rel="stylesheet" href="/~/abfab/pastanaga/pastanaga.css">
</svelte:head>
<header>
    <img src="/~/abfab/abfab.svg" alt="AbFab logo" />
    <ul>
        {#if !useVim}
        <li>
            <AFButton kind="primary" aspect="basic" icon="check" label="Save" size="small"
                on:click={triggerSave}/>
        </li>
        {/if}
        {#if type === 'File'}
            {#if play}
            <li>
                <AFButton aspect="basic" icon="refresh" label="Refresh" size="small"
                    on:click={refreshViewer}/>
            </li>
            {/if}
            <li>
                <AFButton kind="primary" aspect="basic" icon="play" label="Play" size="small" active={play}
                on:click={togglePlay}/>
            </li>
        {/if}
    </ul>
</header>
<main>
    <Toolbar></Toolbar>
    {#if $showNavigation}
    <Navigation></Navigation>
    {/if}
    <div class="editor-container {play ? 'half' : ''}" class:with-nav={$showNavigation} class:has-error={hasError}>
        {#if type === 'Directory' && mode === 'add'}
            <div class="add-container">
                <Add></Add>
            </div>
        {/if}
        
        <div class="editor">
            {#if useVim}
                <VimEditor context={_context} on:save={save}></VimEditor>
            {:else}
                <CodeMirrorEditor bind:this={codemirror} context={_context} on:save={save}></CodeMirrorEditor>
            {/if}
        </div>
        
        {#if hasError }
            <div class="errors-container">
                <span class="discard-button">
                    <AFButton aspect="solid" icon="cross" label="Discard" size="small"
                        on:click={discardErrors}/>
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
    <Viewer bind:this={viewer} componentPath={componentPath}></Viewer>
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