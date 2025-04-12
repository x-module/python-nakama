# -*- coding: utf-8 -*-
import websockets
import asyncio
import json
from typing import Optional, Callable, Any, Dict
from websockets.exceptions import ConnectionClosed

from nakama.client.client import Client
from nakama.common.nakama import Envelope, NotificationsMsg, Notification
from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.socket.notice_handler import NoticeHandler
from nakama.socket.party import Party
from nakama.socket.request_handler import RequestHandler
from nakama.socket.rpc import Rpc
from common.Logger import Logger


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

        self.logger = Logger()

        self._notice_handler = NoticeHandler()
        self._request_handler = RequestHandler()

    @property
    def websocket(self) -> str:
        return self._websocket

    @property
    def ws_url(self) -> str:
        protocol = "wss" if self._ssl else "ws"
        return f"{protocol}://{self._host}:{self._port}/ws"

    def set_notice_handler(self, handler: NoticeHandlerInter):
        self._notice_handler.set_handler(handler)

    async def connect(self):
        asyncio.create_task(self._connect())
        while not self._websocket:
            await asyncio.sleep(0.1)

    async def _connect(self):
        while True:
            try:
                self.logger.debug("尝试连接服务器...")
                self._websocket = await websockets.connect(
                    self.ws_url,
                    additional_headers={"Authorization": f"Bearer {self._token}"},
                    ping_interval=self.ping_interval  # 自动发送Ping
                )
                self.logger.info("连接成功")
                await self.listen()  # 开始监听消息

            except (ConnectionClosed, ConnectionError) as e:
                self.logger.warning(f"连接断开: {e}, {self.retry_interval}秒后重连...")
                await asyncio.sleep(self.retry_interval)
            except Exception as e:
                self.logger.warning(f"未知错误: {e}")
                await asyncio.sleep(self.retry_interval)

    async def listen(self):
        """监听消息并处理心跳超时"""
        notices = [
            Notification(
                id="000000000",
                subject="system notice",
                content="disconnect",
                code=00000,
            )
        ]
        try:
            async for message in self._websocket:
                self.logger.debug("]received source message:%s", message)
                envelope = Envelope().from_json(message)
                # 获取当前设置的消息类型

                self.logger.debug("[%s]received message:%s", envelope.cid, envelope.notifications)
                if envelope.cid:
                    self._request_handler.handle_result(envelope.cid, envelope)
                else:
                    msg = json.loads(message)

                    for msg_type in msg.keys():
                        print(f"-------msg_type--------:{msg_type}")
                        await self._notice_handler.handle_event(msg_type, envelope)

        except websockets.exceptions.ConnectionClosed as e:
            self.logger.warning(f"服务器主动关闭连接: {e}")
            await self._notice_handler.handle_event(Envelope(
                notifications=NotificationsMsg(
                    notifications=notices
                )
            ))
        except asyncio.TimeoutError:
            self.logger.warning("心跳超时，连接可能已静默断开")
            await self._notice_handler.handle_event(Envelope(
                notifications=NotificationsMsg(
                    notifications=notices
                )
            ))
        except Exception as e:
            self.logger.warning(f"接收消息错误: {e}")
            await self._notice_handler.handle_event(Envelope(
                notifications=NotificationsMsg(
                    notifications=notices
                )
            ))

    async def disconnect(self) -> None:
        """断开连接"""
        if self._websocket:
            await self._websocket.close()
            self._websocket = None
