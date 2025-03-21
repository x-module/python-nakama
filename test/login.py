# -*- coding: utf-8 -*-
import asyncio
import base64
import json

from nakama import NakamaClient
import realtime_pb2
from nakama.common.nakama import Envelope, RpcMsg


# from nakama.common.nakama import NotificationsMsg, RpcMsg, Envelope


def msg_handler(msg):
    print("out client Received message:", msg)


params = {
    "playerId": "7e13e7c3-eb29-44bf-b5ab-f460187ca1df"
}
#
# msg_data = {
#     'cid': 4,
#     "id": "get/image/activity/config",
#     "playload": data,
# }
# json_str = json.dumps(msg_data)
# bytes_data = json_str.encode("utf-8")
#
# json_str = json.dumps(msg_data)
# bytes_data = json_str.encode("utf-8")
#
# base64_data = base64.b64encode(bytes_data)


# data = RpcMsg()
# data.id="get/image/activity/config"
# data.payload=json.dumps(params)
# print(data.to_json())


async def main():
    client = NakamaClient('http://192.168.1.55:7350', 'defaultkey')
    # 邮箱登录
    result = await client.authenticate_email(email="aaa@aaa.com", password="ssssssss", create=True, vars={"aaa": '222'})
    print(result.token)
    client.set_message_handler(msg_handler)
    # asyncio.create_task(client.socket.connect())
    await client.session_start()
    print("======================session connected=======================")

    # await client.connect_websocket()
    uri = "check/reconnect/info"
    data = {
        "playerId": "e355554d-c915-4b12-a245-2b31a44e2bd5"
    }
    json_str = json.dumps(data)
    params = Envelope(
        rpc=RpcMsg(
            id=uri,
            payload=json_str,
        ),
        cid="123",
    )
    print("params.SerializeToString():",params.to_json())

    print("start to send socket message")
    await client.send(params.to_json())

    account = await client.account()
    print("account.user.id:", account.user.id)
    # 继续执行其他逻辑
    print("WebSocket task started, continuing with other logic...")
    # await  client.close()
    params = {
        "playerId": "7e13e7c3-eb29-44bf-b5ab-f460187ca1df"
    }
    result = await client.rpc("is/streamer", **params)
    print("rpc result:", result)

    await asyncio.sleep(10000000000)


if __name__ == '__main__':
    asyncio.run(main())
