<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';

    export let content;

    let textarea;
    let codeMirror;
    let isInitialized = false;
    const dispatch = createEventDispatcher();
    const modes = {
        js: {
            name: 'javascript',
            json: false
        },
        json: {
            name: 'javascript',
            json: true
        },
        svelte: {
            name: 'handlebars',
            base: 'text/html'
        },
        md: {
            name: 'markdown'
        }
    };

    export function saveFile(value) {
        if (!value) {
            value = codeMirror.getValue();
        }
        dispatch('save', value);
    }

    async function loadPlugins() {
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/mode/simple.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/mode/multiplex.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/mode/javascript/javascript.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/mode/handlebars/handlebars.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/mode/htmlmixed/htmlmixed.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/mode/xml/xml.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/mode/css/css.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/mode/markdown/markdown.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/edit/closebrackets.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/edit/closetag.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/edit/continuelist.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/comment/comment.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/fold/foldcode.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/fold/foldgutter.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/fold/brace-fold.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/fold/xml-fold.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/fold/indent-fold.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/fold/markdown-fold.js');
        await import('https://www.unpkg.com/codemirror@5.63.3/addon/fold/comment-fold.js');
    }

    onMount(async () => {
        isInitialized = false;
        await import('https://www.unpkg.com/codemirror@5.63.3/lib/codemirror.js');
        await loadPlugins();
        init();
    });

    $: if (isInitialized) {
        codeMirror.setValue(content);
        setMode();
    }
    
    function init() {
        const opts = {
			lineNumbers: true,
			lineWrapping: true,
			indentWithTabs: false,
			indentUnit: 4,
			tabSize: 4,
			value: '',
			autoCloseBrackets: true,
			autoCloseTags: true,
            extraKeys: {
                'Enter': 'newlineAndIndentContinueMarkdownList',
                'Ctrl-/': 'toggleComment',
                'Cmd-/': 'toggleComment',
                'Ctrl-Q': function (cm) {
                    cm.foldCode(cm.getCursor());
                },
                'Cmd-Q': function (cm) {
                    cm.foldCode(cm.getCursor());
                },
                'Ctrl-S': function (cm) {
                    saveFile(cm.getValue());
                },
                'Cmd-S': function (cm) {
                    saveFile(cm.getValue());
                },
            },
			foldGutter: true,
			gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
            theme: 'blackboard',
		};

        codeMirror = CodeMirror.fromTextArea(textarea, opts);
        isInitialized = true;
    };

    function setMode() {
        const filename = location.pathname.replace('/@edit', '').split('/').pop();
        const mode = filename.includes('.') ? filename.split('.').pop() : 'json';
        codeMirror.setOption('mode', modes[mode] || { name: mode });
    }
</script>
<textarea bind:this={textarea}></textarea>
<svelte:head>
    <link rel="stylesheet" href="https://www.unpkg.com/codemirror@5.63.3/lib/codemirror.css">
    <link rel="stylesheet" href="https://www.unpkg.com/codemirror@5.63.3/theme/blackboard.css">
</svelte:head>
<style>
    textarea {
        display: none;
    }
    :global(.CodeMirror) {
        width: 100%;
        height: calc(100vh - 40px) !important;
    }
</style>