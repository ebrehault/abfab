<script>
    import AFInput from '/~/abfab/ui/input.svelte';
    import AFButton from '/~/abfab/ui/button.svelte';
    import { API } from '/~/abfab/core.js';
    let username;
    let password;
    let error = '';
    const urlParams = new URLSearchParams(window.location.search);
    const redirect = urlParams.get('from') || '/~/abfab';

    const login = async () => {
        error = '';
        const body = JSON.stringify({
            username,
            password,
        });
        const response = await API.post('/~/@login', body);
        if (response.status === 200) {
            const body = await response.json();
            localStorage.setItem('auth', body.token);
            location.href = redirect;
        } else {
            error = 'Login failed';
        }
    }
</script>
<svelte:head>
    <link rel="stylesheet" href="/~/abfab/pastanaga/pastanaga.css">
</svelte:head>
<main>
    <img src="/~/abfab/abfab.svg">
    <AFInput id="username" bind:value={username} label="Username"></AFInput>
    <AFInput id="password" type="password" bind:value={password} label="Password"></AFInput>
    <div class="message">
        {error}
    </div>
    <AFButton kind="primary" label="Login" on:click={login}></AFButton>
</main>
<style>
    main {
        display: flex;
        flex-direction: column;
        justify-items: center;
        width: 50vw;
        max-height: 100vh;
        padding: 2em;
        margin: 0 auto;
    }
    .message {
        padding-bottom: 1em;
        margin: 0 auto;
        color: var(--color-accent-secondary-dark);
        height: 3.5em;
    }
</style>