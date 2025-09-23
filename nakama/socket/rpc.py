# -*- coding: utf-8 -*-
import json
from typing import Any, Callable

from nakama.common.nakama import Envelope, RpcMsg, PartyMsg
from nakama.socket.handler import requestHandler
from nakama.utils.logger import Logger


class Rpc:
    def __init__(self, socket):
        self._socket = socket
        self._request = {}
        self._logger = Logger(f"{__name__}.{self.__class__.__name__}")

    def __call__(self, rpc: str, params: dict[str, Any], callback: Callable[[RpcMsg], None]):
        cid = '%d' % requestHandler.getCid()
        params = Envelope(
            rpc=RpcMsg(
                id=rpc,
                payload=json.dumps(params),
            ),
            cid=str(cid),
        )
        self._socket.sendMessage(params.to_dict())
        self._request[cid] = callback
        requestHandler.addRequest(cid, self.callRpcResult)

    def callRpcResult(self, cid: int, result: Envelope):
        if cid in self._request:
            self._request[cid](result.party)
            del self._request[cid]
        else:
            self._logger.error("RPC的请求不存在，cid:%s", cid)
