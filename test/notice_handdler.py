# -*- coding: utf-8 -*-
from nakama.common.nakama import ChannelMsg, PartyPresenceEventMsg
from nakama.socket.notice_handler import BaseNoticeHandler


class NoticeHandler(BaseNoticeHandler):
    async def party_presence_event(self, msg: PartyPresenceEventMsg):
        print("----------party_presence_event:", msg)

