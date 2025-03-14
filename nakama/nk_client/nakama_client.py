# -*- coding: utf-8 -*-

from .account import Account
from .rpc import RPC
from ..common.common import Common
from .interface import NakamaClientInter
from .session import Session
from ..nk_socket.nakama_socket import NakamaSocket


class NakamaClient(NakamaClientInter):
    def __init__(self, host: str, port: int, server_key: str, use_ssl: object = False) -> None:
        self.host = host
        self.port = port
        protocol = use_ssl and 'https' or 'http'
        self._http_uri = f'{protocol}://{self.host}:{self.port}'

        self._session = Session(self)
        self._common = Common(self._http_uri, server_key)
        self._account = Account(self._common)
        self._socket = NakamaSocket(self._common)
        self._rpc = RPC(self._common)

    async def close(self):
        await self._common.http_session.close()

    @property
    def session(self):
        return self._session

    @property
    def rpc(self):
        return self._rpc

    @property
    def account(self):
        return self._account

    @property
    def socket(self):
        return self._socket
