<script>
    import AFInput from '/~/abfab/ui/input.svelte';
    import AFButton from '/~/abfab/ui/button.svelte';
    import { API } from '/~/abfab/core.js';
    let username;
    let password;
    let error = '';
    const urlParams = new URLSearchParams(window.location.search);
    const redirect = urlParams.get('from') || '/~/@edit';

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
    <img src="/~/abfab/abfab.svg" alt="AbFab logo">
    <form on:submit|preventDefault={login}>
        <AFInput id="username" bind:value={username} label="Username"></AFInput>
        <AFInput id="password" type="password" bind:value={password} label="Password"></AFInput>
        <div class="message">
            {error}
        </div>
    	<AFButton kind="primary" type="submit">Login</AFButton>
    </form>
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
    form {
        display: contents;
    }
    .message {
        padding-bottom: 1em;
        margin: 0 auto;
        color: var(--color-accent-secondary-dark);
        height: 3.5em;
    }
</style>