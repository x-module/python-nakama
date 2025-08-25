# -*- coding: utf-8 -*-
import asyncio
import json

from nakama import Socket
from nakama.common.nakama import MatchMsg, ErrorMsg, AccountResponse, MatchDataMsg
from nakama.socket.notice import BaseNoticeHandler
from nakama.utils.logger import Logger


class NoticeHandler(BaseNoticeHandler):
    dsHealthReport: dict[str, int] = {}
    def __init__(self, ):
        super(NoticeHandler, self).__init__()
        self.logger = Logger(__name__)
        self.socket = None
        self.account = None
        self.startDsHeatBeat = False

    def setSocket(self, socket: Socket):
        self.socket = socket

    def setAccount(self, account: AccountResponse):
        self.account = account

    async def error(self, msg: ErrorMsg):
        self.logger.debug("receive error:%s", msg)

    async def match(self, msg: MatchMsg):
        self.logger.debug("receive match:%s", msg)

    async def matchData(self, msg: MatchDataMsg):
        # self.logger.debug("receive match_data:%s  data:%s", msg, msg.data.decode())
        msgData = json.loads(msg.data.decode())
        if msg.op_code == 1001 and msgData["data"]["Address"] != "" and not self.startDsHeatBeat:
            self.startDsHeatBeat = True
            self.logger.debug("---start create player session")
            matchData = {
                "id": 123,
                "data": "data",
            }
            await self.socket.match.matchDataSend(msg.match_id, 501, json.dumps(matchData), False)
            if msg.match_id not in self.dsHealthReport:
                self.dsHealthReport[msg.match_id] = 1
                asyncio.create_task(self.dsHeartbeat(msg.match_id))

        # if msg.op_code == 1001 and msgData["Address"] != "":

    async def dsHeartbeat(self, matchId: str):
        print("---start ds heartbeat ------")
        while True:
            self.logger.warning("dsHeartbeat")
            await self.socket.rpc("report/ds/health", {
                "matchId": matchId,
            })
            await asyncio.sleep(5)
