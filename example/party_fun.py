# -*- coding: utf-8 -*-
import asyncio
import json
import random
import time

from example.notice import NoticeHandler
from nakama import Client
from nakama.common.nakama import AccountDevice, AccountResponse
from nakama.socket.socket import Socket
import uuid


async def login():
    client = Client(
        host="192.168.1.55",
        port=7350,
        serverKey="defaultkey",
        ssl=False
    )
    result = await client.authenticate.custom(payload=AccountDevice(
        id=str(uuid.uuid1()),
    ))
    print("登录结果:", result.to_json())
    account = client.account.get()
    print("账号信息:", account.to_json())

    noticeHandler = NoticeHandler()
    socket = Socket(client)
    socket.setNoticeHandler(noticeHandler)
    await socket.connect()
    noticeHandler.setSocket(socket)
    noticeHandler.setAccount(account)
    print("=========== start join lobby ==============")
    await joinMatch(socket, account)
    await asyncio.sleep(100000)



async def memberLogin(matchId: str):
    client = Client(
        host="192.168.1.55",
        port=7350,
        serverKey="defaultkey",
        ssl=False
    )
    result = await client.authenticate.custom(payload=AccountDevice(
        id=str(uuid.uuid1()),
    ))
    print("登录结果:", result.to_json())
    account = client.account.get()
    print("账号信息:", account.to_json())

    noticeHandler = NoticeHandler()
    socket = Socket(client)
    socket.setNoticeHandler(noticeHandler)
    await socket.connect()
    noticeHandler.setSocket(socket)
    noticeHandler.setAccount(account)
    print("=========== start join lobby ==============")
    matchJoinResult = await socket.match.join(matchId)
    print("match_join_result:", matchJoinResult.match_id)
    asyncio.create_task(playerHeartbeat(socket, matchId))
    await asyncio.sleep(100000)


async def playerHeartbeat(socket: Socket, matchId: str):
    print("---start  player heartbeat---")
    while True:
        matchData = {
            "id": 12223,
            "data": "data",
        }
        print("---player heartbeat data---", matchData)
        await socket.match.matchDataSend(matchId, 502, json.dumps(matchData), False)
        await asyncio.sleep(5)


async def joinMatch(socket: Socket, account: AccountResponse):
    try:
        res = await socket.rpc("join/lobby", {
            "playerId": account.user.id,
            "region": "us-east-1",
        })
        matchId = res["data"]["matchId"]
        print("join matchId:", matchId)
        print("----------------后续操作-----------------")
        matchJoinResult = await socket.match.join(matchId)
        print("match_join_result:", matchJoinResult.match_id)
        asyncio.create_task(playerHeartbeat(socket, matchId))

        # memberCount = random.randint(0, 2)  # 生成 0、1 或 2
        # for i in range(memberCount):
        #     asyncio.create_task(memberLogin(matchId))

        return matchJoinResult.match_id
    except Exception as e:
        print(e)
        await asyncio.sleep(2)
        return await joinMatch(socket, account)


async def batchLogin():
    tasks = []
    for i in range(10):
        print("login %d" % i)
        task = asyncio.create_task(login())
        tasks.append(task)
    # 等待所有任务完成
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(batchLogin())
    time.sleep(10000000)
