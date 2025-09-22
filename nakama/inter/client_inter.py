# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from nakama.utils.request import Network


@dataclass_json
@dataclass
class LoginConfig:
    host: str = "192.168.1.190"
    port: int = 7350
    serverKey: str = "defaultkey"
    ssl: bool = False


class ClientInter(ABC):
    """Nakama 客户端的抽象接口类，定义了与 Nakama 服务器交互的方法"""

    @abstractmethod
    def request(self) -> Network:
        pass

    @abstractmethod
    def config(self) -> LoginConfig:
        pass

    @abstractmethod
    def baseUrl(self)->str:
        pass
