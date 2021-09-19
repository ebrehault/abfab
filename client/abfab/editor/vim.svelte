<script>
    export let context;

    import { VimWasm, checkBrowserCompatibility } from '/~/libs/vim-wasm/vimwasm.js';
    import { EditorStore } from './editor.js';
    import { createEventDispatcher } from 'svelte';
    
    let vim;
    let pathname = location.pathname.replace('/~/', '/').replace('/@edit', '');

    $: if (!vim && $EditorStore.dirs.length > 0) {
        try {
            initVim();
        } catch(e) {
            console.log(e);
        }
    }

    $: if (vim) {
        const _pathname = location.pathname.replace('/~/', '/').replace('/@edit', '');
        if (_pathname !== pathname) {
            const enc = new TextEncoder()
            vim.dropFile(_pathname.slice(1), enc.encode(context));
            pathname = _pathname;
        }
    }

	const dispatch = createEventDispatcher();

    function initVim() {
        const filename = pathname.split('/').pop();
        const isSvelte = filename.endsWith('.svelte');
    
        const errmsg = checkBrowserCompatibility();
        if (errmsg !== undefined) {
            alert(errmsg);
        }
    
        const screenCanvasElement = document.getElementById('vim-canvas');
        vim = new VimWasm({
            canvas: screenCanvasElement,
            input: document.getElementById('vim-input'),
            workerScriptPath: '/~/libs/vim-wasm/vim.js',
        });
    
        // Handle drag and drop
        function cancel(e) {
            e.stopPropagation();
            e.preventDefault();
        }
        screenCanvasElement.addEventListener(
            'dragover',
            (e) => {
                cancel(e);
                if (e.dataTransfer) {
                    e.dataTransfer.dropEffect = 'copy';
                }
            },
            false,
        );
        screenCanvasElement.addEventListener(
            'drop',
            (e) => {
                cancel(e);
                if (e.dataTransfer) {
                    vim.dropFiles(e.dataTransfer.files).catch(console.error);
                }
            },
            false,
        );
    
        vim.onVimExit = (status) => {
            alert(`Vim exited with status ${status}`);
        };
    
        vim.onFileExport = (fullpath, contents) => {
            const decoder = new TextDecoder('utf-8');
            const source = decoder.decode(contents);
            dispatch('save', source);
        };
    
        vim.readClipboard = navigator.clipboard.readText;
        vim.onWriteClipboard = navigator.clipboard.writeText;
        vim.onError = console.error;

        const options = ['set number'];
        if (isSvelte) {
            options.push('set filetype=html');
        }
        options.push('autocmd BufWritePost * export');
        vim.start({
            cmdArgs: [pathname, '-c', options.join('\n')],
            dirs: $EditorStore.dirs,
            files: {
                [pathname]: context,
            },
        });
    }

</script>
<style>
    #vim-editor {
        margin: 0px;
        width: 100%;
        height: 100%;
        background-color: #282c33;
    }
    #vim-canvas {
        padding: 0px;
        width: 100%;
        height: 100%;
    }

    #vim-input {
        width: 1px;
        color: transparent;
        background-color: transparent;
        padding: 0px;
        border: 0px;
        outline: none;
        vertical-align: middle;
        position: absolute;
        top: 0px;
        left: 0px;
    }
</style>
<div id="vim-editor">
    <canvas id="vim-canvas"></canvas>
    <input id="vim-input"
            autocomplete="off"
            autofocus />
</div>

