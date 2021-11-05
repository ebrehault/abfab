<script>
    import AFButton from '/~/abfab/ui/button.svelte';
    import { clickOutside } from '/~/abfab/ui/clickOutside.js';

    export let label = 'Menu';
    export let toTop = false;
    export let icon = 'more-horizontal';
    let showMenu = false;
</script>
<div class="container">
    <AFButton kind="primary" aspect="basic" {icon} size="small"
        	  on:click={() => showMenu = !showMenu}>{label}</AFButton>
    {#if showMenu}
    <div class="menu" class:top={toTop} class:bottom={!toTop} use:clickOutside on:clickoutside={() => showMenu = false}>
        <slot></slot>
    </div>
    {/if}
</div>
<style>
    .container {
        position: relative;
        display: inline-block;
    }
    .menu {
        position: absolute;
        background-color: var(--color-neutral-primary-lightest);
        z-index: 400;
        box-shadow: 0 1px 0.5rem rgb(2 19 34 / 12%), 0 0 0.25rem rgb(2 19 34 / 10%);
        border-radius: .125rem;
        text-align: left;
    }
    .top {
        bottom: 2em;
    }
    .bottom {
        top: 0.5em;
    }
</style>