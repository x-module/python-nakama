# -*- coding: utf-8 -*-

from .authenticate import Authenticate
from ...common.common import Common
from ...common.nakama import AccountResponse
from ...utils.helper import get_request


class Account:
    def __init__(self, common: Common):
        self._common = common
        self._authenticate = Authenticate(common)

    # 获取当前账号信息
    async def get(self) -> AccountResponse:
        result = await get_request(self._common, '/v2/account')
        response = AccountResponse()
        response.from_dict(result)
        return response

    @property
    def authenticate(self):
        return self._authenticate
