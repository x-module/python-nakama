# -*- coding: utf-8 -*-
import asyncio
import base64
import json

from nakama import Client
from nakama.common.nakama import AccountCustom
from nakama.socket.socket import Socket
from test.notice_handdler import NoticeHandler


async def main():
    client = Client(
        host="showdown-dev-02.us-east1.nakamacloud.io",
        port=443,
        server_key="wgAPTyg14PXiWwGn",
        ssl=True
    )
    # result =  client.authenticate.email(email="aaaa@ssss.com",password="aaaa@ssss.com")
    result =  client.authenticate.custom(AccountCustom(
        id="234123412341234",
        vars={
            "aaaa":"bbbb"
        }
    ))
    # result =  client.authenticate.device(id="asdfw4r1231fw3333",create=True)
    print("登录结果:",result.to_json())

    account = client.account.get()
    print("账号信息:",account.to_json())

    notice_handler = NoticeHandler()
    socket = Socket(client)
    socket.set_notice_handler(notice_handler)
    await socket.connect()

    print("----------------后续操作-----------------")
    create_party_result = await socket.party.create(True, 20)
    print("create_party_result:", create_party_result.party_id)
    #
    # params = {
    #     "partyId": create_party_result.party_id,
    #     "members": f"{account.user.id}",
    #     "region": "usest-1",
    #     "latencyInMs": {
    #         "us-west-1": 50,
    #         "us-east-1": 110,
    #         "eu-central-1": 500,
    #         "ap-northeast-1": 500,
    #     }
    # }
    # create_match_result= await socket.rpc.call("swamp/matchmaker/add", params)
    # print("create_match_result:", create_match_result)
    await asyncio.sleep(100000)


if __name__ == '__main__':
    asyncio.run(main())
