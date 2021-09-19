from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import json
import pytest


def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('abfab')
    else:
        settings['applications'] = ['abfab']


testing.configure_with(base_settings_configurator)


class abfab_Requester(ContainerRequesterAsyncContextManager):  # noqa

    async def __aenter__(self):
        await super().__aenter__()
        resp = await self.requester(
            'POST', '/db/guillotina/@addons',
            data=json.dumps({
                'id': 'abfab'
            })
        )
        return self.requester


@pytest.fixture(scope='function')
async def abfab_requester(guillotina):
    return abfab_Requester(guillotina)
