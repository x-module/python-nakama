# -*- coding: utf-8 -*-
from nakama.common.nakama import ChannelMsg, PartyPresenceEventMsg, PartyDataSendMsg, PartyDataMsg, \
    PartyMatchmakerTicketMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerAddMsg, PartyJoinRequestMsg, \
    PartyJoinRequestsMsg, PartyCloseMsg, PartyRemoveMsg, PartyAcceptMsg, PartyLeaderMsg, PartyPromoteMsg, PartyLeaveMsg, \
    PartyJoinMsg, PartyCreateMsg, PartyMsg, PongMsg, PingMsg, StreamPresenceEventMsg, StreamDataMsg, StatusUpdateMsg, \
    StatusUnfollowMsg, StatusPresenceEventMsg, StatusFollowMsg, StatusMsg, RpcMsg, NotificationsMsg, \
    MatchmakerTicketMsg, MatchmakerRemoveMsg, MatchmakerMatchedMsg, MatchmakerAddMsg, MatchPresenceEventMsg, \
    MatchLeaveMsg, MatchJoinMsg, MatchDataSendMsg, MatchDataMsg, MatchCreateMsg, MatchMsg, ErrorMsg, \
    ChannelPresenceEventMsg, ChannelMessageRemoveMsg, ChannelMessageUpdateMsg, ChannelMessageSendMsg, \
    ChannelMessageAckMsg, ChannelMessage, ChannelLeaveMsg, ChannelJoinMsg
from nakama.socket.notice_handler import BaseNoticeHandler


class NoticeHandler(BaseNoticeHandler):
    async def channel(self, msg: ChannelMsg):
        return await super().channel(msg)

    async def channel_join(self, msg: ChannelJoinMsg):
        return await super().channel_join(msg)

    async def channel_leave(self, msg: ChannelLeaveMsg):
        return await super().channel_leave(msg)

    async def channel_message(self, msg: ChannelMessage):
        return await super().channel_message(msg)

    async def channel_message_ack(self, msg: ChannelMessageAckMsg):
        return await super().channel_message_ack(msg)

    async def channel_message_send(self, msg: ChannelMessageSendMsg):
        return await super().channel_message_send(msg)

    async def channel_message_update(self, msg: ChannelMessageUpdateMsg):
        return await super().channel_message_update(msg)

    async def channel_message_remove(self, msg: ChannelMessageRemoveMsg):
        return await super().channel_message_remove(msg)

    async def channel_presence_event(self, msg: ChannelPresenceEventMsg):
        return await super().channel_presence_event(msg)

    async def error(self, msg: ErrorMsg):
        return await super().error(msg)

    async def match(self, msg: MatchMsg):
        return await super().match(msg)

    async def match_create(self, msg: MatchCreateMsg):
        return await super().match_create(msg)

    async def match_data(self, msg: MatchDataMsg):
        return await super().match_data(msg)

    async def match_data_send(self, msg: MatchDataSendMsg):
        return await super().match_data_send(msg)

    async def match_join(self, msg: MatchJoinMsg):
        return await super().match_join(msg)

    async def match_leave(self, msg: MatchLeaveMsg):
        return await super().match_leave(msg)

    async def match_presence_event(self, msg: MatchPresenceEventMsg):
        return await super().match_presence_event(msg)

    async def matchmaker_add(self, msg: MatchmakerAddMsg):
        return await super().matchmaker_add(msg)

    async def matchmaker_matched(self, msg: MatchmakerMatchedMsg):
        return await super().matchmaker_matched(msg)

    async def matchmaker_remove(self, msg: MatchmakerRemoveMsg):
        return await super().matchmaker_remove(msg)

    async def matchmaker_ticket(self, msg: MatchmakerTicketMsg):
        return await super().matchmaker_ticket(msg)

    async def notifications(self, msg: NotificationsMsg):
        return await super().notifications(msg)

    async def rpc(self, msg: RpcMsg):
        return await super().rpc(msg)

    async def status(self, msg: StatusMsg):
        return await super().status(msg)

    async def status_follow(self, msg: StatusFollowMsg):
        return await super().status_follow(msg)

    async def status_presence_event(self, msg: StatusPresenceEventMsg):
        return await super().status_presence_event(msg)

    async def status_unfollow(self, msg: StatusUnfollowMsg):
        return await super().status_unfollow(msg)

    async def status_update(self, msg: StatusUpdateMsg):
        return await super().status_update(msg)

    async def stream_data(self, msg: StreamDataMsg):
        return await super().stream_data(msg)

    async def stream_presence_event(self, msg: StreamPresenceEventMsg):
        return await super().stream_presence_event(msg)

    async def ping(self, msg: PingMsg):
        return await super().ping(msg)

    async def pong(self, msg: PongMsg):
        return await super().pong(msg)

    async def party(self, msg: PartyMsg):
        return await super().party(msg)

    async def party_create(self, msg: PartyCreateMsg):
        return await super().party_create(msg)

    async def party_join(self, msg: PartyJoinMsg):
        return await super().party_join(msg)

    async def party_leave(self, msg: PartyLeaveMsg):
        return await super().party_leave(msg)

    async def party_promote(self, msg: PartyPromoteMsg):
        return await super().party_promote(msg)

    async def party_leader(self, msg: PartyLeaderMsg):
        return await super().party_leader(msg)

    async def party_accept(self, msg: PartyAcceptMsg):
        return await super().party_accept(msg)

    async def party_remove(self, msg: PartyRemoveMsg):
        return await super().party_remove(msg)

    async def party_close(self, msg: PartyCloseMsg):
        return await super().party_close(msg)

    async def party_join_request_list(self, msg: PartyJoinRequestsMsg):
        return await super().party_join_request_list(msg)

    async def party_join_request(self, msg: PartyJoinRequestMsg):
        return await super().party_join_request(msg)

    async def party_matchmaker_add(self, msg: PartyMatchmakerAddMsg):
        return await super().party_matchmaker_add(msg)

    async def party_matchmaker_remove(self, msg: PartyMatchmakerRemoveMsg):
        return await super().party_matchmaker_remove(msg)

    async def party_matchmaker_ticket(self, msg: PartyMatchmakerTicketMsg):
        return await super().party_matchmaker_ticket(msg)

    async def party_data(self, msg: PartyDataMsg):
        return await super().party_data(msg)

    async def party_data_send(self, msg: PartyDataSendMsg):
        return await super().party_data_send(msg)

    async def party_presence_event(self, msg: PartyPresenceEventMsg):
        print("----------party_presence_event:", msg)

