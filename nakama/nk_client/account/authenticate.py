# -*- coding: utf-8 -*-

from ...common.common import Common


class Authenticate(object):
    def __init__(self, common: Common):
        self._common = common

    # 自定义登录
    async def custom(self, id: str, vars=None, create: bool = True, username: str = None):
        params = {}
        if create is not None:
            params["create"] = create and 'true' or 'false'
        if username is not None:
            params["username"] = username
        body = {
            "id": id,
        }
        if vars is not None:
            body["vars"] = vars
        url_path = self._common.http_url + '/v2/account/authenticate/custom'
        result = await   self._common.http_session.post(url_path, params=params, json=body, headers=self._common.auth_header)
        result = await result.json()
        self._common.token = result["token"]
        return result
