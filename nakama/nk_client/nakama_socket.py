# -*- coding: utf-8 -*-
import asyncio

from nakama.common.common import Common
from nakama.nk_client.notice_handler import NoticeHandler, DISCONNECT_TYPE
from nakama.nk_client.request_handler import RequestHandler
from nakama.utils.log import Logger

class NakamaSocket:

    def __init__(self, common: Common):
        self.message_task = None
        self.heartbeat_task = None
        self.ws_listener_task = None
        self.websocket = None
        self._common = common
        self._common._socket = self
        self.logger = Logger("NakamaSocket")
        self._notice_handler = NoticeHandler()
        self._request_handler = RequestHandler()


    @property
    def notice_handler(self):
        return self._notice_handler

    def connect(self):
        return asyncio.create_task(self.connect_websocket())

    async def send(self, data):
        assert self.websocket is not None, 'You must connect() before sending'
        await self.websocket.send_str(data)

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
            print("-------------------hand message----------------")
            try:
                if websocket.closed:
                    await self._notice_handler.handle_event(DISCONNECT_TYPE, None)
                    await self.close()
                    break

                msg = await websocket.receive_json()  # 接收消息
                self.logger.debug("Received message:%s", msg)
                if msg.get('cid') is not None:
                    self._request_handler.handle_result(msg.pop('cid'), msg)
                else:
                    for type, event in msg.items():
                        await self._notice_handler.handle_event(type, event)

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
