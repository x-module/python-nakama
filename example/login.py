# -*- coding: utf-8 -*-
import asyncio

from example.notice import NoticeHandler
from nakama import Client
from nakama.common.nakama import AccountCustom, AccountSteam, AccountDevice, AccountResponse
from nakama.socket.socket import Socket
import uuid


async def login():
    client = Client(
        host="192.168.1.187",
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

    await asyncio.sleep(100000)




if __name__ == '__main__':
    asyncio.run(login())
