# -*- coding: utf-8 -*-

from ...common.common import Common
from ...common.nakama import SessionResponse
from ...utils.helper import post_request, authenticate
from ...utils.log import Logger


def get_params(create: bool = True, username: str = None):
    params = {}
    if create is not None:
        params["create"] = create and 'true' or 'false'
    if username is not None:
        params["username"] = username
    return params


class Authenticate(object):
    def __init__(self, common: Common):
        self._common = common
        self.logger = Logger("authenticate")

    # 自定义登录
    async def custom(self, id: str, vars=None, create: bool = True, username: str = None) -> SessionResponse:
        params = get_params(create=create, username=username)
        body = {
            "id": id,
        }
        self.logger.debug("authenticate.custom login,body: %s", body)
        session = await authenticate(self._common, '/v2/account/authenticate/custom', params, body, vars)
        self.logger.debug("authenticate.custom session response: %s", session)
        return session

    async def email(self, email, password, vars=None, create=None, username=None) -> SessionResponse:
        params = get_params(create=create, username=username)
        body = {
            'email': email,
            'password': password
        }
        self.logger.debug("authenticate.email login,body: %s", body)
        session = await authenticate(self._common, '/v2/account/authenticate/email', params, body, vars)
        self.logger.debug("authenticate.email session response: %s", session)
        return session

    async def device(self, id, vars=None, create=None, username=None):
        params = get_params(create=create, username=username)
        body = {
            'id': id
        }
        self.logger.debug("authenticate.device login,body: %s", body)
        session = await authenticate(self._common, '/v2/account/authenticate/device', params, body, vars)
        self.logger.debug("authenticate.device session response: %s", session)
        return session

    async def apple(self, token, vars=None, create=None, username=None):
        params = get_params(create=create, username=username)
        body = {
            'token': token
        }
        self.logger.debug("authenticate.apple login,body: %s", body)
        session = await authenticate(self._common, '/v2/account/authenticate/apple', params, body, vars)
        self.logger.debug("authenticate.apple session response: %s", session)
        return session

    async def steam(self, token, vars=None, create=None, username=None):
        params = get_params(create=create, username=username)
        body = {
            'token': token
        }
        self.logger.debug("authenticate.steam login,body: %s", body)
        session = await authenticate(self._common, '/v2/account/authenticate/steam', params, body, vars)
        self.logger.debug("authenticate.steam session response: %s", session)
        return session
