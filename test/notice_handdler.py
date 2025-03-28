# -*- coding: utf-8 -*-
from nakama.common.nakama import Envelope
from nakama.inter.notice_handler_inter import NoticeHandlerInter


class NoticeHandler(NoticeHandlerInter):
    async def notification_handler(self, event: Envelope):
        print("notification_handler:", event.notifications)

    async def match_data_handler(self, event: Envelope):
        pass

    async def match_presence_handler(self, event: Envelope):
        pass

    async def matchmaker_matched_handler(self, event: Envelope):
        pass

    async def status_presence_handler(self, event: Envelope):
        pass

    async def stream_presence_handler(self, event: Envelope):
        pass

    async def stream_data_handler(self, event: Envelope):
        pass

    async def channel_message_handler(self, event: Envelope):
        pass

    async def channel_presence_handler(self, event: Envelope):
        pass

    async def disconnect_handler(self, event: Envelope):
        print("disconnect_handler:", event)
