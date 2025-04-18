# -*- coding: utf-8 -*-
from retry import retry

from nakama.common.nakama import SessionResponse, Envelope, AccountCustom, AccountDevice, AccountEmail


def _get_params(create: bool = True, username: str = None) -> dict[str, str]:
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
    def email(self, payload: AccountEmail, create: bool = None, username: str = None) -> SessionResponse:
        endpoint = "/v2/account/authenticate/email"
        params = _get_params(create=create, username=username)
        result = self._client.request(method=self._method, endpoint=endpoint, payload=payload.to_dict(), params=params)
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        self._client.session = SessionResponse().from_dict(result)
        return self._client.session

    @retry(tries=3, delay=1, backoff=2)
    def custom(self, payload: AccountCustom, create: bool = None, username: str = None) -> SessionResponse:
        endpoint = "/v2/account/authenticate/custom"
        params = _get_params(create=create, username=username)
        result = self._client.request(method=self._method, endpoint=endpoint, payload=payload.to_dict(), params=params)
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        self._client.session = SessionResponse().from_dict(result)
        return self._client.session

    @retry(tries=3, delay=1, backoff=2)
    def device(self, payload: AccountDevice, create: bool = None, username: str = None) -> SessionResponse:
        endpoint = "/v2/account/authenticate/device"
        params = _get_params(create=create, username=username)
        result = self._client.request(method=self._method, endpoint=endpoint, payload=payload.to_dict(), params=params)
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        self._client.session = SessionResponse().from_dict(result)
        return self._client.session

    def logout(self):
        payload = {
            'token': self._client.session.token
        }
        if self._client.session.refresh_token:
            payload['refreshToken'] = self._client.session.refresh_token

        endpoint = '/v2/session/logout'
        result = self._client.request(method="POST", endpoint=endpoint, payload=payload)
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error

    def refresh(self, vars=None):
        payload = {
            'token': self._client.session.refresh_token
        }
        if vars:
            payload['vars'] = vars
        endpoint = '/v2/account/session/refresh'
        result = self._client.request(method="POST", endpoint=endpoint, payload=payload)
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
