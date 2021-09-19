<script>
    export let id;
    export let label;
    export let hint;
    export let disabled = false;
    export let readonly = false;
    export let value;
    export let error;
    export let group = [];

    function onChange({target}) {
        const { value, checked } = target;
        if (checked) {
            group = [...group, value];
        } else {
            group = group.filter(item => item !== value)
        }
    }
</script>
<pa-checkbox>
    <div class="pa-toggle">
        <div class="pa-checkbox-wrapper">
            <input
                type="checkbox"
                class="pa-toggle-control pa-no-browser-accessibility-styling"
                class:pa-field-error={!!error}
                id={id}
                name={id}
                value={value}
                checked={group.includes(value)}
                disabled={disabled}
                readonly={readonly}
                aria-describedby={(hint || error) && id+'-hint'}
                aria-checked={group.includes(value)}
                tabindex="0"
                on:change={onChange}>
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