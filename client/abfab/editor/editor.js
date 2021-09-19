import { writable, derived, get } from '/~/libs/svelte/store';
import { getRealPath, API, redirectToLogin } from '/~/abfab/core.js';

export const EditorStore = writable({
    tree: [],
    dirs: [],
    showNavigation: false,
});

export const loadTree = async () => {
    const response = await API.get('/~/@tree');
    if (response.ok) {
        const currentLocation = window.location.pathname.replace('/@edit', '');
        const tree = [
            {
                type: 'Directory',
                path: '/',
                children: await response.json(),
            },
        ];
        const dirs = [];
        const mapTree = (item) => {
            if (item.type === 'Directory') {
                dirs.push(item.path);
            }
            const itemPath = getRealPath(item.path);
            return {
                name: item.path === '/' ? '~' : item.path.split('/').pop(),
                path: itemPath,
                type: item.type,
                children: !!item.children
                    ? item.children.sort((a, b) => a.path.localeCompare(b.path)).map(mapTree)
                    : undefined,
                expanded: currentLocation.startsWith(itemPath),
                selected: currentLocation === itemPath,
            };
        };
        EditorStore.update((state) => ({ ...state, tree: tree.map(mapTree) }));
        EditorStore.update((state) => ({ ...state, dirs }));
    }
};

const _updateTreeItem = (item, target) => {
    if (item.path === target.path) {
        return target;
    } else if (target.path.startsWith(item.path)) {
        return {
            ...item,
            children: (item.children || [])
                .sort((a, b) => a.path.localeCompare(b.path))
                .map((child) => _updateTreeItem(child, target)),
        };
    } else {
        return item;
    }
};

export const updateTreeItem = (target) => {
    const tree = get(EditorStore).tree.map((i) => _updateTreeItem(i, target));
    EditorStore.update((state) => ({ ...state, tree }));
};

export const getTreeItem = (path, tree) => {
    if (!tree) {
        tree = get(EditorStore).tree;
    }
    const exactMatch = tree.find((item) => path === item.path);
    if (exactMatch) {
        return exactMatch;
    } else {
        const match = tree.find((item) => path.startsWith(item.path));
        if (!match) {
            return match;
        } else {
            return getTreeItem(path, match.children || []);
        }
    }
};

const deleteTreeItem = (path, tree) => {
    if (!tree) {
        tree = get(EditorStore).tree;
    }
    if (tree.find((item) => item.path === path)) {
        return tree.filter((item) => item.path !== path);
    } else if (tree.find((item) => path.startsWith(item.path))) {
        return tree.map((item) =>
            path.startsWith(item.path) ? { ...item, children: deleteTreeItem(path, item.children) } : item,
        );
    } else {
        return tree;
    }
};

const addTreeItem = (parentPath, newItem, tree) => {
    if (!tree) {
        tree = get(EditorStore).tree;
    }
    if (!parentPath) {
        tree.push(newItem);
        return tree;
    }
    const parent = tree.find((item) => item.path === parentPath);
    if (parent) {
        if (!parent.children) {
            parent.children = [];
        }
        parent.children.push(newItem);
        return tree.map((item) => (item.path === parentPath ? parent : item));
    } else if (tree.find((item) => parentPath.startsWith(item.path))) {
        return tree.map((item) =>
            parentPath.startsWith(item.path)
                ? { ...item, children: addTreeItem(parentPath, newItem, item.children || []) }
                : item,
        );
    } else {
        return tree;
    }
};

export const showNavigation = derived(EditorStore, (state) => state.showNavigation);

export function saveFile(filepath, type, content) {
    filepath = getRealPath(filepath);
    const path = filepath.split('/');
    const filename = path.pop();
    const container = path.join('/');
    return API.head(filepath)
        .then((res) => {
            if (res.status === 401) {
                redirectToLogin();
            }
            const body = {
                '@type': type,
                id: filename,
            };
            if (content && (type === 'Content' || type === 'Directory')) {
                body.data = JSON.parse(content);
            }
            return res.status === 404
                ? API.post(container, JSON.stringify(body))
                : API.patch(filepath, JSON.stringify(body));
        })
        .then((res) => {
            if (res.status === 401) {
                redirectToLogin();
            }
            if (type === 'File') {
                return API.patch(filepath + '/@upload/file', content, {
                    'Content-Type': 'application/octet-stream',
                    'X-UPLOAD-FILENAME': filename,
                });
            }
        });
}

export async function deleteFile(path) {
    const deletion = await API.delete(path);
    if (deletion.status === 200) {
        EditorStore.update((state) => ({ ...state, tree: deleteTreeItem(path) }));
    }
}

export async function addFile(containerPath, name, type, content) {
    const path = `${containerPath}/${name}`;
    await saveFile(path, type, content);
    EditorStore.update((state) => ({
        ...state,
        tree: addTreeItem(containerPath, {
            name: path.split('/').pop(),
            path: path,
            type: type,
        }),
    }));
}
