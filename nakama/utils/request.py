#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/9/22 14:21
# @Author Tudou <244395692@qq.com>
# @file   request.py
# @desc   request.py
import base64
import json

from PyQt5.QtCore import QUrl, QByteArray

#  发起网络请求
from typing import Callable, Optional, Iterable, Any, Union
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QSslError

from nakama.utils.logger import Logger


class Network(QNetworkAccessManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = Logger(__name__)
        self.reply: Optional[QNetworkReply] = None
        self._onReadyRead: Optional[Callable[[QNetworkReply], None]] = None
        self._onFinished: Optional[Callable[[QNetworkReply], None]] = None
        self._errorOccurred: Optional[Callable[[QNetworkReply.NetworkError], None]] = None
        self._sslErrors: Optional[Callable[[Iterable[QSslError]], None]] = None

        self.request: QNetworkRequest = QNetworkRequest()

        self.onReadyRead()

    def getRequest(self, url: str) -> None:
        """发起 GET 请求"""
        request = QNetworkRequest(QUrl(url))
        self.reply = self.get(request)
        self.reply.readyRead.connect(self.onReadyRead)
        self.reply.finished.connect(self.onFinished)
        self.reply.errorOccurred.connect(self.errorOccurred)
        self.reply.sslErrors.connect(self.sslErrors)

    def setHeader(self, header: QNetworkRequest.KnownHeaders, value: Any):
        self.request.setHeader(header, value)

    def setRawHeader(self, headerName: Union[QByteArray, bytes, bytearray], value: Union[QByteArray, bytes, bytearray]):
        self.request.setRawHeader(headerName, value)

    def postRequest(self, url, data):
        """发起JSON格式的POST请求"""
        # 1. 准备请求
        self.request.setUrl(QUrl(url))
        # 2. 设置JSON头部
        self.request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        # 3. 将Python字典转为JSON字符串再编码为QByteArray
        jsonData = QByteArray(data.to_json().encode('utf-8'))
        # 4. 发起POST请求
        self.reply = self.post(self.request, jsonData)
        self.reply.readyRead.connect(self.onReadyRead)
        self.reply.finished.connect(self.onFinished)
        self.reply.errorOccurred.connect(self.errorOccurred)
        self.reply.sslErrors.connect(self.sslErrors)

    def onReadyRead(self) -> None:
        """当有数据可读时触发"""
        if self._onReadyRead and self.reply:
            self._onReadyRead(self.reply)  # 回调参数：QNetworkReply 对象

    def onFinished(self) -> None:
        self.logger.debug("当请求完成时触发")
        if self.reply:
            if self._onFinished:
                self._onFinished(self.reply)  # 回调参数：QNetworkReply 对象
            self.reply.deleteLater()
            self.reply = None

    def errorOccurred(self, error: QNetworkReply.NetworkError) -> None:
        """当发生网络错误时触发"""
        self.logger.error("当发生网络错误时触发,err:{}".format(error))
        if self._errorOccurred:
            self._errorOccurred(error)  # 回调参数：QNetworkReply.NetworkError 枚举值

    def sslErrors(self, errors: Iterable[QSslError]) -> None:
        """当发生 SSL 错误时触发"""
        self.logger.error("当发生 SSL 错误时触发,err:{}".format(errors))
        if self._sslErrors:
            self._sslErrors(errors)  # 回调参数：QSslError 列表

    # --- 设置回调的方法 ---
    def setOnReadyRead(self, callback: Callable[[QNetworkReply], None]) -> None:
        """设置数据可读时的回调"""
        self._onReadyRead = callback

    def setOnFinished(self, callback: Callable[[QNetworkReply], None]) -> None:
        """设置请求完成时的回调"""
        self._onFinished = callback

    def setErrorOccurred(self, callback: Callable[[QNetworkReply.NetworkError], None]) -> None:
        """设置网络错误时的回调"""
        self._errorOccurred = callback

    def setSslErrors(self, callback: Callable[[Iterable[QSslError]], None]) -> None:
        """设置 SSL 错误时的回调"""
        self._sslErrors = callback
