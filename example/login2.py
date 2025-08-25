# -*- coding: utf-8 -*-
import asyncio

from example.notice import NoticeHandler
from nakama import Client
from nakama.common.nakama import AccountCustom, AccountSteam, AccountDevice, AccountResponse, AccountEmail
from nakama.socket.socket import Socket
import uuid


async def login():
    client = Client(
        host="showdown-dev-02.us-east1.nakamacloud.io",
        port=443,
        serverKey="wgAPTyg14PXiWwGn",
        ssl=True
    )
    result = await client.authenticate.email(payload=AccountEmail(
        email="aaaaaaa@aaa.com",
        password="12341234123412341234"
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
    # res = await socket.rpc("join/lobby", {
    #     "playerId": account.user.id,
    #     "region": "us-east-1",
    # })
    # print("rpc result:", res["data"]["matchId"])
    #
    # print("----------------后续操作-----------------")
    # matchJoinResult = await socket.match.join(res["data"]["matchId"])
    # print("match_join_result:", matchJoinResult.match_id)

    await asyncio.sleep(100000)


async def joinMatch(socket: Socket, account: AccountResponse):
    try:
        res = await socket.rpc("join/lobby", {
            "playerId": account.user.id,
            # "region": "us-east-1",
            "region": "ap-northeast-1",
        })
        print("join matchId:", res["data"]["matchId"])
        print("----------------后续操作-----------------")
        matchJoinResult = await socket.match.join(res["data"]["matchId"])
        print("match_join_result:", matchJoinResult.match_id)
        return matchJoinResult.match_id
    except Exception as e:
        print(e)
        await asyncio.sleep(2)
        return await joinMatch(socket, account)


async def batchLogin():
    tasks = []
    for i in range(13):
        print("login %d" % i)
        task = asyncio.create_task(login())
        tasks.append(task)
    # 等待所有任务完成
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # asyncio.run(batchLogin())

    asyncio.run(  login())
