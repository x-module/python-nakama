# -*- coding: utf-8 -*-
import websockets
import asyncio
import json
from typing import Optional, Callable, Any, Dict
from websockets.exceptions import ConnectionClosed

from nakama.client.client import Client
from nakama.common.nakama import Envelope
from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.socket.notice_handler import NoticeHandler, DISCONNECT_TYPE
from nakama.socket.party import Party
from nakama.socket.request_handler import RequestHandler
from nakama.socket.rpc import Rpc
from nakama.utils.log import Logger


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
                print("尝试连接服务器...")
                self._websocket = await websockets.connect(
                    self.ws_url,
                    additional_headers={"Authorization": f"Bearer {self._token}"},
                    ping_interval=self.ping_interval  # 自动发送Ping
                )
                print("连接成功！")
                await self.listen()  # 开始监听消息

            except (ConnectionClosed, ConnectionError) as e:
                print(f"连接断开: {e}, {self.retry_interval}秒后重连...")
                await asyncio.sleep(self.retry_interval)
            except Exception as e:
                print(f"未知错误: {e}")
                await asyncio.sleep(self.retry_interval)

    async def listen(self):
        """监听消息并处理心跳超时"""
        try:
            async for message in self._websocket:
                envelope = Envelope().from_json(message)
                print("---------source------", message)
                print("---------cid------", envelope.to_json())

                self.logger.debug("Received message:%s", envelope)
                if envelope.cid:
                    self._request_handler.handle_result(envelope.cid, envelope)
                else:
                    for msg_type in json.loads(envelope.to_json()):
                        await self._notice_handler.handle_event(msg_type, envelope)

        except websockets.exceptions.ConnectionClosed as e:

            print(f"服务器主动关闭连接: {e}")
            await self._notice_handler.handle_event(DISCONNECT_TYPE, None)
            raise  # 触发重连
        except asyncio.TimeoutError:
            print("心跳超时，连接可能已静默断开")
            await self._notice_handler.handle_event(DISCONNECT_TYPE, None)
            raise  # 触发重连
        except Exception as e:
            print(f"接收消息错误: {e}")
            await self._notice_handler.handle_event(DISCONNECT_TYPE, None)
            await asyncio.sleep(1)

    async def disconnect(self) -> None:
        """断开连接"""
        if self._websocket:
            await self._websocket.close()
            self._websocket = None
