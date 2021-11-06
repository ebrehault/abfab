import pytest
import json

pytestmark = pytest.mark.asyncio


async def test_empty_directory(container_requester):
    async with container_requester as requester:
        _, status = await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Directory", "id": "dir1"})
        )
        assert status == 201
        response, _ = await requester("GET", "/db/guillotina/dir1")
        assert response == {}
        response, _ = await requester("GET", "/db/guillotina/dir1/@allfiles")
        assert response == []
        response, _ = await requester("GET", "/db/guillotina/dir1/@tree")
        assert response == []
        response, _ = await requester("GET", "/db/guillotina/dir1/@contents")
        assert response == []
        response, _ = await requester("GET", "/db/guillotina/dir1/@edit-data")
        assert response["type_name"] == "Directory"
        assert response["path"] == "/dir1"
        assert not response["data"]
        response, _ = await requester("GET", "/db/guillotina/dir1/@basic")
        assert response["type"] == "Directory"
        assert response["path"] == "/dir1"
        response, _ = await requester("GET", "/db/guillotina/dir1/@default")
        assert response["@type"] == "Directory"

async def test_directory_with_files(container_requester):
    async with container_requester as requester:
        await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "Directory", "id": "dir1"})
        )
        await requester(
            "POST", "/db/guillotina/dir1", data=json.dumps({"@type": "File", "id": "hello.svelte"})
        )
        await requester(
            "POST", "/db/guillotina/dir1", data=json.dumps({"@type": "Content", "id": "data1", "data": {"name": "Eddy"}})
        )
        await requester(
            "POST", "/db/guillotina/dir1", data=json.dumps({"@type": "Directory", "id": "sub1"})
        )
        response, _ = await requester("GET", "/db/guillotina/dir1/@allfiles")
        assert len(response) == 3
        assert response[0]["path"] == "/dir1/hello.svelte"
        response, _ = await requester("GET", "/db/guillotina/dir1/@tree")
        assert len(response) == 3
        assert response[0]["path"] == "/dir1/hello.svelte"
        response, _ = await requester("GET", "/db/guillotina/dir1/@contents")
        assert len(response) == 1
        assert response[0]["path"] == "/dir1/data1"
        assert response[0]["data"] == {'name': 'Eddy'}
