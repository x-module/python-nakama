# -*- coding: utf-8 -*-
from nakama.common.nakama import Envelope, PartyCreateMsg, PartyMsg
from nakama.socket.handler import RequestWaiter, requestHandler


class Party:
    def __init__(self, socket):
        self._socket = socket

    def create(self, open: bool = True, maxSize: int = 10):
        requestWaiter = RequestWaiter()
        cid = '%d' % requestHandler.getCid()
        requestHandler.addRequest(cid, requestWaiter)
        params = Envelope(
            party_create=PartyCreateMsg(
                open=open,
                max_size=maxSize,
            ),
            cid=str(cid),
        )
        self._socket.sendMessage(params.to_dict())
