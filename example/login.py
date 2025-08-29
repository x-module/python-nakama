# -*- coding: utf-8 -*-
import time

from example.notice import NoticeHandler
from nakama import Client
from nakama.common.nakama import AccountCustom, AccountSteam, AccountDevice
from nakama.socket.socket import Socket
from nakama.utils.error import handle_errors


# Host = "192.168.1.190",
# Port = 7350,
# ServerKey = "defaultkey",
# HttpKey = "defaulthttpkey",
# Ssl = False,

@handle_errors
def main():
    client = Client(
        host="192.168.1.55",
        port=7350,
        serverKey="defaultkey",
        ssl=False
        # host="showdown-dev-02.us-east1.nakamacloud.io",
        # port=443,
        # serverKey="wgAPTyg14PXiWwGn",
        # ssl=True
    )
    # result =  client.authenticate.email(email="aaaa@ssss.com",password="aaaa@ssss.com")
    # result = client.authenticate.steam(AccountSteam(
    #     token="2341234123e412w0we34",
    #     vars={
    #         "aaaa": "bbbb"
    #     }
    # ))
    result = client.authenticate.device(payload=AccountDevice(
        id="25739443885670978"
    ))

    print("登录结果:", result.to_json())
    account = client.account.get()
    print("账号信息:", account.to_json())

    noticeHandler = NoticeHandler()
    socket = Socket(client)
    socket.setNoticeHandler(noticeHandler)
    socket.connect()

    print("----------------后续操作-----------------")

    # matchJoinResult = socket.match.join("c3b63857-4c21-4435-97f8-47b44b8e308f.nakama")
    # print("match_join_result:", matchJoinResult.match_id)

    # create_party_result = socket.party.create(True, 20)
    # print("create_party_result:", create_party_result.party_id)
    # #
    #
    # result = socket.rpc("warfare/get/status", {})
    # print("result:", result)

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
    time.sleep(100000)


if __name__ == '__main__':
    main()
