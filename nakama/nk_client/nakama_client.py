# -*- coding: utf-8 -*-

from .account import Account
from .rpc import RPC
from ..common.common import Common
from .interface import NakamaClientInter
from .session import Session
from ..nk_socket.nakama_socket import NakamaSocket


class NakamaClient(NakamaClientInter):
    def __init__(self, host: str, server_key: str,port=None) -> None:
        self.host = host
        self.port = port
        if port is not None:
            self._http_uri = f'{self.host}:{self.port}'
        else:
            self._http_uri =self.host
        self._common = Common(self._http_uri, server_key)
        self._session = Session(self._common)
        self._account = Account(self._common)
        self._socket = NakamaSocket(self._common)
        self._rpc = RPC(self._common)

    async def logout(self):
        await self._socket.close()
        await self._session.logout()
        await self._common.http_session.close()

    @property
    def session(self):
        return self._session

    @property
    def rpc(self):
        return self._rpc

    @property
    def http_url(self):
        return self._http_uri

    @property
    def account(self):
        return self._account

    @property
    def socket(self):
        return self._socket
