# -*- coding: utf-8 -*-
from nakama.common.common import Common
from nakama.utils.helper import link


class AccountLink:
    def __init__(self, common: Common):
        self._common = common

    async def email(self, email, password):
        body = {
            'email': email,
            'password': password
        }
        result = await link(self._common, '/v2/account/link/email', body)
        return result

    async def device(self, id):
        body = {
            'id': id
        }
        result = await link(self._common, '/v2/account/link/device', body)
        return result

    async def custom(self, id):
        body = {
            'id': id
        }
        result = await link(self._common, '/v2/account/link/custom', body)
        return result
