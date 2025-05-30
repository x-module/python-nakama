# -*- coding: utf-8 -*-
import threading
import time

import json
from typing import Optional, Callable, Any, Dict

from nakama.client.client import Client
from nakama.common.nakama import Envelope, NotificationsMsg, Notification
from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.socket.match import Match
from nakama.socket.notice import NoticeHandler
from nakama.socket.party import Party
from nakama.socket.handler import requestHandler
from nakama.socket.rpc import Rpc
import websocket

from nakama.utils.logger import Logger


class Socket:
    def __init__(self, client: Client):
        self._host = client.host
        self._port = client.port
        self._token = client.session.token
        self._ssl = client.ssl
        self._client = client
        self._websocket = None
        self._callbacks: Dict[str, Callable] = {}
        self.rpc = Rpc(self)
        self.party = Party(self)
        self.match = Match(self)

        self.logger = Logger(__name__)
        self.active = False
        self._noticeHandler = NoticeHandler()
        self.connected = False

    @property
    def websocket(self):
        return self._websocket

    @property
    def wsUrl(self) -> str:
        protocol = "wss" if self._ssl else "ws"
        return f"{protocol}://{self._host}:{self._port}/ws"

    def setNoticeHandler(self, handler: NoticeHandlerInter):
        self._noticeHandler.setHandler(handler)

    def onOpen(self, ws):
        self.logger.debug("[%s]连接成功!", self.wsUrl)
        self.connected = True
        # 状态检测线程
        self.active = True
        threading.Thread(target=self.monitor).start()

    def onError(self, ws, error):
        print("on_error", error)

    def onClose(self, ws, close_status_code, close_msg):
        self.logger.debug("[%s]连接关闭!", self.wsUrl)
        self.active = False

    def onMessage(self, ws, message):
        self.logger.debug("接收到原始消息:%s", message)
        envelope = Envelope().from_json(message)
        # 获取当前设置的消息类型
        self.logger.debug("接受解析后消息[%s]:%s", envelope.cid, envelope.notifications)
        if envelope.cid:
            requestHandler.handleResult(envelope.cid, envelope)
        else:
            msg = json.loads(message)
            for msgType in msg.keys():
                self.logger.debug("普通系统消息:%s", envelope.notifications)
                self._noticeHandler.handleEvent(msgType, envelope)

    def connect(self):
        threading.Thread(target=self._connect).start()
        while not self.connected:
            time.sleep(1)

    def onPong(self,ws, message):
        self.logger.debug("接收到Pong消息:%s", message)
        self._noticeHandler.handleEvent("pong", Envelope())
    def _connect(self):
        self.logger.debug("[%s]连接中...", self.wsUrl)
        if not self._websocket:
            self._websocket = websocket.WebSocketApp(self.wsUrl,
                                                     on_pong=self.onPong,
                                                     on_open=self.onOpen,
                                                     on_message=self.onMessage,
                                                     on_error=self.onError,
                                                     header={"Authorization": f"Bearer {self._token}"},
                                                     on_close=self.onClose)
        self._websocket.run_forever(
            # reconnect=1,
            ping_interval=3,  # 每30秒发送一次Ping
            ping_timeout=2  # 等待Pong响应的超时时间
        )

    def monitor(self):
        while self.active:
            if not self._websocket.sock or not self._websocket.sock.connected:
                self.logger.warning("检测到连接断开!")
                self.active = False
            time.sleep(1)

    def disconnect(self) -> None:
        """断开连接"""
        if self._websocket:
            self._websocket.close()
            self._websocket = None
