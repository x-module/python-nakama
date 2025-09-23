# -*- coding: utf-8 -*-
import time
from typing import Callable

from PyQt5.QtCore import pyqtSignal, QObject

from nakama.common.nakama import Envelope
from nakama.utils.logger import Logger


class RequestHandler(QObject):

    rpcResponseReceived: pyqtSignal = pyqtSignal(str, Envelope)

    def __init__(self):
        super().__init__()
        self.cidCount = 0
        self.requests = {}
        self._logger = Logger(f"{__name__}.{self.__class__.__name__}")
        self.rpcResponseReceived.connect(self.requestCallback)

    def getCid(self) -> int:
        if len(self.requests.keys()) == 0:
            self.cidCount = 0
        self.cidCount += 1
        return self.cidCount

    def requestCallback(self, cid, result):
        callback = self.requests[cid]
        if callback is not None:
            callback(cid, result)

    def addRequest(self, cid: str, request: Callable[[str], None]):
        self.requests[cid] = request

    def handleResult(self, cid: str, result):
        callback = self.requests[cid]
        if callback is not None:
            self.rpcResponseReceived.emit(cid, result)
            del self.requests[cid]
        else:
            self._logger.error("未知网路请求，cid:%s,response:%s", cid, result)


requestHandler = RequestHandler()
