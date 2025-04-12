# -*- coding: utf-8 -*-

from nakama.inter.notice_handler_inter import NoticeHandlerInter
from common.Logger import Logger
from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg, Envelope


class NoticeHandler:

    def __init__(self):
        self.logger = Logger(__name__)
        self._handler = None

    def set_handler(self, handler: NoticeHandlerInter):
        self._handler = handler

    async def handle_event(self, msg_type: str, event: Envelope):
        print("====-=-=-=-" * 50)
        print(msg_type)
        print("====-=-=-=-" * 50)
        if self._handler is not None:
            if msg_type == "channel":
                await self._handler.channel(event.channel)
            elif msg_type == "notifications":
                await self._handler.notifications(event.notifications)
            elif msg_type == "rpc":
                await self._handler.rpc(event.rpc)
            elif msg_type == "status":
                await self._handler.status(event.status)
            elif msg_type == "status_follow":
                await self._handler.status_follow(event.status_follow)
            elif msg_type == "status_presence_event":
                await self._handler.status_presence_event(event.status_presence_event)
            elif msg_type == "status_unfollow":
                await self._handler.status_unfollow(event.status_unfollow)
            elif msg_type == "status_update":
                await self._handler.status_update(event.status_update)
            elif msg_type == "stream_data":
                await self._handler.stream_data(event.stream_data)
            elif msg_type == "stream_presence_event":
                await self._handler.stream_presence_event(event.stream_presence_event)
            elif msg_type == "ping":
                await self._handler.ping(event.ping)
            elif msg_type == "pong":
                await self._handler.pong(event.pong)
            elif msg_type == "party":
                await self._handler.party(event.party)
            elif msg_type == "party_create":
                await self._handler.party_create(event.party_create)
            elif msg_type == "party_join":
                await self._handler.party_join(event.party_join)
            elif msg_type == "party_leave":
                await self._handler.party_leave(event.party_leave)
            elif msg_type == "party_promote":
                await self._handler.party_promote(event.party_promote)
            elif msg_type == "party_leader":
                await self._handler.party_leader(event.party_leader)
            elif msg_type == "party_accept":
                await self._handler.party_accept(event.party_accept)
            elif msg_type == "party_remove":
                await self._handler.party_remove(event.party_remove)
            elif msg_type == "party_close":
                await self._handler.party_close(event.party_close)
            elif msg_type == "party_join_request_list":
                await self._handler.party_join_request_list(event.party_join_request_list)
            elif msg_type == "party_join_request":
                await self._handler.party_join_request(event.party_join_request)
            elif msg_type == "party_matchmaker_add":
                await self._handler.party_matchmaker_add(event.party_matchmaker_add)
            elif msg_type == "party_matchmaker_remove":
                await self._handler.party_matchmaker_remove(event.party_matchmaker_remove)
            elif msg_type == "party_matchmaker_ticket":
                await self._handler.party_matchmaker_ticket(event.party_matchmaker_ticket)
            elif msg_type == "party_data":
                await self._handler.party_data(event.party_data)
            elif msg_type == "party_data_send":
                await self._handler.party_data_send(event.party_data_send)
            elif msg_type == "party_presence_event":
                await self._handler.party_presence_event(event.party_presence_event)
            else:
                self.logger.warning("Unknown notice event event:%s", event)
        else:
            self.logger.debug("receive notice:%s", event)


# 基础消息handler
class BaseNoticeHandler(NoticeHandlerInter):
    def __init__(self):
        self.logger = Logger()

    async def channel(self, msg: ChannelMsg):
        self.logger.debug("receive channel:%s", msg)

    async def channel_join(self, msg: ChannelJoinMsg):
        self.logger.debug("receive channel_join:%s", msg)

    async def channel_leave(self, msg: ChannelLeaveMsg):
        self.logger.debug("receive channel_leave:%s", msg)

    async def channel_message(self, msg: ChannelMessage):
        self.logger.debug("receive channel_message:%s", msg)

    async def channel_message_ack(self, msg: ChannelMessageAckMsg):
        self.logger.debug("receive channel_message_ack:%s", msg)

    async def channel_message_send(self, msg: ChannelMessageSendMsg):
        self.logger.debug("receive channel_message_send:%s", msg)

    async def channel_message_update(self, msg: ChannelMessageUpdateMsg):
        self.logger.debug("receive channel_message_update:%s", msg)

    async def channel_message_remove(self, msg: ChannelMessageRemoveMsg):
        self.logger.debug("receive channel_message_remove:%s", msg)

    async def channel_presence_event(self, msg: ChannelPresenceEventMsg):
        self.logger.debug("receive channel_presence_event:%s", msg)

    async def error(self, msg: ErrorMsg):
        self.logger.debug("receive error:%s", msg)

    async def match(self, msg: MatchMsg):
        self.logger.debug("receive match:%s", msg)

    async def match_create(self, msg: MatchCreateMsg):
        self.logger.debug("receive match_create:%s", msg)

    async def match_data(self, msg: MatchDataMsg):
        self.logger.debug("receive match_data:%s", msg)

    async def match_data_send(self, msg: MatchDataSendMsg):
        self.logger.debug("receive match_data_send:%s", msg)

    async def match_join(self, msg: MatchJoinMsg):
        self.logger.debug("receive match_join:%s", msg)

    async def match_leave(self, msg: MatchLeaveMsg):
        self.logger.debug("receive match_leave:%s", msg)

    async def match_presence_event(self, msg: MatchPresenceEventMsg):
        self.logger.debug("receive match_presence_event:%s", msg)

    async def matchmaker_add(self, msg: MatchmakerAddMsg):
        self.logger.debug("receive matchmaker_add:%s", msg)

    async def matchmaker_matched(self, msg: MatchmakerMatchedMsg):
        self.logger.debug("receive matchmaker_matched:%s", msg)

    async def matchmaker_remove(self, msg: MatchmakerRemoveMsg):
        self.logger.debug("receive matchmaker_remove:%s", msg)

    async def matchmaker_ticket(self, msg: MatchmakerTicketMsg):
        self.logger.debug("receive matchmaker_ticket:%s", msg)

    async def notifications(self, msg: NotificationsMsg):
        self.logger.debug("receive notifications:%s", msg)

    async def rpc(self, msg: RpcMsg):
        self.logger.debug("receive rpc:%s", msg)

    async def status(self, msg: StatusMsg):
        self.logger.debug("receive status:%s", msg)

    async def status_follow(self, msg: StatusFollowMsg):
        self.logger.debug("receive status_follow:%s", msg)

    async def status_presence_event(self, msg: StatusPresenceEventMsg):
        self.logger.debug("receive status_presence_event:%s", msg)

    async def status_unfollow(self, msg: StatusUnfollowMsg):
        self.logger.debug("receive status_unfollow:%s", msg)

    async def status_update(self, msg: StatusUpdateMsg):
        self.logger.debug("receive status_update:%s", msg)

    async def stream_data(self, msg: StreamDataMsg):
        self.logger.debug("receive stream_data:%s", msg)

    async def stream_presence_event(self, msg: StreamPresenceEventMsg):
        self.logger.debug("receive stream_presence_event:%s", msg)

    async def ping(self, msg: PingMsg):
        self.logger.debug("receive ping:%s", msg)

    async def pong(self, msg: PongMsg):
        self.logger.debug("receive pong:%s", msg)

    async def party(self, msg: PartyMsg):
        self.logger.debug("receive party:%s", msg)

    async def party_create(self, msg: PartyCreateMsg):
        self.logger.debug("receive party_create:%s", msg)

    async def party_join(self, msg: PartyJoinMsg):
        self.logger.debug("receive party_join:%s", msg)

    async def party_leave(self, msg: PartyLeaveMsg):
        self.logger.debug("receive party_leave:%s", msg)

    async def party_promote(self, msg: PartyPromoteMsg):
        self.logger.debug("receive party_promote:%s", msg)

    async def party_leader(self, msg: PartyLeaderMsg):
        self.logger.debug("receive party_leader:%s", msg)

    async def party_accept(self, msg: PartyAcceptMsg):
        self.logger.debug("receive party_accept:%s", msg)

    async def party_remove(self, msg: PartyRemoveMsg):
        self.logger.debug("receive party_remove:%s", msg)

    async def party_close(self, msg: PartyCloseMsg):
        self.logger.debug("receive party_close:%s", msg)

    async def party_join_request_list(self, msg: PartyJoinRequestsMsg):
        self.logger.debug("receive party_join_request_list:%s", msg)

    async def party_join_request(self, msg: PartyJoinRequestMsg):
        self.logger.debug("receive party_join_request:%s", msg)

    async def party_matchmaker_add(self, msg: PartyMatchmakerAddMsg):
        self.logger.debug("receive party_matchmaker_add:%s", msg)

    async def party_matchmaker_remove(self, msg: PartyMatchmakerRemoveMsg):
        self.logger.debug("receive party_matchmaker_remove:%s", msg)

    async def party_matchmaker_ticket(self, msg: PartyMatchmakerTicketMsg):
        self.logger.debug("receive party_matchmaker_ticket:%s", msg)

    async def party_data(self, msg: PartyDataMsg):
        self.logger.debug("receive party_data:%s", msg)

    async def party_data_send(self, msg: PartyDataSendMsg):
        self.logger.debug("receive party_data_send:%s", msg)

    async def party_presence_event(self, msg: PartyPresenceEventMsg):
        self.logger.debug("receive party_presence_event:%s", msg)
