<script>
    import { AbFabStore, getRealPath, API} from '/~/abfab/core.js';
    import { onDestroy } from 'svelte';
    import { derived } from 'svelte/store';

    export let component;
    export let content;

    // Adapted from https://github.com/sveltejs/kit/blob/master/packages/kit/src/runtime/client/router.js
    if ('scrollRestoration' in history) {
        history.scrollRestoration = 'manual';
    }
    addEventListener('beforeunload', () => {
        history.scrollRestoration = 'auto';
    });
    addEventListener('load', () => {
        history.scrollRestoration = 'manual';
    });
    addEventListener('click', (event) => {
        if (event.button || event.which !== 1) return;
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        if (event.defaultPrevented) return;

        const a = find_anchor(event.target);
        if (!a) return;
        if (!a.href) return;
        const rel = (a.getAttribute('rel') || '').split(/\s+/);
        if (a.hasAttribute('download') || (rel && rel.includes('external'))) {
            return;
        }
        if (a instanceof SVGAElement ? a.target.baseVal : a.target) return;

        const svg = typeof a.href === 'object' && a.href.constructor.name === 'SVGAnimatedString';
		const href = String(svg ? a.href.baseVal : a.href);

        if (href === location.href) {
            if (!location.hash) event.preventDefault();
            return;
        }
        event.preventDefault();
        navigate(href);
    });
    function find_anchor(node) {
        while (node && node.nodeName.toUpperCase() !== 'A') node = node.parentNode;
        return node;
    }
    onpopstate = (event) => navigate(event.target.location.pathname);

    async function navigate(href) {
        history.pushState({}, '', href);
        const [path, query] = href.split('?');
        AbFabStore.update((state) => ({ ...state, query, path: getRealPath(href), _navigateTo: '' }));
        if (path.endsWith('/@edit')) {
            // TODO: move to editor.js and declare dynamically
            const response = await API.get(path.replace('/@edit', '/@edit-data'));
            const code = await response.text();
            const module = await import(`/~/abfab/editor/editor.svelte`);
            content = code;
            component = module.default;
        } else {
            const response = await API.get(`${path}/@basic${!!query ? '?' + query : ''}`);
            const basicData = await response.json();
            if (basicData.type_name === 'Content') {
                const module = await import(getRealPath(basicData.view));
                component = module.default;
                content = basicData.data;
            } else {
                const module = await import(getRealPath(basicData.path));
                component = module.default;
                const queryContent = (new URLSearchParams(query)).get('content');
                content = queryContent ? JSON.parse(decodeURIComponent(queryContent)) : {};
            }   
        }
    }

    const subscriptions = [];
    const _navigateTo = derived(AbFabStore, (state) => state._navigateTo);
    subscriptions.push(_navigateTo.subscribe(value => {
        if(value) {
            navigate(value);
        }
    }));
	onDestroy(() => subscriptions.map(unsubscribe => unsubscribe()));
</script>
<svelte:component this={component} content={content}></svelte:component>
