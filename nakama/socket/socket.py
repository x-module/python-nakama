# -*- coding: utf-8 -*-
import json
from typing import Optional, Callable, Dict

from nakama.common.nakama import Envelope, ErrorMsg
from nakama.inter import ClientInter
from nakama.socket.handler import requestHandler
from nakama.socket.notice import NoticeHandler
from nakama.socket.party import Party
from nakama.socket.rpc import Rpc
from nakama.utils.logger import Logger
from nakama.utils.websocket import WebSocketClient


class Socket(WebSocketClient):
    def __init__(self, client: ClientInter):
        super().__init__()
        self._client = client
        self._callbacks: Dict[str, Callable] = {}
        self._onError: Optional[Callable] = None
        self._onClose: Optional[Callable] = None
        self._onConnect: Optional[Callable] = None

        self.logger = Logger(f"{__name__}.{self.__class__.__name__}")
        self._noticeHandler = NoticeHandler()

        self.party = Party(self)
        self.rpc = Rpc(self)

        self.init()

    def init(self):
        self.setToken(self._client.getSession().token)
        self.setUrl(self.url())
        self.messageReceived.connect(self.onMessageReceived)
        self.connectionChanged.connect(self.onConnectionChanged)

    def setOnError(self, handler: Callable):
        self._onError = handler

    def setOnClose(self, handler: Callable):
        self._onClose = handler

    def setOnConnect(self, handler: Callable):
        self._onConnect = handler

    def url(self) -> str:
        protocol = "wss" if self._client.config().ssl else "ws"
        return f"{protocol}://{self._client.config().host}:{self._client.config().port}/ws"

    def close(self):
        self.close()

    def onConnectionChanged(self, connected, message):
        """处理连接状态变化"""
        self.logger.debug(f"处理连接状态变化: {message}")
        if connected:
            self.onOpen()
            if self._onConnect:
                self._onConnect(message)
        else:
            self.onClose()
            if self._onClose:
                self._onClose(message)

    def onOpen(self):
        self.logger.debug("[%s]连接成功!", self.url())

    def onError(self, ws, error):
        self.logger.error("socket connect error:{}".format(error))
        self._noticeHandler.handleEvent("on_close", Envelope(
            error=ErrorMsg(
                code=1001,
                message="Socket 异常!，error:{}".format(error)
            )
        ))

    def onClose(self):
        self.logger.debug("[%s]连接关闭", self.url)
        self._noticeHandler.handleEvent("on_close", Envelope(
            error=ErrorMsg(
                code=1000,
                message="{}连接关闭!".format(self.url),
            )
        ))

    def onMessageReceived(self, message):
        # self.logger.debug("接收到原始消息:%s", message)
        envelope = Envelope().from_json(message)
        # 获取当前设置的消息类型
        # self.logger.info("接受解析后消息[%s]:%s", envelope.cid, envelope)
        if envelope.cid:
            self.logger.debug("RPC消息:%s", envelope.notifications)
            requestHandler.handleResult(envelope.cid, envelope)
        else:
            msg = json.loads(message)
            for msgType in msg.keys():
                self.logger.info("普通系统消息:%s", envelope.notifications)
                self._noticeHandler.handleEvent(msgType, envelope)
