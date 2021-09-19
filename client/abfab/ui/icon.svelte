<script>
    export let size = 'medium'; // small, medium, or large
    export let icon;
</script>
<pa-icon>
    <svg class="pa-{size}" on:click>
        <use xlink:href="/~/abfab/pastanaga/icons.svg#{icon}"></use>
    </svg>
</pa-icon>