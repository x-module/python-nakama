# -*- coding: utf-8 -*-
import base64
from abc import ABC

from nakama.inter.notice_handler_inter import NoticeHandlerInter
# from nakama.interface.notice_handler_inter import NoticeHandlerInter
from nakama.utils.log import Logger

NOTIFICATIONS_TYPE = 'notifications'
MATCH_DATA_TYPE = 'match_data'
MATCH_PRESENCE_EVENT_TYPE = 'match_presence_event'
MATCHMAKER_MATCHED_TYPE = 'matchmaker_matched'
STATUS_PRESENCE_EVENT_TYPE = 'status_presence_event'
STREAM_PRESENCE_EVENT_TYPE = 'stream_presence_event'
STREAM_DATA_TYPE = 'stream_data'
CHANNEL_MESSAGE_TYPE = 'channel_message'
CHANNEL_PRESENCE_EVENT_TYPE = 'channel_presence_event'
DISCONNECT_TYPE = 'disconnect'


class NoticeHandler:

    def __init__(self):
        self.logger = Logger(__name__)
        self._handler = None

    def set_handler(self, handler:NoticeHandlerInter):
        self._handler = handler

    async def handle_event(self, msg_type, event):
        if self._handler is not None:
            if msg_type == NOTIFICATIONS_TYPE:  # notifications
                await self._handler.notification_handler(event)
            elif msg_type == MATCH_DATA_TYPE:  # match_data
                event.data = event.data.encode()
                pad = len(event.data) % 4
                event.data += b"=" * pad  # correct padding
                event.data = base64.b64decode(event.data)
                await self._handler.match_data_handler(event)
            elif msg_type == MATCH_PRESENCE_EVENT_TYPE:  # match_presence_event
                await self._handler.match_presence_handler(event)
            elif msg_type == MATCHMAKER_MATCHED_TYPE:  # matchmaker_matched
                await self._handler.matchmaker_matched_handler(event)
            elif msg_type == STATUS_PRESENCE_EVENT_TYPE:  # status_presence_event
                await self._handler.status_presence_handler(event)
            elif msg_type == STREAM_PRESENCE_EVENT_TYPE:  # stream_presence_event
                await self._handler.stream_presence_handler(event)
            elif msg_type == STREAM_DATA_TYPE:  # stream_data
                await self._handler.stream_data_handler(event)
            elif msg_type == CHANNEL_MESSAGE_TYPE:  # channel_message
                await self._handler.channel_message_handler(event)
            elif msg_type == CHANNEL_PRESENCE_EVENT_TYPE:  # channel_presence_event
                await self._handler.channel_presence_handler(event)
            elif msg_type == DISCONNECT_TYPE:  # disconnect
                await self._handler.disconnect_handler(event)
            else:
                self.logger.warning("Unknown notice event msg_type: %s,event:%s", msg_type, event)
        else:
            self.logger.debug("receive msg_type:%s notice:%s", msg_type, event)
