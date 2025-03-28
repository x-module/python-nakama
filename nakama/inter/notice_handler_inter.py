# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from nakama.common.nakama import Envelope


class NoticeHandlerInter(ABC):

    @abstractmethod
    async def notification_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def match_data_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def match_presence_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def matchmaker_matched_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def status_presence_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def stream_presence_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def stream_data_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def channel_message_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def channel_presence_handler(self, event: Envelope):
        pass

    @abstractmethod
    async def disconnect_handler(self, event: Envelope):
        pass
