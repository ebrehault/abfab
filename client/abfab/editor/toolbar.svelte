<script>
    import AFButton from '/~/abfab/ui/button.svelte';
    import AFDropdown from '/~/abfab/ui/dropdown.svelte';
    import {AbFabStore} from '../core.js';
    import {EditorStore} from './editor.js';
 
    let showNavigation = false;

    function logout() {
        AbFabStore.update((state) => ({
            ...state,
            logged: false,
        }))
    }

    function toggleNavigation() {
        EditorStore.update((state) => {
            showNavigation = !state.showNavigation;
            return {
                ...state,
                showNavigation,
            };
        });
        window.dispatchEvent(new Event('resize'));
    }
</script>
<nav>
    <ul>
        <li>
            <AFButton kind="primary" aspect="basic" icon="folder" size="small"
                      active={showNavigation} on:click={toggleNavigation}>Explore</AFButton>
        </li>
        <li>
            <AFButton kind="primary" aspect="basic" icon="search" size="small">Search</AFButton>
        </li>
        <li class="more-button">
            <AFDropdown label="Settings" toTop={true}>
                <div class="menu-item" on:click={logout}>
                    Log out
                </div>
            </AFDropdown>
        </li>
    </ul>
</nav>
<style>
    nav {
        width: 3em;
    }
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        text-align: center;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    li {
        padding: 0.5em 0;
    }
    .more-button {
        margin-top: auto;
        position: absolute;
  		bottom: 0em;
    	left: 0.75em;
    }
    .menu-item {
        padding: 0.25em 1em;
        width: 10em;
        cursor: pointer;
    }
</style>