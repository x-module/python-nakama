# -*- coding: utf-8 -*-
import asyncio

from nakama import NakamaClient
from nakama.common.nakama import NotificationsMsg


def msg_handler(msg: NotificationsMsg):
    print("out client Received message:", msg)


async def main():
    client = NakamaClient('http://192.168.1.190:7350', 'defaultkey')
    # 邮箱登录
    result = await client.authenticate_email(email="aaa@aaa.com", password="ssssssss", create=True, vars={"aaa": '222'})
    print(result.token)
    client.set_message_handler(msg_handler)
    # asyncio.create_task(client.socket.connect())

    client.session_start()

    account = await client.account()
    print("account.user.id:", account.user.id)
    # 继续执行其他逻辑
    print("WebSocket task started, continuing with other logic...")
    # await  client.close()
    await asyncio.sleep(10000000000)


if __name__ == '__main__':
    asyncio.run(main())
