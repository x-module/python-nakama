# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg


class NoticeHandlerInter(ABC):
    @abstractmethod
    async def channel(self, msg: ChannelMsg):
        pass

    @abstractmethod
    async def channelJoin(self, msg: ChannelJoinMsg):
        pass

    @abstractmethod
    async def channelLeave(self, msg: ChannelLeaveMsg):
        pass

    @abstractmethod
    async def channelMessage(self, msg: ChannelMessage):
        pass

    @abstractmethod
    async def channelMessageAck(self, msg: ChannelMessageAckMsg):
        pass

    @abstractmethod
    async def channelMessageSend(self, msg: ChannelMessageSendMsg):
        pass

    @abstractmethod
    async def channelMessageUpdate(self, msg: ChannelMessageUpdateMsg):
        pass

    @abstractmethod
    async def channelMessageRemove(self, msg: ChannelMessageRemoveMsg):
        pass

    @abstractmethod
    async def channelPresenceEvent(self, msg: ChannelPresenceEventMsg):
        pass

    @abstractmethod
    async def error(self, msg: ErrorMsg):
        pass

    @abstractmethod
    async def match(self, msg: MatchMsg):
        pass

    @abstractmethod
    async def matchCreate(self, msg: MatchCreateMsg):
        pass

    @abstractmethod
    async def matchData(self, msg: MatchDataMsg):
        pass

    @abstractmethod
    async def matchDataSend(self, msg: MatchDataSendMsg):
        pass

    @abstractmethod
    async def matchJoin(self, msg: MatchJoinMsg):
        pass

    @abstractmethod
    async def matchLeave(self, msg: MatchLeaveMsg):
        pass

    @abstractmethod
    async def matchPresenceEvent(self, msg: MatchPresenceEventMsg):
        pass

    @abstractmethod
    async def matchmakerAdd(self, msg: MatchmakerAddMsg):
        pass

    @abstractmethod
    async def matchmakerMatched(self, msg: MatchmakerMatchedMsg):
        pass

    @abstractmethod
    async def matchmakerRemove(self, msg: MatchmakerRemoveMsg):
        pass

    @abstractmethod
    async def matchmakerTicket(self, msg: MatchmakerTicketMsg):
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
    async def statusFollow(self, msg: StatusFollowMsg):
        pass

    @abstractmethod
    async def statusPresenceEvent(self, msg: StatusPresenceEventMsg):
        pass

    @abstractmethod
    async def statusUnfollow(self, msg: StatusUnfollowMsg):
        pass

    @abstractmethod
    async def statusUpdate(self, msg: StatusUpdateMsg):
        pass

    @abstractmethod
    async def streamData(self, msg: StreamDataMsg):
        pass

    @abstractmethod
    async def streamPresenceEvent(self, msg: StreamPresenceEventMsg):
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
    async def partyCreate(self, msg: PartyCreateMsg):
        pass

    @abstractmethod
    async def partyJoin(self, msg: PartyJoinMsg):
        pass

    @abstractmethod
    async def partyLeave(self, msg: PartyLeaveMsg):
        pass

    @abstractmethod
    async def partyPromote(self, msg: PartyPromoteMsg):
        pass

    @abstractmethod
    async def partyLeader(self, msg: PartyLeaderMsg):
        pass

    @abstractmethod
    async def partyAccept(self, msg: PartyAcceptMsg):
        pass

    @abstractmethod
    async def partyRemove(self, msg: PartyRemoveMsg):
        pass

    @abstractmethod
    async def partyClose(self, msg: PartyCloseMsg):
        pass

    @abstractmethod
    async def partyJoinRequestList(self, msg: PartyJoinRequestsMsg):
        pass

    @abstractmethod
    async def partyJoinRequest(self, msg: PartyJoinRequestMsg):
        pass

    @abstractmethod
    async def partyMatchmakerAdd(self, msg: PartyMatchmakerAddMsg):
        pass

    @abstractmethod
    async def partyMatchmakerRemove(self, msg: PartyMatchmakerRemoveMsg):
        pass

    @abstractmethod
    async def partyMatchmakerTicket(self, msg: PartyMatchmakerTicketMsg):
        pass

    @abstractmethod
    async def partyData(self, msg: PartyDataMsg):
        pass

    @abstractmethod
    async def partyDataSend(self, msg: PartyDataSendMsg):
        pass

    @abstractmethod
    async def partyPresenceEvent(self, msg: PartyPresenceEventMsg):
        pass

    @abstractmethod
    async def disconnect(self):
        pass
