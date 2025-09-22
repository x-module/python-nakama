#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/9/22 15:19
# @Author Tudou <244395692@qq.com>
# @file   authenticate.py
# @desc   authenticate.py

import base64
from typing import Optional, Callable
from urllib.parse import urlencode

from PyQt5.QtNetwork import QNetworkReply
from retry import retry
from nakama.common.nakama import SessionResponse, Envelope, AccountCustom, AccountDevice, AccountEmail, AccountSteam
from nakama.inter.client_inter import ClientInter
from nakama.utils.logger import Logger
from nakama.utils.request import Network


class Authenticate:
    def __init__(self, client: ClientInter) -> None:
        self._client = client
        self.logger = Logger(__name__)
        self._network: Network = Network()
        self._network.setOnFinished(self.onLoginFinished)
        self._onLoginError: Optional[Callable[[str], None]] = None

        self.init()

    def init(self):
        value = f"Basic {base64.b64encode(self._client.config().serverKey.encode()).decode()}"
        self._network.setRawHeader(b"Authorization", bytes(value, "utf-8"))

    def _getParams(self, create: bool = True, username: str = None) -> str:
        params = {}
        if create is not None:
            params["create"] = create and 'true' or 'false'
        if username is not None:
            params["username"] = username
        return urlencode(params)

    @retry(tries=3, delay=1, backoff=2)
    def email(self, payload: AccountEmail, create: bool = True, username: str = None):
        endpoint = "/v2/account/authenticate/email"
        params = self._getParams(create=create, username=username)
        url = "{}{}?{}".format(self._client.baseUrl(), endpoint, params)
        self._network.postRequest(url, payload)

    def onLoginFinished(self, reply: QNetworkReply):
        # 处理响应
        if reply.error():
            self.logger.error("login error:{}".format(reply.errorString()))
            if self._onLoginError is not None:
                self._onLoginError(reply.errorString())
        else:
            result = reply.readAll().data().decode()  # 获取返回数据
            self.logger.debug("login success,data:{}".format(result))
            envelope = Envelope().from_json(result)
            if envelope.error.code != 0:
                raise envelope.error
            self._client.session = SessionResponse().from_json(result)
        reply.deleteLater()  # 销毁回复对象
