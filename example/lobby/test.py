#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/5/21 14:30
# @Author Tudou <244395692@qq.com>
# @file   test.py
# @desc   test.py
import multiprocessing

from example.lobby.account import Account
from example.lobby.config import ServerConfig, Config


def worker():
    serverConfig = Config["187"]
    account = Account(serverConfig)
    account.login()
    print(account.accountDataList)

if __name__ == '__main__':
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=worker)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()  # 等待所有进程完成
    print("done")
    print("done")
    print("done")
    print("done")
    print("done")
    print("done")
