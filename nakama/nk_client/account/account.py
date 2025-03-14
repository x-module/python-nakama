# -*- coding: utf-8 -*-

from .authenticate import Authenticate
from ...common.common import Common
from ...common.nakama import AccountResponse


class Account:
    def __init__(self, common: Common):
        self._common = common
        self._authenticate = Authenticate(common)

    # 获取当前账号信息
    async def get(self) -> AccountResponse:
        url_path = self._common.http_url + '/v2/account'
        resp = await self._common.http_session.get(url_path, headers=self._common.auth_header)
        result = await resp.json()
        accountResponse = AccountResponse()
        accountResponse.from_dict(result)
        return accountResponse

    @property
    def authenticate(self):
        return self._authenticate
