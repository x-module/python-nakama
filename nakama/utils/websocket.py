#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/9/22 16:45
# @Author Tudou <244395692@qq.com>
# @file   websocket.py
# @desc   websocket.py
import json
import time
from typing import Dict, Any

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt5.QtWebSockets import QWebSocket


# 使用PyQt5内置的QWebSocket的客户端[1,4](@ref)
class WebSocketClient(QObject):
    messageReceived: pyqtSignal = pyqtSignal(str)
    connectionChanged: pyqtSignal = pyqtSignal(bool, str)  # 连接状态信号: (是否连接, 状态信息)


    def __init__(self, url):
        super().__init__()
        self.url = url
        self.websocket = None
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_timer = QTimer()
        self.reconnect_timer.timeout.connect(self._tryReconnect)
        self.heartbeat_timer = QTimer()
        self.heartbeat_timer.timeout.connect(self._sendHeartbeat)
        self.last_pong_received = time.time()
        self.pong_timeout = 15  # 心跳响应超时时间(秒)

    def connect(self):
        """连接到WebSocket服务器"""
        if self.websocket:
            self.websocket.deleteLater()

        self.websocket = QWebSocket()
        self.websocket.connected.connect(self._onConnected)
        self.websocket.disconnected.connect(self._onDisconnected)
        self.websocket.textMessageReceived.connect(self._onTextMessageReceived)
        self.websocket.pong.connect(self._onPongReceived)
        self.websocket.error.connect(lambda error: self.connectionChanged.emit(False, f"连接错误: {self.websocket.errorString()}"))
        self.websocket.open(QUrl(self.url))

    def _onConnected(self):
        """连接成功建立时的槽函数"""
        self.connected = True
        self.reconnect_attempts = 0
        self.reconnect_timer.stop()
        self.connectionChanged.emit(True, f"已连接到 {self.url}")

        # 启动心跳检测
        self.heartbeat_timer.start(10000)  # 每10秒发送一次心跳
        self.last_pong_received = time.time()

    def _onDisconnected(self):
        """连接断开时的槽函数"""
        self.connected = False
        self.heartbeat_timer.stop()
        self.connectionChanged.emit(False, "连接已断开")

        # 安排重连
        self._scheduleReconnect()

    def _onTextMessageReceived(self, message):
        """收到文本消息时的槽函数"""
        try:
            self.messageReceived.emit(message)
        except json.JSONDecodeError:
            print(f"收到非JSON消息: {message}")

    def _onPongReceived(self, elapsed_time, payload):
        """收到pong响应时的槽函数[1](@ref)"""
        self.last_pong_received = time.time()

    def _sendHeartbeat(self):
        """发送心跳包[1](@ref)"""
        if self.connected:
            current_time = time.time()
            # 检查上次收到pong是否超时
            if current_time - self.last_pong_received > self.pong_timeout:
                self.connectionChanged.emit(False, "心跳超时，连接可能已断开")
                self.websocket.abort()  # 中止连接，触发disconnected信号
            else:
                self.websocket.ping(b"ping")

    def _scheduleReconnect(self):
        """安排重连尝试"""
        if self.reconnect_attempts < self.max_reconnect_attempts:
            delay = min(2 ** self.reconnect_attempts, 10)  # 指数退避，最大30秒
            self.connectionChanged.emit(False, f"{delay}秒后尝试第{self.reconnect_attempts + 1}次重连...")
            self.reconnect_timer.start(delay * 1000)  # 转换为毫秒
        else:
            self.connectionChanged.emit(False, "重连尝试次数超限，请手动重连")

    def _tryReconnect(self):
        """尝试重新连接"""
        self.reconnect_timer.stop()
        self.reconnect_attempts += 1
        self.connect()

    def sendMessage(self, message: Dict[str, Any]):
        """发送消息到服务器"""
        if self.connected:
            try:
                json_message = json.dumps(message)
                self.websocket.sendTextMessage(json_message)
            except Exception as e:
                self.connectionChanged.emit(False, f"发送消息失败: {str(e)}")
        else:
            self.connectionChanged.emit(False, "未连接，无法发送消息")

    def close(self):
        """关闭连接"""
        self.reconnect_timer.stop()
        self.heartbeat_timer.stop()
        if self.websocket:
            self.websocket.close()
            self.websocket.deleteLater()
            self.websocket = None




from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkRequest
from PyQt5.QtWebSockets import QWebSocket

# 创建 WebSocket 连接
websocket = QWebSocket()

# 构造请求对象
url = QUrl("ws://example.com/ws")  # 或 wss://
request = QNetworkRequest(url)

# 设置 Authorization 头部
token = "your_access_token"
request.setRawHeader(b"Authorization", f"Bearer {token}".encode("utf-8"))

# 可选：设置其他头部
request.setRawHeader(b"X-Custom-Header", b"value")

# 发起连接
websocket.open(request)
