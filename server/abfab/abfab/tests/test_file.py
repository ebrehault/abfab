import pytest
import json
import os

pytestmark = pytest.mark.asyncio


async def save_file(requester, filename, directory="/db/guillotina/dir1", creation=True):
    if creation:
        await requester(
                "POST", directory, data=json.dumps({"@type": "File", "id": filename})
            )
    with open(os.path.join(os.path.dirname(__file__), filename), "r", encoding='utf-8') as f:
        data = f.read()
        size = len(data)
    await requester(
        "PATCH",
        f"{directory}/{filename}/@upload/file",
        data=data,
        headers={"x-upload-size": f"{size}"},
    )

async def test_get_file(container_requester):
    async with container_requester as requester:
        await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Directory", "id": "dir1"})
        )
        await save_file(requester, "hello.js")
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.js")
        assert response == b"alert('hello');\n"
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.js/@edit-data")
        assert response == b"alert('hello');\n"
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.js/@basic")
        assert response["path"] == "/dir1/hello.js"

async def test_get_svelte_file(container_requester):
    async with container_requester as requester:
        await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Directory", "id": "dir1"})
        )
        await save_file(requester, "hello.svelte")
        await save_file(requester, "hello.svelte.js")
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.svelte")
        assert response == b'<!-- some compiled code -->'
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.svelte", headers={'Accept': 'text/html'})
        assert response.startswith(b'<!DOCTYPE html>')
        assert b"import Component from '/~/dir1/hello.svelte.js';" in response
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.svelte/@edit-data")
        assert response == b"<script>alert('hello');</script>"
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.svelte/@basic")
        assert response["path"] == "/dir1/hello.svelte"

async def test_editor(container_requester):
    async with container_requester as requester:
        await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Directory", "id": "dir1"})
        )
        await save_file(requester, "hello.svelte")
        await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Directory", "id": "abfab"})
        )
        await requester(
            "POST", "/db/guillotina/abfab", data=json.dumps({"@type": "Directory", "id": "editor"})
        )
        await save_file(requester, "editor.svelte", "/db/guillotina/abfab/editor")
        await save_file(requester, "editor.svelte.js", "/db/guillotina/abfab/editor")
        response, _ = await requester("GET", "/db/guillotina/dir1/hello.svelte/@edit")
        assert response.startswith('<!DOCTYPE html>')
        assert "import Component from '/~/abfab/editor/editor.svelte';" in response
