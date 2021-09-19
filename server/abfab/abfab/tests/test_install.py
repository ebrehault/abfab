import pytest


pytestmark = [pytest.mark.asyncio]


async def test_install(abfab_requester):  # noqa
    async with abfab_requester as requester:
        response, _ = await requester('GET', '/db/guillotina/@addons')
        assert 'abfab' in response['installed']
