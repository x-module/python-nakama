# -*- coding: utf-8 -*-

from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.utils.log import Logger
from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg, Envelope


class NoticeHandler:

    def __init__(self):
        self.logger = Logger(__name__)
        self._handler = None

    def set_handler(self, handler: NoticeHandlerInter):
        self._handler = handler

    async def handle_event(self, event: Envelope):
        if self._handler is not None:
            if event.channel:
                await self._handler.channel(event.channel)
            elif event.channel_join:
                await self._handler.channel_join(event.channel_join)
            elif event.channel_leave:
                await self._handler.channel_leave(event.channel_leave)
            elif event.channel_message:
                await self._handler.channel_message(event.channel_message)
            elif event.channel_message_ack:
                await self._handler.channel_message_ack(event.channel_message_ack)
            elif event.channel_message_send:
                await self._handler.channel_message_send(event.channel_message_send)
            elif event.channel_message_update:
                await self._handler.channel_message_update(event.channel_message_update)
            elif event.channel_message_remove:
                await self._handler.channel_message_remove(event.channel_message_remove)
            elif event.channel_presence_event:
                await self._handler.channel_presence_event(event.channel_presence_event)
            elif event.error:
                await self._handler.error(event.error)
            elif event.match:
                await self._handler.match(event.match)
            elif event.match_create:
                await self._handler.match_create(event.match_create)
            elif event.match_data:
                await self._handler.match_data(event.match_data)
            elif event.match_data_send:
                await self._handler.match_data_send(event.match_data_send)
            elif event.match_join:
                await self._handler.match_join(event.match_join)
            elif event.match_leave:
                await self._handler.match_leave(event.match_leave)
            elif event.match_presence_event:
                await self._handler.match_presence_event(event.match_presence_event)
            elif event.matchmaker_add:
                await self._handler.matchmaker_add(event.matchmaker_add)
            elif event.matchmaker_matched:
                await self._handler.matchmaker_matched(event.matchmaker_matched)
            elif event.matchmaker_remove:
                await self._handler.matchmaker_remove(event.matchmaker_remove)
            elif event.matchmaker_ticket:
                await self._handler.matchmaker_ticket(event.matchmaker_ticket)
            elif event.notifications:
                await self._handler.notifications(event.notifications)
            elif event.rpc:
                await self._handler.rpc(event.rpc)
            elif event.status:
                await self._handler.status(event.status)
            elif event.status_follow:
                await self._handler.status_follow(event.status_follow)
            elif event.status_presence_event:
                await self._handler.status_presence_event(event.status_presence_event)
            elif event.status_unfollow:
                await self._handler.status_unfollow(event.status_unfollow)
            elif event.status_update:
                await self._handler.status_update(event.status_update)
            elif event.stream_data:
                await self._handler.stream_data(event.stream_data)
            elif event.stream_presence_event:
                await self._handler.stream_presence_event(event.stream_presence_event)
            elif event.ping:
                await self._handler.ping(event.ping)
            elif event.pong:
                await self._handler.pong(event.pong)
            elif event.party:
                await self._handler.party(event.party)
            elif event.party_create:
                await self._handler.party_create(event.party_create)
            elif event.party_join:
                await self._handler.party_join(event.party_join)
            elif event.party_leave:
                await self._handler.party_leave(event.party_leave)
            elif event.party_promote:
                await self._handler.party_promote(event.party_promote)
            elif event.party_leader:
                await self._handler.party_leader(event.party_leader)
            elif event.party_accept:
                await self._handler.party_accept(event.party_accept)
            elif event.party_remove:
                await self._handler.party_remove(event.party_remove)
            elif event.party_close:
                await self._handler.party_close(event.party_close)
            elif event.party_join_request_list:
                await self._handler.party_join_request_list(event.party_join_request_list)
            elif event.party_join_request:
                await self._handler.party_join_request(event.party_join_request)
            elif event.party_matchmaker_add:
                await self._handler.party_matchmaker_add(event.party_matchmaker_add)
            elif event.party_matchmaker_remove:
                await self._handler.party_matchmaker_remove(event.party_matchmaker_remove)
            elif event.party_matchmaker_ticket:
                await self._handler.party_matchmaker_ticket(event.party_matchmaker_ticket)
            elif event.party_data:
                await self._handler.party_data(event.party_data)
            elif event.party_data_send:
                await self._handler.party_data_send(event.party_data_send)
            elif event.party_presence_event:
                await self._handler.party_presence_event(event.party_presence_event)
            else:
                self.logger.warning("Unknown notice event event:%s", event)
        else:
            self.logger.debug("receive notice:%s", event)


# 基础消息handler
class BaseNoticeHandler(NoticeHandlerInter):

    async def channel(self, msg: ChannelMsg):
        pass

    async def channel_join(self, msg: ChannelJoinMsg):
        pass

    async def channel_leave(self, msg: ChannelLeaveMsg):
        pass

    async def channel_message(self, msg: ChannelMessage):
        pass

    async def channel_message_ack(self, msg: ChannelMessageAckMsg):
        pass

    async def channel_message_send(self, msg: ChannelMessageSendMsg):
        pass

    async def channel_message_update(self, msg: ChannelMessageUpdateMsg):
        pass

    async def channel_message_remove(self, msg: ChannelMessageRemoveMsg):
        pass

    async def channel_presence_event(self, msg: ChannelPresenceEventMsg):
        pass

    async def error(self, msg: ErrorMsg):
        pass

    async def match(self, msg: MatchMsg):
        pass

    async def match_create(self, msg: MatchCreateMsg):
        pass

    async def match_data(self, msg: MatchDataMsg):
        pass

    async def match_data_send(self, msg: MatchDataSendMsg):
        pass

    async def match_join(self, msg: MatchJoinMsg):
        pass

    async def match_leave(self, msg: MatchLeaveMsg):
        pass

    async def match_presence_event(self, msg: MatchPresenceEventMsg):
        pass

    async def matchmaker_add(self, msg: MatchmakerAddMsg):
        pass

    async def matchmaker_matched(self, msg: MatchmakerMatchedMsg):
        pass

    async def matchmaker_remove(self, msg: MatchmakerRemoveMsg):
        pass

    async def matchmaker_ticket(self, msg: MatchmakerTicketMsg):
        pass

    async def notifications(self, msg: NotificationsMsg):
        pass

    async def rpc(self, msg: RpcMsg):
        pass

    async def status(self, msg: StatusMsg):
        pass

    async def status_follow(self, msg: StatusFollowMsg):
        pass

    async def status_presence_event(self, msg: StatusPresenceEventMsg):
        pass

    async def status_unfollow(self, msg: StatusUnfollowMsg):
        pass

    async def status_update(self, msg: StatusUpdateMsg):
        pass

    async def stream_data(self, msg: StreamDataMsg):
        pass

    async def stream_presence_event(self, msg: StreamPresenceEventMsg):
        pass

    async def ping(self, msg: PingMsg):
        pass

    async def pong(self, msg: PongMsg):
        pass

    async def party(self, msg: PartyMsg):
        pass

    async def party_create(self, msg: PartyCreateMsg):
        pass

    async def party_join(self, msg: PartyJoinMsg):
        pass

    async def party_leave(self, msg: PartyLeaveMsg):
        pass

    async def party_promote(self, msg: PartyPromoteMsg):
        pass

    async def party_leader(self, msg: PartyLeaderMsg):
        pass

    async def party_accept(self, msg: PartyAcceptMsg):
        pass

    async def party_remove(self, msg: PartyRemoveMsg):
        pass

    async def party_close(self, msg: PartyCloseMsg):
        pass

    async def party_join_request_list(self, msg: PartyJoinRequestsMsg):
        pass

    async def party_join_request(self, msg: PartyJoinRequestMsg):
        pass

    async def party_matchmaker_add(self, msg: PartyMatchmakerAddMsg):
        pass

    async def party_matchmaker_remove(self, msg: PartyMatchmakerRemoveMsg):
        pass

    async def party_matchmaker_ticket(self, msg: PartyMatchmakerTicketMsg):
        pass

    async def party_data(self, msg: PartyDataMsg):
        pass

    async def party_data_send(self, msg: PartyDataSendMsg):
        pass

    async def party_presence_event(self, msg: PartyPresenceEventMsg):
        pass
