# -*- coding: utf-8 -*-
import json
from typing import Any

from nakama.common.nakama import Envelope, RpcMsg
from nakama.socket.handler import RequestWaiter, requestHandler


class Rpc:
    def __init__(self, socket):
        self._socket = socket

    def __call__(self, *args, **kwargs):
        request_waiter = RequestWaiter()
        cid = '%d' % requestHandler.getCid()
        requestHandler.addRequest(cid, request_waiter)
        params = Envelope(
            rpc=RpcMsg(
                id=args[0],
                payload=json.dumps(kwargs),
            ),
            cid=str(cid),
        )
        self._socket.websocket.send(params.to_json())
        envelope = request_waiter.result()
        print("-------------call rpc------------:", envelope.to_json())
        if envelope.error.code:
            raise Exception(envelope.error)
        return json.loads(envelope.rpc.payload)