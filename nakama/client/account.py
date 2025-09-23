#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/9/23 13:00
# @Author Tudou <244395692@qq.com>
# @file   account.py
# @desc   account.py
import base64
from typing import Callable

from PyQt5.QtNetwork import QNetworkReply
from retry import retry

from nakama.common.nakama import AccountResponse, Envelope, PartyMsg
from nakama.utils.logger import Logger
from nakama.utils.request import Network


class Account:
    def __init__(self, client):
        self._client = client
        self._logger = Logger(f"{__name__}.{self.__class__.__name__}")
        self._network: Network = Network()
        self._network.setOnFinished(self.onGetAccountFinished)
        self._callback: Callable[[AccountResponse], None] = None
        self._onError: Callable[[str], None] = None

    @retry(tries=3, delay=1, backoff=2)
    def get(self, callback: Callable[[str], None], onError: Callable[[str], None]):
        value = f"Bearer {self._client.getSession().token}"
        self._network.setRawHeader(b"Authorization", bytes(value, "utf-8"))
        self._callback = callback
        self._onError = onError
        endpoint = '/v2/account'
        url = "{}{}?".format(self._client.baseUrl(), endpoint)
        self._network.getRequest(url)

    def onGetAccountFinished(self, reply: QNetworkReply):
        # 处理响应
        if reply.error():
            self._logger.error("get account data  error:{}".format(reply.errorString()))
            if self._onError is not None:
                self._onError(reply.errorString())
        else:
            result = reply.readAll().data().decode()  # 获取返回数据
            if result:
                self._logger.debug("get account data success,data:{}".format(result))
                envelope = Envelope().from_json(result)
                if envelope.error.code != 0:
                    raise envelope.error
                if self._callback is not None:
                    self._callback(AccountResponse().from_json(result))
            else:
                self._logger.debug("get account data failed,data empty:{}".format(result))
        reply.deleteLater()  # 销毁回复对象
