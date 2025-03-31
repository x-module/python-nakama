# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg


class NoticeHandlerInter(ABC):
    @abstractmethod
    async def channel(self, msg: ChannelMsg):
        pass

    @abstractmethod
    async def channel_join(self, msg: ChannelJoinMsg):
        pass

    @abstractmethod
    async def channel_leave(self, msg: ChannelLeaveMsg):
        pass

    @abstractmethod
    async def channel_message(self, msg: ChannelMessage):
        pass

    @abstractmethod
    async def channel_message_ack(self, msg: ChannelMessageAckMsg):
        pass

    @abstractmethod
    async def channel_message_send(self, msg: ChannelMessageSendMsg):
        pass

    @abstractmethod
    async def channel_message_update(self, msg: ChannelMessageUpdateMsg):
        pass

    @abstractmethod
    async def channel_message_remove(self, msg: ChannelMessageRemoveMsg):
        pass

    @abstractmethod
    async def channel_presence_event(self, msg: ChannelPresenceEventMsg):
        pass

    @abstractmethod
    async def error(self, msg: ErrorMsg):
        pass

    @abstractmethod
    async def match(self, msg: MatchMsg):
        pass

    @abstractmethod
    async def match_create(self, msg: MatchCreateMsg):
        pass

    @abstractmethod
    async def match_data(self, msg: MatchDataMsg):
        pass

    @abstractmethod
    async def match_data_send(self, msg: MatchDataSendMsg):
        pass

    @abstractmethod
    async def match_join(self, msg: MatchJoinMsg):
        pass

    @abstractmethod
    async def match_leave(self, msg: MatchLeaveMsg):
        pass

    @abstractmethod
    async def match_presence_event(self, msg: MatchPresenceEventMsg):
        pass

    @abstractmethod
    async def matchmaker_add(self, msg: MatchmakerAddMsg):
        pass

    @abstractmethod
    async def matchmaker_matched(self, msg: MatchmakerMatchedMsg):
        pass

    @abstractmethod
    async def matchmaker_remove(self, msg: MatchmakerRemoveMsg):
        pass

    @abstractmethod
    async def matchmaker_ticket(self, msg: MatchmakerTicketMsg):
        pass

    @abstractmethod
    async def notifications(self, msg: NotificationsMsg):
        pass

    @abstractmethod
    async def rpc(self, msg: RpcMsg):
        pass

    @abstractmethod
    async def status(self, msg: StatusMsg):
        pass

    @abstractmethod
    async def status_follow(self, msg: StatusFollowMsg):
        pass

    @abstractmethod
    async def status_presence_event(self, msg: StatusPresenceEventMsg):
        pass

    @abstractmethod
    async def status_unfollow(self, msg: StatusUnfollowMsg):
        pass

    @abstractmethod
    async def status_update(self, msg: StatusUpdateMsg):
        pass

    @abstractmethod
    async def stream_data(self, msg: StreamDataMsg):
        pass

    @abstractmethod
    async def stream_presence_event(self, msg: StreamPresenceEventMsg):
        pass

    @abstractmethod
    async def ping(self, msg: PingMsg):
        pass

    @abstractmethod
    async def pong(self, msg: PongMsg):
        pass

    @abstractmethod
    async def party(self, msg: PartyMsg):
        pass

    @abstractmethod
    async def party_create(self, msg: PartyCreateMsg):
        pass

    @abstractmethod
    async def party_join(self, msg: PartyJoinMsg):
        pass

    @abstractmethod
    async def party_leave(self, msg: PartyLeaveMsg):
        pass

    @abstractmethod
    async def party_promote(self, msg: PartyPromoteMsg):
        pass

    @abstractmethod
    async def party_leader(self, msg: PartyLeaderMsg):
        pass

    @abstractmethod
    async def party_accept(self, msg: PartyAcceptMsg):
        pass

    @abstractmethod
    async def party_remove(self, msg: PartyRemoveMsg):
        pass

    @abstractmethod
    async def party_close(self, msg: PartyCloseMsg):
        pass

    @abstractmethod
    async def party_join_request_list(self, msg: PartyJoinRequestsMsg):
        pass

    @abstractmethod
    async def party_join_request(self, msg: PartyJoinRequestMsg):
        pass

    @abstractmethod
    async def party_matchmaker_add(self, msg: PartyMatchmakerAddMsg):
        pass

    @abstractmethod
    async def party_matchmaker_remove(self, msg: PartyMatchmakerRemoveMsg):
        pass

    @abstractmethod
    async def party_matchmaker_ticket(self, msg: PartyMatchmakerTicketMsg):
        pass

    @abstractmethod
    async def party_data(self, msg: PartyDataMsg):
        pass

    @abstractmethod
    async def party_data_send(self, msg: PartyDataSendMsg):
        pass

    @abstractmethod
    async def party_presence_event(self, msg: PartyPresenceEventMsg):
        pass
