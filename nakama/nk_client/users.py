# -*- coding: utf-8 -*-
from nakama.common.common import Common
from nakama.common.nakama import UsersResponse
from nakama.utils.helper import get_request


class Users:
    def __init__(self, common: Common):
        self._common = common

    async def get(self, ids=None, usernames=None) -> UsersResponse:
        params = {}
        if ids is not None:
            params['ids'] = ids
        if usernames is not None:
            params['usernames'] = usernames

        return await get_request(self._common, '/v2/user', params)
