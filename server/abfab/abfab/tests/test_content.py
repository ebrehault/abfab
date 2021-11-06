import pytest
import json
from .test_file import save_file

pytestmark = pytest.mark.asyncio


async def test_get_content(container_requester):
    async with container_requester as requester:
        await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Directory", "id": "dir1"})
        )
        await requester(
            "POST", "/db/guillotina/dir1", data=json.dumps({"@type": "Content", "id": "data1", "data": {"name": "Eddy"}})
        )
        await save_file(requester, "hello.svelte")
        await save_file(requester, "hello.svelte.js")
        response, _ = await requester("GET", "/db/guillotina/dir1/data1")
        assert response == {'name': 'Eddy'}

        # if no view, html will just display the json value
        response, _ = await requester("GET", "/db/guillotina/dir1/data1", headers={'Accept': 'text/html'})
        assert response == b"<html><body>{'name': 'Eddy'}</body></html>"

        # viewpath can be passed as parameter
        response, _ = await requester("GET", "/db/guillotina/dir1/data1?viewpath=/dir1/hello.svelte", headers={'Accept': 'text/html'})
        assert response.startswith(b'<!DOCTYPE html>')
        assert b"import Component from '/~/dir1/hello.svelte.js';" in response
        assert b"let response = await API.fetch('./data1');" in response

        # view alias can be defined at directory level
        await requester(
            "PATCH", "/db/guillotina/dir1", data=json.dumps({"data": {"views": {"hello": "./hello.svelte"}}})
        )
        response, _ = await requester("GET", "/db/guillotina/dir1/data1?view=hello", headers={'Accept': 'text/html'})
        assert response.startswith(b'<!DOCTYPE html>')
        assert b"import Component from '/~/dir1/hello.svelte.js';" in response
        assert b"let response = await API.fetch('./data1');" in response

        # "view" is the default view alias
        await requester(
            "PATCH", "/db/guillotina/dir1", data=json.dumps({"data": {"views": {"view": "./hello.svelte"}}})
        )
        response, _ = await requester("GET", "/db/guillotina/dir1/data1", headers={'Accept': 'text/html'})
        assert response.startswith(b'<!DOCTYPE html>')
        assert b"import Component from '/~/dir1/hello.svelte.js';" in response
        assert b"let response = await API.fetch('./data1');" in response

        # basic view mention the view
        response, _ = await requester("GET", "/db/guillotina/dir1/data1/@basic")
        assert response["view"] == "/dir1/hello.svelte"