# -*- coding: utf-8 -*-

from ...common.common import Common
from ...common.nakama import SessionResponse


class Authenticate(object):
    def __init__(self, common: Common):
        self._common = common

    def get_params(self, create: bool = True, username: str = None):
        params = {}
        if create is not None:
            params["create"] = create and 'true' or 'false'
        if username is not None:
            params["username"] = username
        return params

    # 自定义登录
    async def custom(self, id: str, vars=None, create: bool = True, username: str = None) -> SessionResponse:
        params = self.get_params(create=create, username=username)
        body = {
            "id": id,
        }
        if vars:
            body["vars"] = vars
        url_path = self._common.http_url + '/v2/account/authenticate/custom'
        result = await   self._common.http_session.post(url_path, params=params, json=body, headers=self._common.auth_header)
        result = await result.json()
        print("==========result:", result)
        session = SessionResponse()
        session.from_dict(result)
        self._common.session = session
        return session

    async def email(self, email, password, vars=None, create=None, username=None) -> SessionResponse:
        params = self.get_params(create=create, username=username)
        body = {
            'email': email,
            'password': password
        }
        if vars: body["vars"] = vars
        url_path = self._common.http_url + '/v2/account/authenticate/email'
        result = await   self._common.http_session.post(url_path, params=params, json=body, headers=self._common.auth_header)
        result = await result.json()
        session = SessionResponse()
        session.from_dict(result)
        self._common.session = session
        return session
