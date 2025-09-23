# -*- coding: utf-8 -*-
from typing import Optional, Callable

from nakama.common.nakama import Envelope, PartyCreateMsg, PartyMsg
from nakama.socket.handler import requestHandler
from nakama.utils.logger import Logger


class Party:
    def __init__(self, socket):
        self._socket = socket
        self._request = {}
        self._logger = Logger(f"{__name__}.{self.__class__.__name__}")

    def create(self, open: bool, maxSize: int, callback: Callable[[PartyMsg], None]):
        cid = '%d' % requestHandler.getCid()
        params = Envelope(
            party_create=PartyCreateMsg(
                open=open,
                max_size=maxSize,
            ),
            cid=str(cid),
        )
        self._socket.sendMessage(params.to_dict())
        self._request[cid] = callback

        requestHandler.addRequest(cid, self.createResult)

    def createResult(self, cid: int, result: Envelope):
        if cid in self._request:
            self._request[cid](result.party)
            del self._request[cid]
        else:
            self._logger.error("创建party的请求不存在，cid:%s", cid)
