# -*- coding: utf-8 -*-
import threading
import time

import json
from typing import Optional, Callable, Any, Dict

from nakama.client.client import Client
from nakama.common.nakama import Envelope, NotificationsMsg, Notification
from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.socket.notice_handler import NoticeHandler
from nakama.socket.party import Party
from nakama.socket.handler import request_handler
from nakama.socket.rpc import Rpc
from tools.logger import Logger
import websocket


class Socket:
    def __init__(self, client: Client):
        self._host = client.host
        self._port = client.port
        self._token = client.session.token
        self._ssl = client.ssl
        self._client = client
        self._websocket = None
        self._callbacks: Dict[str, Callable] = {}
        self.ping_interval = 20  # 心跳间隔(秒)
        self.retry_interval = 5  # 重连间隔(秒)
        self.rpc = Rpc(self)
        self.party = Party(self)

        self.logger = Logger(__name__)
        self.active = False
        self._notice_handler = NoticeHandler()
        self.connected = False

    @property
    def websocket(self):
        return self._websocket

    @property
    def ws_url(self) -> str:
        protocol = "wss" if self._ssl else "ws"
        return f"{protocol}://{self._host}:{self._port}/ws"

    def set_notice_handler(self, handler: NoticeHandlerInter):
        self._notice_handler.set_handler(handler)

    def on_open(self, ws):
        self.logger.debug("[%s]连接成功!", self.ws_url)
        self.connected = True
        # 状态检测线程
        self.active = True
        threading.Thread(target=self.monitor).start()

    def on_error(self, ws, error):
        print("on_error", error)

    def on_close(self, ws, close_status_code, close_msg):
        self.logger.debug("[%s]连接关闭!", self.ws_url)
        self.active = False

    def on_message(self, ws, message):
        self.logger.debug("接收到原始消息:%s", message)
        envelope = Envelope().from_json(message)
        # 获取当前设置的消息类型
        self.logger.debug("[%s]接受解析后消息:%s", envelope.cid, envelope.notifications)
        if envelope.cid:
            request_handler.handle_result(envelope.cid, envelope)
        else:
            msg = json.loads(message)
            for msg_type in msg.keys():
                self._notice_handler.handle_event(msg_type, envelope)

    def connect(self):
        threading.Thread(target=self._connect).start()
        while not self.connected:
            time.sleep(1)

    def _connect(self):
        self.logger.debug("[%s]连接中...", self.ws_url)
        if not self._websocket:
            self._websocket = websocket.WebSocketApp(self.ws_url,
                                                     on_open=self.on_open,
                                                     on_message=self.on_message,
                                                     on_error=self.on_error,
                                                     header={"Authorization": f"Bearer {self._token}"},
                                                     on_close=self.on_close)
        self._websocket.run_forever(reconnect=1)

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
