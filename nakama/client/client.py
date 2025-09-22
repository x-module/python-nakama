# -*- coding: utf-8 -*-
import base64

from PyQt5.QtNetwork import QNetworkRequest

from nakama.client.authenticate import Authenticate
from nakama.common.nakama import SessionResponse
from nakama.inter.client_inter import LoginConfig, ClientInter
from nakama.utils.logger import Logger
from nakama.utils.request import Network


class Client(ClientInter):

    def __init__(self, config: LoginConfig = LoginConfig()):
        self._session = None
        self._network: Network = Network()
        self._config = config
        self._config.serverKey = '%s:' % self._config.serverKey
        self._headers = {}
        self.logger = Logger(f"{__name__}.{self.__class__.__name__}")

        self.authenticate = Authenticate(self)  # 初始化应用

        self.initApp()

    def initApp(self):
        value = f"Basic {base64.b64encode(self._config.serverKey.encode()).decode()}"
        self._network.setRawHeader(b"Authorization", bytes(value, "utf-8"))

    def request(self) -> Network:
        return self._network

    def config(self) -> LoginConfig:
        return self._config

    def baseUrl(self) -> str:
        protocol = "https" if self._config.ssl else "http"
        return f"{protocol}://{self._config.host}:{self._config.port}"

    def getSession(self) -> SessionResponse:
        return self._session

    def setSession(self, session: SessionResponse):
        self._session = session
        self._headers = {
            'Authorization': 'Bearer %s' % session.token
        }
