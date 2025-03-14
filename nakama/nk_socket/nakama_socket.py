# -*- coding: utf-8 -*-
import asyncio
import time

import aiohttp

from ..common.common import Common


class NakamaSocket:
    def __init__(self, common: Common):
        self.ws_listener_task = None
        self.websocket = None
        self._common = common

    async def _websocket_listener(self, ws):
        async for msg in self.websocket:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print("Received message:", msg.data)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                print("WebSocket closed")
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("WebSocket error:", self.websocket.exception())
                break

    def connect(self):
        asyncio.create_task(self.connect_websocket())

    async def connect_websocket(self):
        """
        连接 WebSocket 并启动心跳和消息处理任务
        """
        url = self._common.http_url + ('/ws?token=%s' % self._common.token)
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as websocket:
                print("WebSocket connected")
                # 启动心跳任务
                heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))
                # 启动消息处理任务
                message_task = asyncio.create_task(self.handle_messages(websocket))
                try:
                    # 等待任意一个任务完成
                    done, pending = await asyncio.wait(
                        {heartbeat_task, message_task},
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    # 取消未完成的任务
                    for task in pending:
                        task.cancel()
                        try:
                            await task  # 等待任务取消
                        except asyncio.CancelledError:
                            print(f"Task {task.get_name()} cancelled")
                except Exception as e:
                    print(f"WebSocket connection failed: {e}")
                finally:
                    print("WebSocket connection closed")

    async def send_heartbeat(self, websocket, interval: int = 10):
        """
        发送 WebSocket 心跳的协程
        :param websocket: WebSocket 连接对象
        :param interval: 心跳间隔时间（秒）
        """
        while True:
            try:
                print("Sending heartbeat...")
                await websocket.ping()  # 发送心跳消息
                await asyncio.sleep(interval)  # 等待指定间隔
            except Exception as e:
                print(f"Heartbeat failed: {e}")
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
                    print(f"Received message: {msg.data}")
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    print("WebSocket closed")
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print("WebSocket error")
                    break
            except Exception as e:
                print(f"Message handling failed: {e}")
                break  # 如果发生错误，退出循环
