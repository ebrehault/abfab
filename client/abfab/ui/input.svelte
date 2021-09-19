<script>
    import { onMount } from 'svelte';

    export let id;
    export let label;
    export let type = 'text';
    export let placeholder;
    export let hint;
    export let disabled = false;
    export let required = false;
    export let readonly = false;
    export let value;
    export let error;
    let element;

    onMount(() => element.type = type);

</script>
<div class="pa-field">
    <input bind:this={element}
           class="pa-field-control"
           class:pa-field-control-filled={!!value}
           class:pa-field-error={!!error}
           id={id}
           name={id}
           placeholder={placeholder}
           disabled={disabled}
           required={required}
           readonly={readonly}
           aria-describedby={(hint || error) && id+'-hint'}
           bind:value={value}
           on:input on:keyup on:change on:keypress on:keydown on:focus on:blur>
    <label class="pa-field-label" for={id}>{label}</label>
    {#if (hint || error)}
    <small aria-live="polite"
           class="pa-field-help"
           class:pa-field-help-error={!!error}
           id={id + '-hint'}>{error || hint}</small>
    {/if}
</div>