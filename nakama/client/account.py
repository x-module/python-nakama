# -*- coding: utf-8 -*-
from retry import retry

from nakama.common.nakama import Envelope, AccountResponse


class Account():
    def __init__(self, client):
        self._client = client

    @retry(tries=3, delay=1, backoff=2)
    def get(self) -> AccountResponse:
        endpoint = '/v2/account'
        result = self._client.request(method="GET", endpoint=endpoint)
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return AccountResponse().from_dict(result)
