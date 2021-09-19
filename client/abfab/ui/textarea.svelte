<script>
    export let id;
    export let label;
    export let placeholder;
    export let hint;
    export let disabled = false;
    export let readonly = false;
    export let value;
    export let error;
</script>
<div class="pa-field">
    <textarea class="pa-field-control pa-field-textarea"
           class:pa-field-control-filled={!!value}
           class:pa-field-error={!!error}
           id={id}
           name={id}
           placeholder={placeholder}
           disabled={disabled}
           readonly={readonly}
           aria-describedby={(hint || error) && id+'-hint'}
           bind:value={value}
           on:input on:keyup on:change on:keypress on:keydown on:focus on:blur></textarea>
    <label class="pa-field-label" for={id}>{label}</label>
    {#if (hint || error)}
    <small aria-live="polite"
           class="pa-field-help"
           class:pa-field-help-error={!!error}
           id={id + '-hint'}>{error || hint}</small>
    {/if}
</div>