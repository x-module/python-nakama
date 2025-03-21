# -*- coding: utf-8 -*-
import asyncio
import base64
import json

from nakama import NakamaClient
from nakama.common.nakama import Envelope, RpcMsg
from test.notice_handdler import NoticeHandler


# from nakama.common.nakama import NotificationsMsg, RpcMsg, Envelope


def msg_handler(msg):
    print("out client Received message:", msg)


async def main():
    client = NakamaClient('http://192.168.1.55:7350', 'defaultkey')

    notice_handler = NoticeHandler()
    client.set_notice_handler(notice_handler)

    # 邮箱登录
    result = await client.authenticate_email(email="aaa@aaa.com", password="ssssssss", create=True, vars={"aaa": '222'})
    print(result.token)
    # asyncio.create_task(client.socket.connect())
    await client.session_start()
    print("======================session connected=======================")

    account = await client.account()
    print("account.user.id:", account.user.id)
    # await  client.close()
    params = {
        "playerId": account.user.id
    }
    result = await client.rpc("check/reconnect/info", **params)
    print("rpc result:", result)

    await asyncio.sleep(10000000000)


if __name__ == '__main__':
    asyncio.run(main())
