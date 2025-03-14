# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class NakamaClientInter(ABC):

    @abstractmethod
    async def close(self):
        pass
