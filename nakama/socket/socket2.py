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
import websocket

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

    def onPong(self, ws, message):
        self.logger.debug("接收到Pong消息:%s", message)
        self._noticeHandler.handleEvent("pong", Envelope())

    async def _websocket_listener(self, websocket):
        print("websocket listener")

    async def _websocket_listener1(self, ws):
        while True:
            # if ws.closed:
            #     await self.handlers.handle_event('disconnect', None)
            #     await self.close()
            #     break

            print("---------接受消息--------------")
            msg = await ws.receive_json()
            print(msg)
            print("---------接受消息--------------")


            # msg = await ws.receive_json()
            # print(msg)
            # print(msg)
            # print(msg)
            # print(msg)
            # # if msg.get('cid') is not None:
            #     cid = msg.pop('cid')
            #     self.request_handler.handle_result(cid, msg)
            # else:
            #     for type, event in msg.items():
            #         await self.handlers.handle_event(type, event)

    async def connect(self, loop=None):
        assert self._client.session.token is not None, 'You must set session.token'
        if loop is None:
            loop = asyncio.get_running_loop()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            # "Authorization": f"Basic {self._client.session.token}"
        }
        httpSession = aiohttp.ClientSession(headers=headers)
        self._websocket = await httpSession.ws_connect(self.wsUrl)
        print("-------logindoen----------")
        print("-------logindoen----------")
        print("-------logindoen----------")
        print("-------logindoen----------",self._websocket)
        if self.websocket.closed:
            print("WebSocket is closed!")  # 检查 WebSocket 是否已关闭
        self.ws_listener_task = loop.create_task(self.test111())
        print("Task was cancelled!",self.ws_listener_task.cancelled())  # 检查任务是否被取消
        print("-----------end--------------")
        print("-----------end--------------")
        print("-----------end--------------")
    async def test111(self):
        print("test")
    async def close(self):
        assert self.websocket is not None, 'You must connect() before close'
        self.ws_listener_task.cancel()
        self.ws_listener_task = None
        await self.websocket.close()
        self.websocket = None

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
