# -*- coding: utf-8 -*-
import json
from typing import Any

from nakama.common.nakama import Envelope, StorageObjectsResponse


class Rpc:
    def __init__(self, client):
        self._client = client

    def call(self, func: str, kwargs: dict[str:Any]):
        endpoint = f'/v2/rpc/{func}'
        result = self._client.request(method="POST", endpoint=endpoint, payload=json.dumps(kwargs))
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return result
