# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg


class NoticeHandlerInter(ABC):
    @abstractmethod
    def channel(self, msg: ChannelMsg):
        pass

    @abstractmethod
    def channelJoin(self, msg: ChannelJoinMsg):
        pass

    @abstractmethod
    def channelLeave(self, msg: ChannelLeaveMsg):
        pass

    @abstractmethod
    def channelMessage(self, msg: ChannelMessage):
        pass

    @abstractmethod
    def channelMessageAck(self, msg: ChannelMessageAckMsg):
        pass

    @abstractmethod
    def channelMessageSend(self, msg: ChannelMessageSendMsg):
        pass

    @abstractmethod
    def channelMessageUpdate(self, msg: ChannelMessageUpdateMsg):
        pass

    @abstractmethod
    def channelMessageRemove(self, msg: ChannelMessageRemoveMsg):
        pass

    @abstractmethod
    def channelPresenceEvent(self, msg: ChannelPresenceEventMsg):
        pass

    @abstractmethod
    def error(self, msg: ErrorMsg):
        pass

    @abstractmethod
    def match(self, msg: MatchMsg):
        pass

    @abstractmethod
    def matchCreate(self, msg: MatchCreateMsg):
        pass

    @abstractmethod
    def matchData(self, msg: MatchDataMsg):
        pass

    @abstractmethod
    def matchDataSend(self, msg: MatchDataSendMsg):
        pass

    @abstractmethod
    def matchJoin(self, msg: MatchJoinMsg):
        pass

    @abstractmethod
    def matchLeave(self, msg: MatchLeaveMsg):
        pass

    @abstractmethod
    def matchPresenceEvent(self, msg: MatchPresenceEventMsg):
        pass

    @abstractmethod
    def matchmakerAdd(self, msg: MatchmakerAddMsg):
        pass

    @abstractmethod
    def matchmakerMatched(self, msg: MatchmakerMatchedMsg):
        pass

    @abstractmethod
    def matchmakerRemove(self, msg: MatchmakerRemoveMsg):
        pass

    @abstractmethod
    def matchmakerTicket(self, msg: MatchmakerTicketMsg):
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
    def statusFollow(self, msg: StatusFollowMsg):
        pass

    @abstractmethod
    def statusPresenceEvent(self, msg: StatusPresenceEventMsg):
        pass

    @abstractmethod
    def statusUnfollow(self, msg: StatusUnfollowMsg):
        pass

    @abstractmethod
    def statusUpdate(self, msg: StatusUpdateMsg):
        pass

    @abstractmethod
    def streamData(self, msg: StreamDataMsg):
        pass

    @abstractmethod
    def streamPresenceEvent(self, msg: StreamPresenceEventMsg):
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
    def partyCreate(self, msg: PartyCreateMsg):
        pass

    @abstractmethod
    def partyJoin(self, msg: PartyJoinMsg):
        pass

    @abstractmethod
    def partyLeave(self, msg: PartyLeaveMsg):
        pass

    @abstractmethod
    def partyPromote(self, msg: PartyPromoteMsg):
        pass

    @abstractmethod
    def partyLeader(self, msg: PartyLeaderMsg):
        pass

    @abstractmethod
    def partyAccept(self, msg: PartyAcceptMsg):
        pass

    @abstractmethod
    def partyRemove(self, msg: PartyRemoveMsg):
        pass

    @abstractmethod
    def partyClose(self, msg: PartyCloseMsg):
        pass

    @abstractmethod
    def partyJoinRequestList(self, msg: PartyJoinRequestsMsg):
        pass

    @abstractmethod
    def partyJoinRequest(self, msg: PartyJoinRequestMsg):
        pass

    @abstractmethod
    def partyMatchmakerAdd(self, msg: PartyMatchmakerAddMsg):
        pass

    @abstractmethod
    def partyMatchmakerRemove(self, msg: PartyMatchmakerRemoveMsg):
        pass

    @abstractmethod
    def partyMatchmakerTicket(self, msg: PartyMatchmakerTicketMsg):
        pass

    @abstractmethod
    def partyData(self, msg: PartyDataMsg):
        pass

    @abstractmethod
    def partyDataSend(self, msg: PartyDataSendMsg):
        pass

    @abstractmethod
    def partyPresenceEvent(self, msg: PartyPresenceEventMsg):
        pass
