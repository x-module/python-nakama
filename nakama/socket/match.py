# -*- coding: utf-8 -*-
import base64
import json

from nakama.common.nakama import Envelope, PartyMsg, MatchJoinMsg, MatchMsg, MatchDataSendMsg, UserPresenceMsg, RpcMsg, MatchLeaveMsg
from nakama.socket.handler import  requestHandler, WSRequestWaiter
from nakama.utils.logger import Logger


class Match:
    def __init__(self, socket):
        self._socket = socket
        self.logger = Logger(__name__)

    async def join(self, matchId: str) -> MatchMsg:
        requestWaiter = WSRequestWaiter()
        cid = '%d' % requestHandler.getCid()
        requestHandler.addRequest(cid, requestWaiter)
        params = Envelope(
            match_join=MatchJoinMsg(
                match_id=matchId,
            ),
            cid=str(cid),
        )
        await self._socket.send(params.to_dict())
        envelope = await requestWaiter
        if envelope.error.code:
            raise Exception(envelope.error)
        return envelope.match

    async def matchDataSend(self, matchId: str, opCode: int, data: str, reliable: bool, presences: list[UserPresenceMsg] = []):
        # 响应走的是match通知，不会有相应
        params = Envelope(
            match_data_send=MatchDataSendMsg(
                match_id=matchId,
                op_code=opCode,
                data=data.encode(),
                reliable=reliable,
                presences=presences,
            )
        )
        # self.logger.debug("matchDataSend info:{}".format(params.match_data_send))
        await self._socket.send(params.to_dict())

    async def leave(self, matchId: str) -> MatchLeaveMsg:
        requestWaiter = WSRequestWaiter()
        cid = '%d' % requestHandler.getCid()
        requestHandler.addRequest(cid, requestWaiter)
        params = Envelope(
            match_leave=MatchLeaveMsg(
                match_id=matchId,
            ),
            cid=str(cid),
        )
        await self._socket.send(params.to_dict())
        envelope = await requestWaiter
        if envelope.error.code:
            raise Exception(envelope.error)
        return envelope.match_leave
