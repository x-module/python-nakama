# -*- coding: utf-8 -*-
from nakama.common.nakama import Envelope, PartyCreateMsg, PartyMsg
from nakama.socket.handler import RequestWaiter, requestHandler


class Party:
    def __init__(self, socket):
        self._socket = socket

    def create(self, open: bool, max_size: int) -> PartyMsg:
        request_waiter = RequestWaiter()
        cid = '%d' % requestHandler.getCid()
        requestHandler.addRequest(cid, request_waiter)
        params = Envelope(
            party_create=PartyCreateMsg(
                open=open,
                max_size=max_size,
            ),
            cid=str(cid),
        )
        self._socket.websocket.send(params.to_json())
        envelope = request_waiter.result()
        if envelope.error.code:
            raise Exception(envelope.error)
        return envelope.party
