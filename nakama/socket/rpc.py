# -*- coding: utf-8 -*-
import json
from typing import Any, Callable

from nakama.common.nakama import Envelope, RpcMsg, PartyMsg, ErrorMsg
from nakama.socket.handler import requestHandler
from nakama.utils.logger import Logger


class Rpc:
    def __init__(self, socket):
        self._socket = socket
        self._successCallback = {}
        self._errorCallback = {}
        self._logger = Logger(f"{__name__}.{self.__class__.__name__}")

    def __call__(self, rpc: str, params: dict[str, Any], successCallback: Callable[[RpcMsg], None], errorCallback: Callable[[ErrorMsg], None]):
        cid = '%d' % requestHandler.getCid()
        params = Envelope(
            rpc=RpcMsg(
                id=rpc,
                payload=json.dumps(params),
            ),
            cid=str(cid),
        )
        self._socket.sendMessage(params.to_dict())
        self._successCallback[cid] = successCallback
        self._errorCallback[cid] = errorCallback
        requestHandler.addRequest(cid, self.callRpcResult)

    def callRpcResult(self, cid: int, result: Envelope):
        if result.error and result.error.code:
            self._logger.error("请求RPC异常，err:{}".format(result.error))
            if cid in self._errorCallback:
                self._errorCallback[cid](result.error)
            else:
                self._logger.error("RPC请求失败回调不存在，cid:%s", cid)
        else:
            if cid in self._successCallback:
                self._successCallback[cid](result.rpc)
            else:
                self._logger.error("RPC请求成功回调不存在，cid:%s", cid)

        if cid in self._errorCallback:
            del self._errorCallback[cid]
        if cid in self._successCallback:
            del self._successCallback[cid]
