# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg


class NoticeHandlerInter(ABC):
    @abstractmethod
    def channel(self, msg: ChannelMsg):
        pass

    @abstractmethod
    def channel_join(self, msg: ChannelJoinMsg):
        pass

    @abstractmethod
    def channel_leave(self, msg: ChannelLeaveMsg):
        pass

    @abstractmethod
    def channel_message(self, msg: ChannelMessage):
        pass

    @abstractmethod
    def channel_message_ack(self, msg: ChannelMessageAckMsg):
        pass

    @abstractmethod
    def channel_message_send(self, msg: ChannelMessageSendMsg):
        pass

    @abstractmethod
    def channel_message_update(self, msg: ChannelMessageUpdateMsg):
        pass

    @abstractmethod
    def channel_message_remove(self, msg: ChannelMessageRemoveMsg):
        pass

    @abstractmethod
    def channel_presence_event(self, msg: ChannelPresenceEventMsg):
        pass

    @abstractmethod
    def error(self, msg: ErrorMsg):
        pass

    @abstractmethod
    def match(self, msg: MatchMsg):
        pass

    @abstractmethod
    def match_create(self, msg: MatchCreateMsg):
        pass

    @abstractmethod
    def match_data(self, msg: MatchDataMsg):
        pass

    @abstractmethod
    def match_data_send(self, msg: MatchDataSendMsg):
        pass

    @abstractmethod
    def match_join(self, msg: MatchJoinMsg):
        pass

    @abstractmethod
    def match_leave(self, msg: MatchLeaveMsg):
        pass

    @abstractmethod
    def match_presence_event(self, msg: MatchPresenceEventMsg):
        pass

    @abstractmethod
    def matchmaker_add(self, msg: MatchmakerAddMsg):
        pass

    @abstractmethod
    def matchmaker_matched(self, msg: MatchmakerMatchedMsg):
        pass

    @abstractmethod
    def matchmaker_remove(self, msg: MatchmakerRemoveMsg):
        pass

    @abstractmethod
    def matchmaker_ticket(self, msg: MatchmakerTicketMsg):
        pass

    @abstractmethod
    def notifications(self, msg: NotificationsMsg):
        pass

    @abstractmethod
    def rpc(self, msg: RpcMsg):
        pass

    @abstractmethod
    def status(self, msg: StatusMsg):
        pass

    @abstractmethod
    def status_follow(self, msg: StatusFollowMsg):
        pass

    @abstractmethod
    def status_presence_event(self, msg: StatusPresenceEventMsg):
        pass

    @abstractmethod
    def status_unfollow(self, msg: StatusUnfollowMsg):
        pass

    @abstractmethod
    def status_update(self, msg: StatusUpdateMsg):
        pass

    @abstractmethod
    def stream_data(self, msg: StreamDataMsg):
        pass

    @abstractmethod
    def stream_presence_event(self, msg: StreamPresenceEventMsg):
        pass

    @abstractmethod
    def ping(self, msg: PingMsg):
        pass

    @abstractmethod
    def pong(self, msg: PongMsg):
        pass

    @abstractmethod
    def party(self, msg: PartyMsg):
        pass

    @abstractmethod
    def party_create(self, msg: PartyCreateMsg):
        pass

    @abstractmethod
    def party_join(self, msg: PartyJoinMsg):
        pass

    @abstractmethod
    def party_leave(self, msg: PartyLeaveMsg):
        pass

    @abstractmethod
    def party_promote(self, msg: PartyPromoteMsg):
        pass

    @abstractmethod
    def party_leader(self, msg: PartyLeaderMsg):
        pass

    @abstractmethod
    def party_accept(self, msg: PartyAcceptMsg):
        pass

    @abstractmethod
    def party_remove(self, msg: PartyRemoveMsg):
        pass

    @abstractmethod
    def party_close(self, msg: PartyCloseMsg):
        pass

    @abstractmethod
    def party_join_request_list(self, msg: PartyJoinRequestsMsg):
        pass

    @abstractmethod
    def party_join_request(self, msg: PartyJoinRequestMsg):
        pass

    @abstractmethod
    def party_matchmaker_add(self, msg: PartyMatchmakerAddMsg):
        pass

    @abstractmethod
    def party_matchmaker_remove(self, msg: PartyMatchmakerRemoveMsg):
        pass

    @abstractmethod
    def party_matchmaker_ticket(self, msg: PartyMatchmakerTicketMsg):
        pass

    @abstractmethod
    def party_data(self, msg: PartyDataMsg):
        pass

    @abstractmethod
    def party_data_send(self, msg: PartyDataSendMsg):
        pass

    @abstractmethod
    def party_presence_event(self, msg: PartyPresenceEventMsg):
        pass
