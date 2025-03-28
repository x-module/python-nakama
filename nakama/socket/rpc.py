# -*- coding: utf-8 -*-
import json
from typing import Any

from nakama.common.nakama import Envelope, RpcMsg
from nakama.socket.request_handler import RequestHandler, RequestWaiter


class Rpc:
    def __init__(self, socket):
        self._socket = socket

    async def call(self, func: str, kwargs:dict[str:Any]):
        request_waiter = RequestWaiter()
        request_handler = RequestHandler()
        cid = '%d' % request_handler.get_cid()
        request_handler.add_request(cid, request_waiter)
        params = Envelope(
            rpc=RpcMsg(
                id=func,
                payload=json.dumps(kwargs),
            ),
            cid=str(cid),
        )
        await self._socket.websocket.send(params.to_json())
        envelope = await request_waiter
        print("-------------call rpc------------:", envelope.to_json())
        if envelope.error.code:
            raise Exception(envelope.error)
        return json.loads(envelope.rpc.payload)
