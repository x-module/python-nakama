#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/5/21 14:16
# @Author Tudou <244395692@qq.com>
# @file   config.py
# @desc   config.py

from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ServerConfig:
    Host: str
    Port: int
    ServerKey: str
    Ssl: bool


Config: dict[str:ServerConfig] = {
    "187": ServerConfig(
        Host="192.168.1.187",
        Port=7350,
        ServerKey="defaultkey",
        Ssl=False,
    )
}
