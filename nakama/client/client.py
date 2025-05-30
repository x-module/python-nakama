# -*- coding: utf-8 -*-
import base64
from typing import Optional, Any

import requests

from nakama.client.account import Account
from nakama.client.authenticate import Authenticate
from nakama.client.leaderboard import Leaderboard
from nakama.client.rpc import Rpc
from nakama.client.storage import Storage
from nakama.common.nakama import SessionResponse
from nakama.client.link import Link
from nakama.client.unlink import Unlink
from nakama.utils.logger import Logger


class Client(object):
    def __init__(
            self,
            host: str = "192.168.1.190",
            port: int = 7350,
            serverKey: str = "defaultkey",
            ssl: bool = False
    ):
        self._host = host
        self._port = port
        self._serverKey = '%s:' % serverKey
        self._ssl = ssl
        self._headers = {}

        self.logger = Logger(__name__)

        self._session: SessionResponse = SessionResponse()

        self.authenticate = Authenticate(self)  # 初始化应用
        self.link = Link(self)
        self.unlink = Unlink(self)
        self.account = Account(self)
        self.leaderboard = Leaderboard(self)
        self.storage = Storage(self)
        self.rpc = Rpc(self)

        self.initApp()

    def initApp(self):
        self._headers = {"Authorization": f"Basic {base64.b64encode(self._serverKey.encode()).decode()}"}

    def request(self, method: str, endpoint: str, params: Optional[dict] = None, payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=payload,
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()

    @property
    def session(self) -> SessionResponse:
        return self._session

    @session.setter
    def session(self, session: SessionResponse):
        self._session = session
        self._headers = {
            'Authorization': 'Bearer %s' % session.token
        }
    def logout(self):
        self.authenticate.logout()

    @property
    def base_url(self):
        protocol = "https" if self.ssl else "http"
        return f"{protocol}://{self._host}:{self._port}"

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def ssl(self):
        return self._ssl
