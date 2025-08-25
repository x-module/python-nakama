# -*- coding: utf-8 -*-
import base64

from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg, Envelope
from nakama.utils.logger import Logger


class NoticeHandler:
    def __init__(self):
        self.logger = Logger(__name__)
        self._handler: NoticeHandlerInter

    def setHandler(self, handler: NoticeHandlerInter):
        self._handler = handler

    async def handleEvent(self, msgType: str, event: Envelope):
        if self._handler is not None:
            if msgType == "channel":
                await self._handler.channel(event.channel)
            elif msgType == "notifications":
                await self._handler.notifications(event.notifications)
            elif msgType == "rpc":
                await self._handler.rpc(event.rpc)
            elif msgType == "status":
                await self._handler.status(event.status)
            elif msgType == "status_follow":
                await self._handler.statusFollow(event.status_follow)
            elif msgType == "status_presence_event":
                await self._handler.statusPresenceEvent(event.status_presence_event)
            elif msgType == "status_unfollow":
                await self._handler.statusUnfollow(event.status_unfollow)
            elif msgType == "status_update":
                await self._handler.statusUpdate(event.status_update)
            elif msgType == "stream_data":
                await self._handler.streamData(event.stream_data)
            elif msgType == "stream_presence_event":
                await self._handler.streamPresenceEvent(event.stream_presence_event)
            elif msgType == "ping":
                await self._handler.ping(event.ping)
            elif msgType == "pong":
                await self._handler.pong(event.pong)
            elif msgType == "party":
                await self._handler.party(event.party)
            elif msgType == "party_create":
                await self._handler.partyCreate(event.party_create)
            elif msgType == "party_join":
                await self._handler.partyJoin(event.party_join)
            elif msgType == "party_leave":
                await self._handler.partyLeave(event.party_leave)
            elif msgType == "party_promote":
                await self._handler.partyPromote(event.party_promote)
            elif msgType == "party_leader":
                await self._handler.partyLeader(event.party_leader)
            elif msgType == "party_accept":
                await self._handler.partyAccept(event.party_accept)
            elif msgType == "party_remove":
                await self._handler.partyRemove(event.party_remove)
            elif msgType == "party_close":
                await self._handler.partyClose(event.party_close)
            elif msgType == "party_join_request_list":
                await self._handler.partyJoinRequestList(event.party_join_request_list)
            elif msgType == "party_join_request":
                await self._handler.partyJoinRequest(event.party_join_request)
            elif msgType == "party_matchmaker_add":
                await self._handler.partyMatchmakerAdd(event.party_matchmaker_add)
            elif msgType == "party_matchmaker_remove":
                await self._handler.partyMatchmakerRemove(event.party_matchmaker_remove)
            elif msgType == "party_matchmaker_ticket":
                await self._handler.partyMatchmakerTicket(event.party_matchmaker_ticket)
            elif msgType == "party_data":
                await self._handler.partyData(event.party_data)
            elif msgType == "party_data_send":
                await self._handler.partyDataSend(event.party_data_send)
            elif msgType == "party_presence_event":
                await self._handler.partyPresenceEvent(event.party_presence_event)
            elif msgType == 'match_data':
                await self._handler.matchData(event.match_data)
            elif msgType == 'match_create':
                await self._handler.matchCreate(event.match_data)
            elif msgType == 'match_presence_event':
                await self._handler.matchPresenceEvent(event.match_presence_event)
            else:
                self.logger.warning("Unknown notice event msgType:%s event:%s", msgType, event)
        else:
            self.logger.debug("receive notice:%s", event)


# 基础消息handler
class BaseNoticeHandler(NoticeHandlerInter):
    def __init__(self):
        self.logger = Logger(__name__)

    async def channel(self, msg: ChannelMsg):
        self.logger.debug("receive channel:%s", msg)

    async def channelJoin(self, msg: ChannelJoinMsg):
        self.logger.debug("receive channel_join:%s", msg)

    async def channelLeave(self, msg: ChannelLeaveMsg):
        self.logger.debug("receive channel_leave:%s", msg)

    async def channelMessage(self, msg: ChannelMessage):
        self.logger.debug("receive channelMessage:%s", msg)

    async def channelMessageAck(self, msg: ChannelMessageAckMsg):
        self.logger.debug("receive channelMessage_ack:%s", msg)

    async def channelMessageSend(self, msg: ChannelMessageSendMsg):
        self.logger.debug("receive channelMessage_send:%s", msg)

    async def channelMessageUpdate(self, msg: ChannelMessageUpdateMsg):
        self.logger.debug("receive channelMessage_update:%s", msg)

    async def channelMessageRemove(self, msg: ChannelMessageRemoveMsg):
        self.logger.debug("receive channelMessage_remove:%s", msg)

    async def channelPresenceEvent(self, msg: ChannelPresenceEventMsg):
        self.logger.debug("receive channel_presence_event:%s", msg)

    async def error(self, msg: ErrorMsg):
        self.logger.debug("receive error:%s", msg)

    async def match(self, msg: MatchMsg):
        self.logger.debug("receive match:%s", msg)

    async def matchCreate(self, msg: MatchCreateMsg):
        self.logger.debug("receive match_create:%s", msg)

    async def matchData(self, msg: MatchDataMsg):
        self.logger.debug("receive match_data:%s", msg)

    async def matchDataSend(self, msg: MatchDataSendMsg):
        self.logger.debug("receive match_data_send:%s", msg)

    async def matchJoin(self, msg: MatchJoinMsg):
        self.logger.debug("receive match_join:%s", msg)

    async def matchLeave(self, msg: MatchLeaveMsg):
        self.logger.debug("receive match_leave:%s", msg)

    async def matchPresenceEvent(self, msg: MatchPresenceEventMsg):
        self.logger.debug("receive match_presence_event:%s", msg)

    async def matchmakerAdd(self, msg: MatchmakerAddMsg):
        self.logger.debug("receive matchmaker_add:%s", msg)

    async def matchmakerMatched(self, msg: MatchmakerMatchedMsg):
        self.logger.debug("receive matchmaker_matched:%s", msg)

    async def matchmakerRemove(self, msg: MatchmakerRemoveMsg):
        self.logger.debug("receive matchmaker_remove:%s", msg)

    async def matchmakerTicket(self, msg: MatchmakerTicketMsg):
        self.logger.debug("receive matchmaker_ticket:%s", msg)

    async def notifications(self, msg: NotificationsMsg):
        self.logger.debug("receive notifications:%s", msg)

    async def rpc(self, msg: RpcMsg):
        self.logger.debug("receive rpc:%s", msg)

    async def status(self, msg: StatusMsg):
        self.logger.debug("receive status:%s", msg)

    async def statusFollow(self, msg: StatusFollowMsg):
        self.logger.debug("receive status_follow:%s", msg)

    async def statusPresenceEvent(self, msg: StatusPresenceEventMsg):
        self.logger.debug("receive status_presence_event:%s", msg)

    async def statusUnfollow(self, msg: StatusUnfollowMsg):
        self.logger.debug("receive status_unfollow:%s", msg)

    async def statusUpdate(self, msg: StatusUpdateMsg):
        self.logger.debug("receive status_update:%s", msg)

    async def streamData(self, msg: StreamDataMsg):
        self.logger.debug("receive stream_data:%s", msg)

    async def streamPresenceEvent(self, msg: StreamPresenceEventMsg):
        self.logger.debug("receive stream_presence_event:%s", msg)

    async def ping(self, msg: PingMsg):
        self.logger.debug("receive ping:%s", msg)

    async def pong(self, msg: PongMsg):
        self.logger.debug("receive pong:%s", msg)

    async def party(self, msg: PartyMsg):
        self.logger.debug("receive party:%s", msg)

    async def partyCreate(self, msg: PartyCreateMsg):
        self.logger.debug("receive party_create:%s", msg)

    async def partyJoin(self, msg: PartyJoinMsg):
        self.logger.debug("receive party_join:%s", msg)

    async def partyLeave(self, msg: PartyLeaveMsg):
        self.logger.debug("receive party_leave:%s", msg)

    async def partyPromote(self, msg: PartyPromoteMsg):
        self.logger.debug("receive party_promote:%s", msg)

    async def partyLeader(self, msg: PartyLeaderMsg):
        self.logger.debug("receive party_leader:%s", msg)

    async def partyAccept(self, msg: PartyAcceptMsg):
        self.logger.debug("receive party_accept:%s", msg)

    async def partyRemove(self, msg: PartyRemoveMsg):
        self.logger.debug("receive party_remove:%s", msg)

    async def partyClose(self, msg: PartyCloseMsg):
        self.logger.debug("receive party_close:%s", msg)

    async def partyJoinRequestList(self, msg: PartyJoinRequestsMsg):
        self.logger.debug("receive party_join_request_list:%s", msg)

    async def partyJoinRequest(self, msg: PartyJoinRequestMsg):
        self.logger.debug("receive party_join_request:%s", msg)

    async def partyMatchmakerAdd(self, msg: PartyMatchmakerAddMsg):
        self.logger.debug("receive party_matchmaker_add:%s", msg)

    async def partyMatchmakerRemove(self, msg: PartyMatchmakerRemoveMsg):
        self.logger.debug("receive party_matchmaker_remove:%s", msg)

    async def partyMatchmakerTicket(self, msg: PartyMatchmakerTicketMsg):
        self.logger.debug("receive party_matchmaker_ticket:%s", msg)

    async def partyData(self, msg: PartyDataMsg):
        self.logger.debug("receive party_data:%s", msg)

    async def partyDataSend(self, msg: PartyDataSendMsg):
        self.logger.debug("receive party_data_send:%s", msg)

    async def partyPresenceEvent(self, msg: PartyPresenceEventMsg):
        self.logger.debug("receive party_presence_event:%s", msg)
