# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import asyncio
import time

from nakama import NakamaClient

async def main():
    client = NakamaClient('192.168.1.187', 7350, 'defaultkey')
    result = await client.account.authenticate.custom("1278888882341234", create=True, username="admin", vars={"aaa": '222'})
    print(result)
    # asyncio.create_task(client.socket.connect())
    client.socket.connect(lambda :print("connected"))
    account = await client.account.get()
    print(account)
    result = await client.rpc("get/goods")
    print(result)

    # 继续执行其他逻辑
    print("WebSocket task started, continuing with other logic...")
    # await  client.close()
    await asyncio.sleep(10000000000)

if __name__ == '__main__':
    asyncio.run(main())

