# -*- coding: utf-8 -*-


import asyncio
import json
import random
import time
from dataclasses import dataclass

from notice import NoticeHandler
from nakama import Client
from nakama.common.nakama import AccountDevice, AccountResponse, MatchLeaveMsg
from nakama.socket.socket import Socket
import uuid

from nakama.utils.logger import Logger


@dataclass
class LoginData:
    client: Client
    socket: Socket
    account: AccountResponse
    sleep: int


class TeamManager:
    def __init__(self):
        self._memberList: dict[str, list[LoginData]] = {}

    def addMember(self, leader: str, member: LoginData):
        if leader not in self._memberList:
            self._memberList[leader] = []
        self._memberList[leader].append(member)

    def getMemberList(self, leader: str):
        if leader in self._memberList:
            return self._memberList[leader]
        else:
            return []


class BatchPartyMatch(TeamManager):
    def __init__(self, playerCount: int, hasMember: bool) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.playerList: list[LoginData] = []
        self.hasMember: bool = hasMember
        self.playerCount = playerCount
        self.logoutPlayer: dict[str, int] = {}

    async def login(self) -> LoginData:
        client = Client(
            host="192.168.1.55",
            port=7350,
            serverKey="defaultkey",
            ssl=False
        )
        await client.authenticate.custom(payload=AccountDevice(
            id=str(uuid.uuid1()),
        ))
        account = client.account.get()
        self.logger.debug("账号信息:%s", account.to_json())
        socket = Socket(client)
        noticeHandler = NoticeHandler()
        socket.setNoticeHandler(noticeHandler)
        await socket.connect()
        noticeHandler.setSocket(socket)
        noticeHandler.setAccount(account)
        return LoginData(client, socket, account, random.randint(120, 150))
        # return LoginData(client, socket, account, random.randint(10, 20))

    async def logout(self, loginData: LoginData):
        self.logger.debug("账号退出，player:%s", loginData.account.user.id)
        self.logoutPlayer[loginData.account.user.id] = 1
        await loginData.socket.close()

    async def playerHeartbeat(self, loginData: LoginData, matchId: str):
        self.logger.debug("---start  player heartbeat---")
        while loginData.account.user.id not in self.logoutPlayer:
            matchData = {
                "id": 1111,
                "data": "playerHeartbeat",
            }
            self.logger.warning("playerHeartbeat")
            await loginData.socket.match.matchDataSend(matchId, 502, json.dumps(matchData), False)
            await asyncio.sleep(5)

    async def ReservedLocation(self, loginData: LoginData) -> str:
        self.logger.debug("---开始预约房间---")
        try:
            res = await loginData.socket.rpc("join/lobby", {
                "playerId": loginData.account.user.id,
                "region": "us-east-1",
            })
            matchId = res["data"]["matchId"]
            self.logger.debug("请求预约房间成功，matchId:%s", matchId)
            return matchId
        except Exception as e:
            print(e)
            await asyncio.sleep(1)
            return await self.ReservedLocation(loginData)

    # async def joinMatch1(self, loginData: LoginData)->str:
    #     self.logger.debug("---start joinMatch---")
    #     try:
    #         res = await loginData.socket.rpc("join/lobby", {
    #             "playerId": loginData.account.user.id,
    #             "region": "us-east-1",
    #         })
    #         matchId = res["data"]["matchId"]
    #         self.logger.debug("请求房间成功，matchId:%s", matchId)
    #         matchJoinResult = await loginData.socket.match.join(matchId)
    #         self.logger.info("开始玩家心跳，matchId:%s", matchId)
    #         asyncio.create_task(self.playerHeartbeat(loginData, matchId))
    #         # memberCount = random.randint(0, 2)  # 生成 0、1 或 2
    #         # for i in range(memberCount):
    #         #     asyncio.create_task(memberLogin(matchId))
    #         return matchJoinResult.match_id
    #     except Exception as e:
    #         print(e)
    #         await asyncio.sleep(2)
    #         return await self.joinMatch1(loginData)

    async def leaveMatch(self, loginData: LoginData, matchId: str) -> MatchLeaveMsg:
        self.logger.debug("退出房间 matchId:%s playerId:%s", matchId, loginData.account.user.id)
        return await loginData.socket.match.leave(matchId)

    async def relogin(self, loginData=None):
        self.logger.debug("---relogin---")
        if not loginData:
            loginData = await self.login()
        if loginData.account.user.id in self.logoutPlayer:
            del self.logoutPlayer[loginData.account.user.id]

        memCount = random.randint(0, 2)
        for j in range(memCount):
            memLoginData = await self.login()
            self.addMember(loginData.account.user.id, memLoginData)

        matchId = await self.ReservedLocation(loginData)
        # # leader 加入房间
        await loginData.socket.match.join(matchId)
        self.logger.info("开始玩家心跳，matchId:%s", matchId)
        asyncio.create_task(self.playerHeartbeat(loginData, matchId))

        memberList = self.getMemberList(loginData.account.user.id)
        for member in memberList:
            await member.socket.match.join(matchId)
            self.logger.info("开始玩家心跳，matchId:%s", matchId)
            asyncio.create_task(self.playerHeartbeat(member, matchId))

        await asyncio.sleep(loginData.sleep)
        await self.leaveMatch(loginData, matchId)

        for member in memberList:
            await self.logout(member)

        await asyncio.sleep(3)
        await self.relogin()

    async def batchLogin(self):
        for i in range(self.playerCount):
            asyncio.create_task(self.relogin())

        await asyncio.sleep(10000)

    async def batchLogin1(self):
        for i in range(self.playerCount):
            loginData = await self.login()
            memCount = random.randint(0, 2)
            # memCount = 2
            for j in range(memCount):
                memLoginData = await self.login()
                self.addMember(loginData.account.user.id, memLoginData)
            self.playerList.append(loginData)

        while True:
            if len(self.playerList) < self.playerCount:
                time.sleep(1)
            else:
                break
        for loginData in self.playerList:
            matchId = await self.ReservedLocation(loginData)
            # # leader 加入房间
            await loginData.socket.match.join(matchId)
            self.logger.info("开始玩家心跳，matchId:%s", matchId)
            asyncio.create_task(self.playerHeartbeat(loginData, matchId))
            # # 成员加入房间
            memberList = self.getMemberList(loginData.account.user.id)
            for member in memberList:
                await member.socket.match.join(matchId)
                self.logger.info("开始玩家心跳，matchId:%s", matchId)
                asyncio.create_task(self.playerHeartbeat(member, matchId))
                await asyncio.sleep(loginData.sleep)
                await self.leaveMatch(member, matchId)
            await asyncio.sleep(loginData.sleep)
            await self.leaveMatch(loginData, matchId)

        await asyncio.sleep(10000)


if __name__ == "__main__":
    batchPartyMatch = BatchPartyMatch(1, False)
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(batchPartyMatch.batchLogin())
    loop.run_until_complete(batchPartyMatch.batchLogin())
    # time.sleep(1000000)
