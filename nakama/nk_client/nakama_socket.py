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

    async def connect_websocket(self):
        """
        连接 WebSocket 并启动心跳和消息处理任务
        """
        url = self._common.http_url + ('/ws?token=%s' % self._common.session.token)
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as websocket:
                self.logger.info("WebSocket connected")
                self.websocket = websocket
                # 启动心跳任务
                self.heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))
                # 启动消息处理任务
                self.message_task = asyncio.create_task(self.handle_messages(websocket))
                try:
                    # 等待任意一个任务完成
                    done, pending = await asyncio.wait(
                        {self.heartbeat_task, self.message_task},
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    # 取消未完成的任务
                    for task in pending:
                        task.cancel()
                        try:
                            await task  # 等待任务取消
                        except asyncio.CancelledError:
                            self.logger.error(f"Task {task.get_name()} cancelled")
                except Exception as e:
                    self.logger.error(f"WebSocket connection failed: {e}")
                finally:
                    self.logger.warning("WebSocket connection closed")

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
                msg = await websocket.receive()  # 接收消息

                if msg.type == aiohttp.WSMsgType.TEXT:
                    self.logger.debug(f"Received message: {msg.data}")
                    notice = NotificationsMsg()
                    notice.from_dict(json.loads(msg.data)["notifications"])
                    if self.message_handler:
                        self.message_handler(notice)
                    self.logger.info("received notice: {}".format(notice))
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    self.logger.debug(f"Received closed message: {msg.data}")
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self.logger.debug("WebSocket error")
                    break
                else:
                    self.logger.debug(f"Unknown message type: {msg.type}")
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
