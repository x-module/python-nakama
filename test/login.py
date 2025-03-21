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

    create_party_result = await client.create_party(True, 20)
    print("create_party_result:", create_party_result.party_id)
    account = await client.account()
    print("account.user.id:", account.user.id)

    # await  client.close()

    await asyncio.sleep(5)
    params = {
        "partyId": create_party_result.party_id,
        "members": f"{account.user.id}",
        "region": "usest-1",
        "latencyInMs": {
            "us-west-1": 50,
            "us-east-1": 110,
            "eu-central-1": 500,
            "ap-northeast-1": 500,
        }
    }
    try:
        res = await client.rpc("swamp/matchmaker/add", **params)
        print("rpc result:", res)
    except Exception as e:
        print("request rpc error:", e)

    print("start to logout......")
    await asyncio.sleep(5)
    await  client.session_end()
    await  client.session_logout()

    await asyncio.sleep(10000000000)


if __name__ == '__main__':
    asyncio.run(main())
