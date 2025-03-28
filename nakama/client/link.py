# -*- coding: utf-8 -*-
from retry import retry

from nakama.common.nakama import Envelope, AccountEmail, AccountDevice, AccountCustom


class Link:
    def __init__(self, client):
        self._client = client
        self._method = "PUT"

    @retry(tries=3, delay=1, backoff=2)
    def email(self, payload: AccountEmail):
        endpoint = '/v2/account/link/email'
        result = self._client.request(method=self._method, endpoint=endpoint, payload=payload.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error

    @retry(tries=3, delay=1, backoff=2)
    def device(self, payload: AccountDevice):
        endpoint = '/v2/account/link/device'
        result = self._client.request(method=self._method, endpoint=endpoint, payload=payload.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error

    @retry(tries=3, delay=1, backoff=2)
    def custom(self, payload: AccountCustom):
        endpoint = '/v2/account/link/device'
        result = self._client.request(method=self._method, endpoint=endpoint, payload=payload.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
