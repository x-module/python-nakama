#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/5/21 14:13
# @Author Tudou <244395692@qq.com>
# @file   account.py
# @desc   account.py
import uuid
from typing import List

from example.lobby.config import ServerConfig
from example.lobby.notice import NoticeHandler
from nakama import Client, Socket
from nakama.common.nakama import AccountDevice, AccountResponse
from nakama.utils.logger import Logger
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class AccountData:
    client: Client
    socket: Socket
    account: AccountResponse


class Account:
    def __init__(self, serverConfig: ServerConfig):
        self.serverConfig = serverConfig
        self.logger = Logger(__name__)
        self.accountDataList: List[AccountData] = []

    def login(self):
        client = Client(
            host=self.serverConfig.Host,
            port=self.serverConfig.Port,
            serverKey=self.serverConfig.ServerKey,
            ssl=self.serverConfig.Ssl
        )

        # 设备登录
        result = client.authenticate.device(payload=AccountDevice(
            id=str(uuid.uuid4()),
        ))
        self.logger.debug("登录结果:%s", result.to_json())
        account = client.account.get()
        self.logger.debug("账号信息:%s", account.to_json())
        noticeHandler = NoticeHandler()
        socket = Socket(client)
        socket.setNoticeHandler(noticeHandler)
        socket.connect()
        self.logger.debug("登录成功!")
        self.accountDataList.append(AccountData(client, socket, account))

    def logout(self, accountData: AccountData):
        self.logger.debug("账号退出，playerId:%s", accountData.account.user.id)
        accountData.client.logout()
        accountData.socket.disconnect()
        self.logger.info("账号退出成功！，playerId:%s", accountData.account.user.id)
