# -*- coding: utf-8 -*-
import asyncio
import json
import time

import aiohttp

from nakama.common.common import Common
from nakama.common.nakama import NotificationsMsg
from nakama.utils.log import Logger


class NakamaSocket:
    def __init__(self, common: Common):
        self.message_task = None
        self.heartbeat_task = None
        self.ws_listener_task = None
        self.websocket = None
        self._common = common
        self.logger = Logger("NakamaSocket")
        self.message_handler = None

    def set_message_handler(self, message_handler):
        self.message_handler = message_handler

    def connect(self):
        return asyncio.create_task(self.connect_websocket())

    async def send(self, data):
        # while self.websocket is None:
        #     await asyncio.sleep(0.1)
        assert self.websocket is not None, 'You must connect() before sending'
        await self.websocket.send_str(data)
        # await self.websocket.send_bytes(data)

    async def connect_websocket(self):
        """
        连接 WebSocket 并启动心跳和消息处理任务
        """
        url = self._common.http_url + ('/ws?token=%s' % self._common.session.token)
        self.websocket = await self._common.http_session.ws_connect(url)
        self.logger.debug("WebSocket connected")
        loop = asyncio.get_running_loop()
        # 启动心跳任务
        self.heartbeat_task = loop.create_task(self.send_heartbeat(self.websocket))
        # 启动消息处理任务
        self.message_task = loop.create_task(self.handle_messages(self.websocket))

    async def send_heartbeat(self, websocket, interval: int = 30):
        """
        发送 WebSocket 心跳的协程
        :param websocket: WebSocket 连接对象
        :param interval: 心跳间隔时间（秒）
        """
        while True:
            try:
                self.logger.debug("Sending heartbeat...")
                await websocket.ping()  # 发送心跳消息
                await asyncio.sleep(interval)  # 等待指定间隔
            except Exception as e:
                self.logger.error(f"Heartbeat failed: {e}")
                break  # 如果发生错误，退出循环

    async def handle_messages(self, websocket):
        """
        处理 WebSocket 消息的协程
        :param websocket: WebSocket 连接对象
        """
        while True:
            try:
                msg = await websocket.receive_json()  # 接收消息
                print("Received message:", msg)
                if msg.get('cid') is not None:
                    print("-----msg have cid:", msg.get('cid'))
                    # cid = msg.pop('cid')
                    # self.request_handler.handle_result(cid, msg)
                else:
                    for type, event in msg.items():
                        print("-------msg have not cid,type:", type, " event:", event)
                        # await self.handlers.handle_event(type, event)

            except Exception as e:
                self.logger.error("Failed to receive message: {}".format(e))
                break  # 如果发生错误，退出循环

    async def close(self):
        assert self.websocket is not None, 'You must connect() before close'
        self.heartbeat_task.cancel()
        self.heartbeat_task = None
        self.message_task.cancel()
        self.message_task = None
        await self.websocket.close()
        self.websocket = None
