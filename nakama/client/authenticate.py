# -*- coding: utf-8 -*-
import json

from retry import retry

from nakama.common.nakama import SessionResponse, Envelope, AccountCustom, AccountDevice, AccountEmail, AccountSteam
from nakama.utils.utils import GetErrEnvelope


def getParams(create: bool = True, username: str = None) -> dict[str, str]:
    params = {}
    if create is not None:
        params["create"] = create and 'true' or 'false'
    if username is not None:
        params["username"] = username
    return params


class Authenticate:
    def __init__(self, client):
        self._client = client
        self._method = "POST"

    @retry(tries=3, delay=1, backoff=2)
    async def email(self, payload: AccountEmail, create: bool = None, username: str = None) -> SessionResponse:
        endpoint = "/v2/account/authenticate/email"
        url = f"{self._client.base_url}{endpoint}"
        params = getParams(create=create, username=username)
        print("login url:", url)
        async with self._client.httpSession.post(url, headers=self._client._headers, json=payload.to_dict(), params=params) as response:
            result = await response.json()
            envelope = GetErrEnvelope(result)
            if envelope.error.code != 0:
                raise envelope.error
            self._client.session = SessionResponse().from_dict(result)
            return self._client.session

    @retry(tries=3, delay=1, backoff=2)
    async def custom(self, payload: AccountCustom, create: bool = None, username: str = None) -> SessionResponse:
        endpoint = "/v2/account/authenticate/custom"
        url = f"{self._client.base_url}{endpoint}"
        params = getParams(create=create, username=username)
        async with self._client.httpSession.post(url, headers=self._client._headers, json=payload.to_dict(), params=params) as response:
            result = await response.json()
            envelope = GetErrEnvelope(result)
            if envelope.error.code != 0:
                raise envelope.error
            self._client.session = SessionResponse().from_dict(result)
            return self._client.session

    @retry(tries=3, delay=1, backoff=2)
    async def device(self, payload: AccountDevice, create: bool = None, username: str = None) -> SessionResponse:
        endpoint = "/v2/account/authenticate/device"
        url = f"{self._client.base_url}{endpoint}"
        params = getParams(create=create, username=username)
        async with self._client.httpSession.post(url, headers=self._client._headers, json=payload.to_dict(), params=params) as response:
            result = await response.json()
            envelope = GetErrEnvelope(result)
            if envelope.error.code != 0:
                raise envelope.error
            self._client.session = SessionResponse().from_dict(result)
            return self._client.session

    @retry(tries=3, delay=1, backoff=2)
    async def steam(self, payload: AccountSteam, create: bool = None, username: str = None) -> SessionResponse:
        endpoint = "/v2/account/authenticate/steam"
        url = f"{self._client.base_url}{endpoint}"
        params = getParams(create=create, username=username)
        async with self._client.httpSession.post(url, headers=self._client._headers, json=payload.to_dict(), params=params) as response:
            result = await response.json()
            envelope = GetErrEnvelope(result)
            if envelope.error.code != 0:
                raise envelope.error
            self._client.session = SessionResponse().from_dict(result)
            return self._client.session

    async def logout(self):
        payload = {
            'token': self._client.session.token
        }
        if self._client.session.refresh_token:
            payload['refreshToken'] = self._client.session.refresh_token

        endpoint = '/v2/session/logout'
        url = f"{self._client.base_url}{endpoint}"
        async with self._client.httpSession.post(url, headers=self._client._headers, params=payload) as response:
            result = await response.json()
            print("---------result:", result)
            envelope = GetErrEnvelope(result)
            if envelope.error.code != 0:
                raise envelope.error
            self._client.session = SessionResponse().from_dict(result)
            return self._client.session

    def refresh(self, vars=None):
        payload = {
            'token': self._client.session.refresh_token
        }
        if vars:
            payload['vars'] = vars
        endpoint = '/v2/account/session/refresh'
        result = self._client.request(method="POST", endpoint=endpoint, payload=payload)
        envelope = GetErrEnvelope(result)
        if envelope.error.code != 0:
            raise envelope.error
