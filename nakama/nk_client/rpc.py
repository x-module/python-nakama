# -*- coding: utf-8 -*-
import asyncio
import json

from nakama.common.common import Common


# RPC 调用
class RPC:
    def __init__(self, common: Common):
        self._common = common

    # call rpc
    async def call(self, func_id, **kwargs):
        assert self._common is not None, "The current account is not logged in, please log in first"
        url_path = self._common.http_url + '/v2/rpc/' + func_id
        result = await self._common.http_session.post(url_path, json=json.dumps(kwargs), headers=self._common.auth_header)
        return await result.json()
