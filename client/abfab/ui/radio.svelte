<script>
    export let id;
    export let label;
    export let hint;
    export let disabled = false;
    export let readonly = false;
    export let value;
    export let error;
    export let group;
    let element;
</script>
<pa-checkbox>
    <div class="pa-toggle">
        <div class="pa-checkbox-wrapper">
            <input
                bind:this={element}
                type="radio"
                class="pa-toggle-control pa-no-browser-accessibility-styling"
                class:pa-field-error={!!error}
                id={id}
                name={id}
                value={value}
                bind:group
                disabled={disabled}
                readonly={readonly}
                aria-describedby={(hint || error) && id+'-hint'}
                aria-checked={!!element && element.checked}
                tabindex="0">
            <label class="pa-toggle-label" for={id}>{label}</label>
        </div>
        {#if (hint || error)}
        <small aria-live="polite"
            class="pa-field-help"
            class:pa-field-help-error={!!error}
            id={id + '-hint'}>{error || hint}</small>
        {/if}
    </div>
</pa-checkbox>