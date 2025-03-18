# -*- coding: utf-8 -*-
import base64
import json
import re

from nakama.common.common import Common


class Session:
    def __init__(self, common: Common):
        self._common = common

    def refresh_session(self):
        pass
        # 获取当前账号信息

    async def logout(self):
        url_path = self._common.http_url + '/v2/session/logout'
        resp = await self._common.http_session.get(url_path, headers=self._common.auth_header)
        result = await resp.json()
        return result
