<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';

    export let context;

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
        await import('/~/libs/codemirror/addon/mode/simple.js');
        await import('/~/libs/codemirror/addon/mode/multiplex.js');
        await import('/~/libs/codemirror/mode/javascript/javascript.js');
        await import('/~/libs/codemirror/mode/handlebars/handlebars.js');
        await import('/~/libs/codemirror/mode/htmlmixed/htmlmixed.js');
        await import('/~/libs/codemirror/mode/xml/xml.js');
        await import('/~/libs/codemirror/mode/css/css.js');
        await import('/~/libs/codemirror/mode/markdown/markdown.js');
        await import('/~/libs/codemirror/addon/edit/closebrackets.js');
        await import('/~/libs/codemirror/addon/edit/closetag.js');
        await import('/~/libs/codemirror/addon/edit/continuelist.js');
        await import('/~/libs/codemirror/addon/comment/comment.js');
        await import('/~/libs/codemirror/addon/fold/foldcode.js');
        await import('/~/libs/codemirror/addon/fold/foldgutter.js');
        await import('/~/libs/codemirror/addon/fold/brace-fold.js');
        await import('/~/libs/codemirror/addon/fold/xml-fold.js');
        await import('/~/libs/codemirror/addon/fold/indent-fold.js');
        await import('/~/libs/codemirror/addon/fold/markdown-fold.js');
        await import('/~/libs/codemirror/addon/fold/comment-fold.js');
    }

    onMount(async () => {
        isInitialized = false;
        await import('/~/libs/codemirror/lib/codemirror.js');
        await loadPlugins();
        init();
    });

    $: if (isInitialized) {
        codeMirror.setValue(context);
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
    <link rel="stylesheet" href="/~/libs/codemirror/lib/codemirror.css">
    <link rel="stylesheet" href="/~/libs/codemirror/theme/blackboard.css">
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