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
from PyQt5.QtNetwork import QNetworkRequest
from PyQt5.QtWebSockets import QWebSocket

from nakama.utils.logger import Logger


# https://blog.csdn.net/ckg3824278/article/details/151115567

# 使用PyQt5内置的QWebSocket的客户端[1,4](@ref)
class WebSocketClient(QObject):
    messageReceived: pyqtSignal = pyqtSignal(str)
    connectionChanged: pyqtSignal = pyqtSignal(bool, str)  # 连接状态信号: (是否连接, 状态信息)

    def __init__(self, url: str = "", token: str = ""):
        super().__init__()
        self._url = url
        self._token = token
        self._connected = False
        self._websocket = None
        self._reconnectAttempts = 0
        self._maxReconnectAttempts = 10
        self._reconnectTimer = QTimer()
        self._reconnectTimer.timeout.connect(self._tryReconnect)
        self._heartbeatTimer = QTimer()
        self._heartbeatTimer.timeout.connect(self._sendHeartbeat)
        self._lastPongReceived = time.time()
        self._pongTimeout = 15  # 心跳响应超时时间(秒)
        self._logger = Logger(f"{__name__}.{self.__class__.__name__}")

    def setUrl(self, url):
        self._url = url

    def setToken(self, token):
        self._token = token

    def connect(self):
        """连接到WebSocket服务器"""
        self._logger.debug("开始Socket连接，url:%s token:%s", self._url, self._token)
        if self._websocket:
            self._websocket.deleteLater()

        self._websocket = QWebSocket()
        # self._websocket.setPingInterval(30000)  # 设置心跳间隔为30秒（单位：毫秒）

        self._websocket.connected.connect(self._onConnected)
        self._websocket.disconnected.connect(self._onDisconnected)
        self._websocket.textMessageReceived.connect(self._onTextMessageReceived)
        self._websocket.pong.connect(self._onPongReceived)
        self._websocket.error.connect(lambda error: self.connectionChanged.emit(False, f"连接错误: {self._websocket.errorString()}"))

        request = QNetworkRequest(QUrl(self._url))
        # 设置 Authorization 头部
        request.setRawHeader(b"Authorization", f"Bearer {self._token}".encode("utf-8"))
        # 发起连接
        self._websocket.open(request)

    def _onConnected(self):
        """连接成功建立时的槽函数"""
        self._logger.debug("成功建立socket连接,发送事件")
        self._connected = True
        self._reconnectAttempts = 0
        self._reconnectTimer.stop()
        self.connectionChanged.emit(True, f"已连接到 {self._url}")

        # 启动心跳检测
        self._logger.debug("启动心跳检测")
        self._heartbeatTimer.start(10000)  # 每10秒发送一次心跳
        self._lastPongReceived = time.time()

    def _onDisconnected(self):
        """连接断开时的槽函数"""
        self._logger.warning("连接断开")
        self._connected = False
        self._heartbeatTimer.stop()
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
        # self._logger.debug("收到pong响应")
        self._lastPongReceived = time.time()

    def _sendHeartbeat(self):
        """发送心跳包[1](@ref)"""
        # self._logger.debug("发送心跳包")
        if self._connected:
            current_time = time.time()
            # 检查上次收到pong是否超时
            if current_time - self._lastPongReceived > self._pongTimeout:
                self.connectionChanged.emit(False, "心跳超时，连接可能已断开")
                self._websocket.abort()  # 中止连接，触发disconnected信号
            else:
                self._websocket.ping(b"ping")

    def _scheduleReconnect(self):
        """安排重连尝试"""
        if self._reconnectAttempts < self._maxReconnectAttempts:
            delay = min(2 ** self._reconnectAttempts, 10)  # 指数退避，最大30秒
            self.connectionChanged.emit(False, f"{delay}秒后尝试第{self._reconnectAttempts + 1}次重连...")
            self._reconnectTimer.start(delay * 1000)  # 转换为毫秒
        else:
            self.connectionChanged.emit(False, "重连尝试次数超限，请手动重连")

    def _tryReconnect(self):
        """尝试重新连接"""
        self._reconnectTimer.stop()
        self._reconnectAttempts += 1
        self.connect()

    def sendMessage(self, message: Dict[str, Any]):
        """发送消息到服务器"""
        if self._connected:
            self._logger.debug("发送消息到服务器:{}".format(json.dumps(message)))
            try:
                self._websocket.sendTextMessage(json.dumps(message))
            except Exception as e:
                self.connectionChanged.emit(False, f"发送消息失败: {str(e)}")
        else:
            self.connectionChanged.emit(False, "未连接，无法发送消息")

    def close(self):
        """关闭连接"""
        self._logger.debug("关闭连接")
        self._reconnectTimer.stop()
        self._heartbeatTimer.stop()
        if self._websocket:
            self._websocket.close()
            self._websocket.deleteLater()
            self._websocket = None
