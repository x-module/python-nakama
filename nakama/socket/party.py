# -*- coding: utf-8 -*-
from nakama.common.nakama import Envelope, PartyCreateMsg, PartyMsg
from nakama.socket.handler import RequestWaiter, requestHandler


class Party:
    def __init__(self, socket):
        self._socket = socket

    async def create(self, open: bool, maxSize: int) -> PartyMsg:
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
        await self._socket.send(params.to_json())
        envelope = requestWaiter.result()
        if envelope.error.code:
            raise Exception(envelope.error)
        return envelope.party
