# -*- coding: utf-8 -*-

from .account import Account
from .rpc import RPC
from ..common.common import Common
from .interface import NakamaClientInter
from .session import Session
from nakama.nk_client.nakama_socket import NakamaSocket


class NakamaClient(NakamaClientInter):
    def __init__(self, server: str, server_key: str, port=None) -> None:
        if port is not None:
            self._http_uri = f'{server}:{port}'
        else:
            self._http_uri = server

        self._common = Common(self._http_uri, server_key)

        self._session = Session(self._common)
        self._account = Account(self._common)
        self._socket = NakamaSocket(self._common)
        self._rpc = RPC(self._common)

    def set_message_handler(self, message_handler):
        self._socket.set_message_handler(message_handler)

    async def logout(self):
        await self._socket.close()
        await self._session.logout()
        await self._common.http_session.close()

    def token(self):
        return self._common.session.token

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
