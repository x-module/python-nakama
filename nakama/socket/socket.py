# -*- coding: utf-8 -*-
import asyncio
import base64
import threading
import time

import json
from typing import Optional, Callable, Any, Dict

import aiohttp

from nakama.client.client import Client
from nakama.common.nakama import Envelope, NotificationsMsg, Notification
from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.socket.match import Match
from nakama.socket.notice import NoticeHandler
from nakama.socket.party import Party
from nakama.socket.handler import requestHandler
from nakama.socket.rpc import Rpc

from nakama.utils.logger import Logger


class Socket:
    def __init__(self, client: Client):
        self.ws_listener_task = None
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
        return f"{protocol}://{self._host}:{self._port}/ws?token={self._client.session.token}&format=json"

    def setNoticeHandler(self, handler: NoticeHandlerInter):
        self._noticeHandler.setHandler(handler)

    async def _websocket_listener(self, ws):
        while True:
            if ws.closed:
                await self._noticeHandler.handleEvent('disconnect', None)
                await self.close()
                break
            message = await ws.receive_json()
            # print("socket message:", message)
            if message:
                envelope = Envelope().from_dict(message)
                # 获取当前设置的消息类型
                if envelope.cid:
                    requestHandler.handleResult(envelope.cid, envelope)
                else:
                    for msgType in message.keys():
                        await self._noticeHandler.handleEvent(msgType, envelope)

    async def connect(self, loop=None):
        assert self._client.session.token is not None, 'You must set session.token'
        if loop is None:
            loop = asyncio.get_running_loop()
        self._websocket = await self._client.httpSession.ws_connect(self.wsUrl)
        if self._websocket.closed:
            print("WebSocket is closed!")  # 检查 WebSocket 是否已关闭
        self.ws_listener_task = loop.create_task(self._websocket_listener(self._websocket))

    async def close(self):
        assert self._websocket is not None, 'You must connect() before close'
        self.ws_listener_task.cancel()
        self.ws_listener_task = None
        await self._websocket.close()
        self._websocket = None

    async def send(self, data):
        assert self._websocket is not None, 'You must connect() before sending'
        # await self._websocket.send_str(data)
        await self._websocket.send_json(data)
