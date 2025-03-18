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
        body = {
            'token': self._common.session.token
        }
        if self._common.session.refresh_token is not None:
            body['refreshToken'] = self._common.session.refresh_token

        url_path = self._common.http_url + '/v2/session/logout'
        resp = await self._common.http_session.post(url_path, json=body, headers=self._common.auth_header)
        return await resp.json()


    async def refresh(self, vars=None):
        assert self._common.session.refresh_token is not None, 'You must specify refresh token'
        body = {
            'token': self._common.session.refresh_token
        }
        if vars is not None:
            body['vars'] = vars

        url_path = self._common.http_url + '/v2/account/session/refresh'
        result = await self._common.http_session.post(url_path, json=body, headers=self._common.auth_header)
        return await result.json()
