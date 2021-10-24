<svelte:options tag="abfab-element"></svelte:options>
<script>
    import { getRealPath, API} from '/~/abfab/core.js';
    import { onMount } from 'svelte';

    export let componentpath;
    export let contentpath;
    let component;
    let content;

    onMount(async () => {
        const module = await import(getRealPath(componentpath));
        component = module.default;
        const response = await API.get(contentpath);
        content = await response.json();
    });
</script>
{#if component && content}
<svelte:component this={component} content={content}></svelte:component>
{/if}