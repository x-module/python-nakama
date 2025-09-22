# -*- coding: utf-8 -*-
from typing import Optional, Callable, Dict

from nakama.utils.logger import Logger
from nakama.utils.websocket import WebSocketClient


class Socket:
    def __init__(self, client: Client):
        self._host = client.host
        self._port = client.port
        self._token = client.session.token
        self._ssl = client.ssl
        self._client = client
        self._websocket = None
        self._callbacks: Dict[str, Callable] = {}
        self.onError: Optional[Callable] = None

        self.logger = Logger(__name__)


    def init_websocket(self):
        """初始化WebSocket客户端"""
        self.websocketClient = WebSocketClient("ws://localhost:8080/ws")
        self.websocketClient.messageReceived.connect(self.on_message_received)
        self.websocketClient.connectionChanged.connect(self.on_connection_changed)
