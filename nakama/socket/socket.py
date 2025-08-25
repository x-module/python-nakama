# -*- coding: utf-8 -*-
import asyncio
import base64
import threading
import time
import json
import logging
from typing import Optional, Callable, Any, Dict

import aiohttp
from aiohttp import ClientSession, WSMsgType

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
        self._heartbeat_task = None  # 心跳检测任务
        self._reconnect_attempts = 0  # 当前重连次数
        self._max_reconnect_attempts = 5  # 最大重连次数
        self._is_manual_close = False  # 是否手动关闭

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
        """重构监听循环：依赖消息接收异常检测断开"""
        try:
            async for msg in ws:  # 连接断开时会自动抛出异常
                if msg.type == WSMsgType.TEXT:
                    envelope = Envelope().from_dict(json.loads(msg.data))
                    if envelope.cid:
                        requestHandler.handleResult(envelope.cid, envelope)
                    else:
                        for msgType in json.loads(msg.data).keys():
                            await self._noticeHandler.handleEvent(msgType, envelope)
                elif msg.type == WSMsgType.CLOSED:
                    print("----closed-----")
                    break  # 收到关闭帧
                elif msg.type == WSMsgType.ERROR:
                    raise ws.exception()  # 主动抛出错误
        except (aiohttp.ClientConnectionError, ConnectionResetError) as e:
            self.logger.error(f"WebSocket connection lost: {e}")
        finally:
            # 无论何种断开都触发重连（非手动关闭时）
            await self._handle_disconnect()

    async def _start_heartbeat(self, ws):
        """心跳检测任务（双向保活）[6,8](@ref)"""
        try:
            while not ws.closed:
                await asyncio.sleep(30)  # 心跳间隔30秒
                try:
                    await ws.ping()  # 标准Ping帧
                    self.logger.debug("Sent ping")
                    # 等待Pong响应（10秒超时）
                    await asyncio.wait_for(ws.receive(), timeout=10)
                except asyncio.TimeoutError:
                    self.logger.warning("Heartbeat timeout, triggering reconnect")
                    await self._handle_disconnect()
                    break
                except (aiohttp.ClientConnectionError, ConnectionResetError):
                    self.logger.warning("WebSocket connection lost,err: ConnectionResetError")
                    await self._handle_disconnect()
                    break
        except asyncio.CancelledError:
            pass  # 任务被正常取消

    async def _handle_disconnect(self):
        """统一处理断开事件"""
        if not self._is_manual_close:
            await self._noticeHandler.handleEvent('disconnect', None)
            await self.close()
            await self._reconnect()  # 触发自动重连

    async def _reconnect(self):
        """指数退避重连机制[1,4](@ref)"""
        if self._reconnect_attempts >= self._max_reconnect_attempts:
            self.logger.error("Max reconnect attempts exceeded")
            return

        self._reconnect_attempts += 1
        delay = min(2 ** self._reconnect_attempts, 30)  # 最大延迟30秒
        self.logger.warning(f"Reconnecting ({self._reconnect_attempts}/{self._max_reconnect_attempts}) in {delay}s")
        await asyncio.sleep(delay)
        await self.connect()

    async def connect(self):
        """支持自动重连的连接入口"""
        assert self._client.session.token is not None, 'Missing session token'
        self._is_manual_close = False
        try:
            self._websocket = await self._client.httpSession.ws_connect(
                self.wsUrl,
                heartbeat=30.0  # 启用aiohttp内置心跳
            )
            self.logger.info("WebSocket connected")
            # 启动监听和心跳任务
            loop = asyncio.get_running_loop()
            loop.create_task(self._websocket_listener(self._websocket))
            self._heartbeat_task = loop.create_task(self._start_heartbeat(self._websocket))
            self._reconnect_attempts = 0  # 重置重连计数
        except (aiohttp.ClientConnectionError, OSError) as e:
            self.logger.error(f"Connect failed: {e}")
            await self._reconnect()

    async def close(self):
        """安全关闭连接[7](@ref)"""
        self._is_manual_close = True
        # 取消心跳任务
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None
        # 关闭WebSocket
        if self._websocket and not self._websocket.closed:
            await self._websocket.close()
            self._websocket = None
        self.logger.info("WebSocket closed111")

    async def send(self, data):
        if not self._websocket or self._websocket.closed:
            self.logger.warning("Send failed: connection not ready")
            return False
        await self._websocket.send_json(data)
        return True
