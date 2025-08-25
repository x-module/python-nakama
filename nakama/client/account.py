# -*- coding: utf-8 -*-
from retry import retry

from nakama.common.nakama import Envelope, AccountResponse
from nakama.utils.utils import GetErrEnvelope


class Account:
    def __init__(self, client):
        self._client = client

    @retry(tries=3, delay=1, backoff=2)
    def get(self) -> AccountResponse:
        endpoint = '/v2/account'
        result = self._client.request(method="GET", endpoint=endpoint)
        envelope = GetErrEnvelope(result)
        if envelope.error.code != 0:
            raise envelope.error
        return AccountResponse().from_dict(result)
