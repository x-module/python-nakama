# -*- coding: utf-8 -*-
from nakama.common.nakama import Envelope, PartyMsg, MatchJoinMsg, MatchMsg
from nakama.socket.handler import RequestWaiter, requestHandler


class Match:
    def __init__(self, socket):
        self._socket = socket

    def join(self, matchId: str) -> MatchMsg:
        requestWaiter = RequestWaiter()
        cid = '%d' % requestHandler.getCid()
        requestHandler.addRequest(cid, requestWaiter)
        params = Envelope(
            match_join=MatchJoinMsg(
                match_id=matchId,
            ),
            cid=str(cid),
        )
        self._socket.websocket.send(params.to_json())
        envelope = requestWaiter.result()
        if envelope.error.code:
            raise Exception(envelope.error)
        return envelope.match

