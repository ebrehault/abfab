from guillotina import configure
from guillotina.component import get_multi_adapter
from guillotina.behaviors.attachment import IAttachment
from guillotina.api.content import DefaultGET
from guillotina.response import HTTPFound, Response
from guillotina.exceptions import Unauthorized
from guillotina.interfaces import IFileManager, IContainer, IPrincipalRoleMap
from guillotina.utils import get_current_container, navigate_to, get_object_url, get_content_path, get_registry, get_security_policy
from abfab.content import IFile, IDirectory, IContent, IAbFabEditable, IAbFabRegistry
from urllib.parse import urlparse
from pathlib import PurePath

ANONYMOUS_USER_ID = "Anonymous User"

def get_view_by_name(name, content):
    parent = content.__parent__
    if parent.type_name == 'Container':
        return None
    else:
        if parent.data and parent.data.get('views') and (parent.data['views'].get(name) or parent.data['views'].get('view')):
            view_path = parent.data['views'][name] or parent.data['views']['view']
            if view_path.startswith('.'):
                return str(PurePath(get_content_path(parent)).joinpath(view_path))
            else:
                return view_path
        else:
            return get_view_by_name(name, parent)

async def get_object_by_path(path):
    container = get_current_container()
    return await navigate_to(container, path)

async def get_last_modified():
    registry = await get_registry()
    config = registry.for_interface(IAbFabRegistry)
    if config is None:
        return "0"
    return config["lastFileChange"] or "0"

def check_permission(obj):
    policy = get_security_policy()
    if not policy.check_permission("guillotina.ViewContent", obj):
        raise Unauthorized("Cannot access content")

def get_status(context):
    status = None
    prinrole = IPrincipalRoleMap(context)._bycol
    if prinrole.get(ANONYMOUS_USER_ID) and prinrole[ANONYMOUS_USER_ID].get("guillotina.Reader"):
        if prinrole[ANONYMOUS_USER_ID]["guillotina.Reader"].get_name() == "Allow":
            status = "public"
        else:
            status = "private"
    return status

async def view_source(context, request, content_type=None):
    behavior = IAttachment(context)
    await behavior.load(create=False)
    field = IAttachment["file"].bind(behavior)
    adapter = get_multi_adapter((context, request, field), IFileManager)
    last_change = await get_last_modified()
    return await adapter.download(disposition="inline", content_type=content_type, extra_headers={'ETag': last_change})

async def wrap_component(request, js_component, path_to_content, type='json'):
    get_content = ""
    if path_to_content:
        path_to_content = (path_to_content.startswith('/') and "/~" + path_to_content) or path_to_content
        get_content = """import {{API, redirectToLogin}} from '/~/abfab/core.js';
let content;
try {{
    let response = await API.fetch('{path_to_content}');
    content = await response.{type}();
}} catch (e) {{
    redirectToLogin();
}}""".format(path_to_content=path_to_content, type=type)
    else:
        content = request.query.get('content', {})
        get_content = """let content = {content}""".format(content=content)
    body = """<!DOCTYPE html>
<html lang="en">
<script type="module">
    import Component from '/~{component}';
    import Main from '/~/abfab/main.svelte.js';
    {get_content}
    const component = new Main({{
        target: document.body,
        props: {{content, component: Component}},
    }});
    export default component;
</script>
</html>
""".format(component=get_content_path(js_component), get_content=get_content)
    last_change = await get_last_modified()
    return Response(
        content=body,
        status=200,
        headers={
            'ETag': last_change,
        }
    )

@configure.service(context=IFile, method='GET',
                   permission='guillotina.Public', allow_access=True)
async def get_file(context, request):
    if context.id.endswith(".svelte") and 'raw' not in request.query:
        js = await get_object_by_path(get_content_path(context) + '.js')
        if "text/html" in request.headers["ACCEPT"]:
            return await wrap_component(request, js, None)
        else:
            return await view_source(js, request)
    return await view_source(context, request)

async def get_index(context, request):
    path = context.id + '/'
    entrypoint = context.module or context.main
    if entrypoint and entrypoint.startswith('./'):
        entrypoint = entrypoint[2:]
    if entrypoint:
        return HTTPFound(path + entrypoint)
    if "text/html" in request.headers.get("ACCEPT"):
        index_html = await context.async_get('index.html')
        if index_html:
            return HTTPFound(path + 'index.html')
    else:
        index_mjs = await context.async_get('index.mjs')
        if index_mjs:
            return HTTPFound(path + 'index.mjs')
        index_js = await context.async_get('index.js')
        if index_js:
            return HTTPFound(path + 'index.js')

@configure.service(context=IDirectory, method='GET',
                   permission='guillotina.ViewContent', allow_access=True)
async def get_directory(context, request):
    return await get_index(context, request)

@configure.service(context=IContent, method='GET',
                   permission='guillotina.Public', allow_access=True)
async def get_view_or_data(context, request):
    if "text/html" in request.headers["ACCEPT"]:
        view_path = request.query.get('viewpath')
        if not view_path:
            view_name = request.query.get('view')
            if not view_name and context.view:
                view_path = context.view
            else:
                view_path = get_view_by_name(view_name or 'view', context)
        if not view_path:
            check_permission(context)
            return context.data
        if view_path.endswith('.svelte'):
            view_path += '.js'
        view = await get_object_by_path(view_path)
        if view.type_name == 'Directory':
            return await get_index(view, request)
        if view.content_type == "application/javascript" or view.id.endswith('.svelte'):
            return await wrap_component(request, view, './' + context.id)
        else:
            check_permission(context)
            return await view_source(view, request)
    else:
        check_permission(context)
        return context.data

@configure.service(context=IAbFabEditable, method='GET', name='@edit',
                   permission='guillotina.Public', allow_access=True)
@configure.service(context=IContainer, method='GET', name='@edit',
                   permission='guillotina.Public', allow_access=True)
async def run_editor(context, request):
    editor_view = await get_object_by_path('/abfab/editor/editor.svelte')
    return await wrap_component(request, editor_view, './@edit-data', 'text')

@configure.service(context=IFile, method='GET', name='@edit-data',
                   permission='guillotina.ViewContent', allow_access=True)
async def get_editable_file(context, request):
    return await view_source(context, request, content_type="text/plain")

@configure.service(context=IDirectory, method='GET', name='@allfiles',
                   permission='guillotina.AccessContent', allow_access=True)
async def get_all_files(context, request):
    children = []
    async for _, obj in context.async_items():
        children.append({"type": obj.type_name, "url": get_object_url(obj), "path": get_content_path(obj)})
        if obj.type_name == 'Directory':
            sub = await get_all_files(obj, request)
            children += sub
    return children

@configure.service(context=IDirectory, method='GET', name='@tree',
                   permission='guillotina.AccessContent', allow_access=True)
@configure.service(context=IContainer, method='GET', name='@tree',
                   permission='guillotina.AccessContent', allow_access=True)
async def get_tree(context, request, depth=3):
    children = []
    depth = depth - 1
    async for _, obj in context.async_items():
        data = {"type": obj.type_name, "path": get_content_path(obj)}
        if obj.type_name == 'Directory':
            if depth > 0:
                data["children"] = await get_tree(obj, request, depth)
            else:
                data["not_loaded"] = True
        children.append(data)
    return children

@configure.service(context=IDirectory, method='GET', name='@contents',
                   permission='guillotina.AccessContent', allow_access=True)
async def get_contents(context, request):
    children = []
    async for _, obj in context.async_items():
        if obj.type_name == "Content":
            data = {"path": get_content_path(obj), "data": obj.data}
            children.append(data)
    return children

@configure.service(context=IContent, method='GET', name='@basic',
                   permission='guillotina.ViewContent', allow_access=True)
@configure.service(context=IContent, method='GET', name='@edit-data',
                   permission='guillotina.ViewContent', allow_access=True)
async def get_content_basic(context, request):
    view_name = request.query.get('view')
    if not view_name and context.view:
        view_path = context.view
    else:
        view_path = get_view_by_name(view_name or 'view', context)
    return {
        "type_name": context.type_name,
        "path": get_content_path(context),
        "view": view_path,
        "status": get_status(context),
        "data": context.data,
    }

@configure.service(context=IDirectory, method='GET', name='@edit-data',
                   permission='guillotina.ViewContent', allow_access=True)
async def get_directory_edit_data(context, request):
    return {
        "type_name": context.type_name,
        "path": get_content_path(context),
        "status": get_status(context),
        "data": context.data,
    }

@configure.service(context=IContainer, method='GET', name='@edit-data',
                   permission='guillotina.ViewContent', allow_access=True)
async def get_root_edit_data(context, request):
    return {
        "type_name": "Directory",
        "path": "/",
        "data": {},
    }

@configure.service(context=IDirectory, method='GET', name='@basic',
                   permission='guillotina.ViewContent', allow_access=True)
@configure.service(context=IFile, method='GET', name='@basic',
                   permission='guillotina.Public', allow_access=True)
async def get_basic(context, request):
    return {"type": context.type_name, "path": get_content_path(context)}

@configure.service(context=IDirectory, method='GET', name='@default',
                   permission='guillotina.ViewContent', allow_access=True)
@configure.service(context=IContent, method='GET', name='@default',
                   permission='guillotina.ViewContent', allow_access=True)
@configure.service(context=IFile, method='GET', name='@default',
                   permission='guillotina.Public', allow_access=True)
async def get_default(context, request):
    get = DefaultGET(context, request)
    return await get()

@configure.service(context=IFile, method="HEAD", permission="guillotina.Public", allow_access=True)
async def default_head(context, request):
    last_change = await get_last_modified()
    return Response(
        content={},
        status=200,
        headers={
            'ETag': last_change,
        }
    )