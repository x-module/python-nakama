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
    def channel(self, msg: ChannelMsg):
        return super().channel(msg)

    def channel_join(self, msg: ChannelJoinMsg):
        return super().channel_join(msg)

    def channel_leave(self, msg: ChannelLeaveMsg):
        return super().channel_leave(msg)

    def channel_message(self, msg: ChannelMessage):
        return super().channel_message(msg)

    def channel_message_ack(self, msg: ChannelMessageAckMsg):
        return super().channel_message_ack(msg)

    def channel_message_send(self, msg: ChannelMessageSendMsg):
        return super().channel_message_send(msg)

    def channel_message_update(self, msg: ChannelMessageUpdateMsg):
        return super().channel_message_update(msg)

    def channel_message_remove(self, msg: ChannelMessageRemoveMsg):
        return super().channel_message_remove(msg)

    def channel_presence_event(self, msg: ChannelPresenceEventMsg):
        return super().channel_presence_event(msg)

    def error(self, msg: ErrorMsg):
        return super().error(msg)

    def match(self, msg: MatchMsg):
        return super().match(msg)

    def match_create(self, msg: MatchCreateMsg):
        return super().match_create(msg)

    def match_data(self, msg: MatchDataMsg):
        return super().match_data(msg)

    def match_data_send(self, msg: MatchDataSendMsg):
        return super().match_data_send(msg)

    def match_join(self, msg: MatchJoinMsg):
        return super().match_join(msg)

    def match_leave(self, msg: MatchLeaveMsg):
        return super().match_leave(msg)

    def match_presence_event(self, msg: MatchPresenceEventMsg):
        return super().match_presence_event(msg)

    def matchmaker_add(self, msg: MatchmakerAddMsg):
        return super().matchmaker_add(msg)

    def matchmaker_matched(self, msg: MatchmakerMatchedMsg):
        return super().matchmaker_matched(msg)

    def matchmaker_remove(self, msg: MatchmakerRemoveMsg):
        return super().matchmaker_remove(msg)

    def matchmaker_ticket(self, msg: MatchmakerTicketMsg):
        return super().matchmaker_ticket(msg)

    def notifications(self, msg: NotificationsMsg):
        return super().notifications(msg)

    def rpc(self, msg: RpcMsg):
        return super().rpc(msg)

    def status(self, msg: StatusMsg):
        return super().status(msg)

    def status_follow(self, msg: StatusFollowMsg):
        return super().status_follow(msg)

    def status_presence_event(self, msg: StatusPresenceEventMsg):
        return super().status_presence_event(msg)

    def status_unfollow(self, msg: StatusUnfollowMsg):
        return super().status_unfollow(msg)

    def status_update(self, msg: StatusUpdateMsg):
        return super().status_update(msg)

    def stream_data(self, msg: StreamDataMsg):
        return super().stream_data(msg)

    def stream_presence_event(self, msg: StreamPresenceEventMsg):
        return super().stream_presence_event(msg)

    def ping(self, msg: PingMsg):
        return super().ping(msg)

    def pong(self, msg: PongMsg):
        return super().pong(msg)

    def party(self, msg: PartyMsg):
        return super().party(msg)

    def party_create(self, msg: PartyCreateMsg):
        return super().party_create(msg)

    def party_join(self, msg: PartyJoinMsg):
        return super().party_join(msg)

    def party_leave(self, msg: PartyLeaveMsg):
        return super().party_leave(msg)

    def party_promote(self, msg: PartyPromoteMsg):
        return super().party_promote(msg)

    def party_leader(self, msg: PartyLeaderMsg):
        return super().party_leader(msg)

    def party_accept(self, msg: PartyAcceptMsg):
        return super().party_accept(msg)

    def party_remove(self, msg: PartyRemoveMsg):
        return super().party_remove(msg)

    def party_close(self, msg: PartyCloseMsg):
        return super().party_close(msg)

    def party_join_request_list(self, msg: PartyJoinRequestsMsg):
        return super().party_join_request_list(msg)

    def party_join_request(self, msg: PartyJoinRequestMsg):
        return super().party_join_request(msg)

    def party_matchmaker_add(self, msg: PartyMatchmakerAddMsg):
        return super().party_matchmaker_add(msg)

    def party_matchmaker_remove(self, msg: PartyMatchmakerRemoveMsg):
        return super().party_matchmaker_remove(msg)

    def party_matchmaker_ticket(self, msg: PartyMatchmakerTicketMsg):
        return super().party_matchmaker_ticket(msg)

    def party_data(self, msg: PartyDataMsg):
        return super().party_data(msg)

    def party_data_send(self, msg: PartyDataSendMsg):
        return super().party_data_send(msg)

    def party_presence_event(self, msg: PartyPresenceEventMsg):
        print("----------party_presence_event:", msg)
