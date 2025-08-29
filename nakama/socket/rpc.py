# -*- coding: utf-8 -*-
import json
from typing import Any

from nakama.common.nakama import Envelope, RpcMsg
from nakama.socket.handler import  requestHandler, WSRequestWaiter
from nakama.utils.logger import Logger


class Rpc:
    def __init__(self, socket):
        self._socket = socket
        self.logger = Logger(__name__)

    async def __call__(self, *args, **kwargs):
        requestWaiter = WSRequestWaiter()

        cid = '%d' % requestHandler.getCid()
        requestHandler.addRequest(cid, requestWaiter)
        if len(args) == 0:
            raise Exception("rpc params is empty")
        if len(args) == 1:
            func = args[0]
            params = {}
        elif len(args) == 2:
            func = args[0]
            params = args[1]
        else:
            raise Exception("rpc params is empty")

        params = Envelope(
            rpc=RpcMsg(
                id=func,
                payload=json.dumps(params),
            ),
            cid=str(cid),
        )
        self.logger.debug("rpc info:{}".format(params.rpc))
        await self._socket.send(params.to_dict())
        envelope  = await  requestWaiter
        # print("-------------call rpc result------------:", envelope.to_json())
        if envelope.error.code:
            raise Exception(envelope.error)
        return json.loads(envelope.rpc.payload)
