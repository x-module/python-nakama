# -*- coding: utf-8 -*-

from nakama.inter.notice_handler_inter import NoticeHandlerInter
from nakama.common.nakama import ChannelMsg, ChannelJoinMsg, ChannelLeaveMsg, ChannelMessage, ChannelMessageAckMsg, ChannelMessageSendMsg, ChannelMessageUpdateMsg, ChannelMessageRemoveMsg, ChannelPresenceEventMsg, ErrorMsg, MatchMsg, MatchCreateMsg, MatchDataMsg, MatchDataSendMsg, MatchJoinMsg, MatchLeaveMsg, MatchPresenceEventMsg, MatchmakerAddMsg, MatchmakerMatchedMsg, MatchmakerRemoveMsg, MatchmakerTicketMsg, NotificationsMsg, RpcMsg, StatusMsg, StatusFollowMsg, StatusPresenceEventMsg, \
    StatusUnfollowMsg, StatusUpdateMsg, StreamDataMsg, StreamPresenceEventMsg, PingMsg, PongMsg, PartyMsg, PartyCreateMsg, PartyJoinMsg, PartyLeaveMsg, PartyPromoteMsg, PartyLeaderMsg, PartyAcceptMsg, PartyRemoveMsg, PartyCloseMsg, PartyJoinRequestsMsg, PartyJoinRequestMsg, PartyMatchmakerAddMsg, PartyMatchmakerRemoveMsg, PartyMatchmakerTicketMsg, PartyDataMsg, PartyDataSendMsg, PartyPresenceEventMsg, Envelope
from nakama.utils.logger import Logger


class NoticeHandler:
    def __init__(self):
        self.logger = Logger(f"{__name__}.{self.__class__.__name__}")
        self._handler: NoticeHandlerInter = BaseNoticeHandler()

    def setHandler(self, handler: NoticeHandlerInter):
        self._handler = handler

    def handleEvent(self, msgType: str, event: Envelope):
        if self._handler is not None:
            if msgType == "channel":
                self._handler.channel(event.channel)
            elif msgType == "notifications":
                self._handler.notifications(event.notifications)
            elif msgType == "rpc":
                self._handler.rpc(event.rpc)
            elif msgType == "status":
                self._handler.status(event.status)
            elif msgType == "status_follow":
                self._handler.statusFollow(event.status_follow)
            elif msgType == "status_presence_event":
                self._handler.statusPresenceEvent(event.status_presence_event)
            elif msgType == "status_unfollow":
                self._handler.statusUnfollow(event.status_unfollow)
            elif msgType == "status_update":
                self._handler.statusUpdate(event.status_update)
            elif msgType == "stream_data":
                self._handler.streamData(event.stream_data)
            elif msgType == "stream_presence_event":
                self._handler.streamPresenceEvent(event.stream_presence_event)
            elif msgType == "ping":
                self._handler.ping(event.ping)
            elif msgType == "pong":
                self._handler.pong(event.pong)
            elif msgType == "party":
                self._handler.party(event.party)
            elif msgType == "party_create":
                self._handler.partyCreate(event.party_create)
            elif msgType == "party_join":
                self._handler.partyJoin(event.party_join)
            elif msgType == "party_leave":
                self._handler.partyLeave(event.party_leave)
            elif msgType == "party_promote":
                self._handler.partyPromote(event.party_promote)
            elif msgType == "party_leader":
                self._handler.partyLeader(event.party_leader)
            elif msgType == "party_accept":
                self._handler.partyAccept(event.party_accept)
            elif msgType == "party_remove":
                self._handler.partyRemove(event.party_remove)
            elif msgType == "party_close":
                self._handler.partyClose(event.party_close)
            elif msgType == "party_join_request_list":
                self._handler.partyJoinRequestList(event.party_join_request_list)
            elif msgType == "party_join_request":
                self._handler.partyJoinRequest(event.party_join_request)
            elif msgType == "party_matchmaker_add":
                self._handler.partyMatchmakerAdd(event.party_matchmaker_add)
            elif msgType == "party_matchmaker_remove":
                self._handler.partyMatchmakerRemove(event.party_matchmaker_remove)
            elif msgType == "party_matchmaker_ticket":
                self._handler.partyMatchmakerTicket(event.party_matchmaker_ticket)
            elif msgType == "party_data":
                self._handler.partyData(event.party_data)
            elif msgType == "party_data_send":
                self._handler.partyDataSend(event.party_data_send)
            elif msgType == "party_presence_event":
                self._handler.partyPresenceEvent(event.party_presence_event)
            elif msgType == "on_error":
                self._handler.error(event.error)
            elif msgType == "on_close":
                self._handler.close(event.error)
            else:
                self.logger.warning("Unknown notice event event:%s", event)
        else:
            self.logger.debug("receive notice:%s", event)


# 基础消息handler
class BaseNoticeHandler(NoticeHandlerInter):
    def __init__(self):
        self.logger = Logger(f"{__name__}.{self.__class__.__name__}")

    def close(self, msg: ErrorMsg):
        self.logger.error("receive ErrorMsg:%s", msg)

    def channel(self, msg: ChannelMsg):
        self.logger.debug("receive channel:%s", msg)

    def channelJoin(self, msg: ChannelJoinMsg):
        self.logger.debug("receive channel_join:%s", msg)

    def channelLeave(self, msg: ChannelLeaveMsg):
        self.logger.debug("receive channel_leave:%s", msg)

    def channelMessage(self, msg: ChannelMessage):
        self.logger.debug("receive channelMessage:%s", msg)

    def channelMessageAck(self, msg: ChannelMessageAckMsg):
        self.logger.debug("receive channelMessage_ack:%s", msg)

    def channelMessageSend(self, msg: ChannelMessageSendMsg):
        self.logger.debug("receive channelMessage_send:%s", msg)

    def channelMessageUpdate(self, msg: ChannelMessageUpdateMsg):
        self.logger.debug("receive channelMessage_update:%s", msg)

    def channelMessageRemove(self, msg: ChannelMessageRemoveMsg):
        self.logger.debug("receive channelMessage_remove:%s", msg)

    def channelPresenceEvent(self, msg: ChannelPresenceEventMsg):
        self.logger.debug("receive channel_presence_event:%s", msg)

    def error(self, msg: ErrorMsg):
        self.logger.debug("receive error:%s", msg)

    def match(self, msg: MatchMsg):
        self.logger.debug("receive match:%s", msg)

    def matchCreate(self, msg: MatchCreateMsg):
        self.logger.debug("receive match_create:%s", msg)

    def matchData(self, msg: MatchDataMsg):
        self.logger.debug("receive match_data:%s", msg)

    def matchDataSend(self, msg: MatchDataSendMsg):
        self.logger.debug("receive match_data_send:%s", msg)

    def matchJoin(self, msg: MatchJoinMsg):
        self.logger.debug("receive match_join:%s", msg)

    def matchLeave(self, msg: MatchLeaveMsg):
        self.logger.debug("receive match_leave:%s", msg)

    def matchPresenceEvent(self, msg: MatchPresenceEventMsg):
        self.logger.debug("receive match_presence_event:%s", msg)

    def matchmakerAdd(self, msg: MatchmakerAddMsg):
        self.logger.debug("receive matchmaker_add:%s", msg)

    def matchmakerMatched(self, msg: MatchmakerMatchedMsg):
        self.logger.debug("receive matchmaker_matched:%s", msg)

    def matchmakerRemove(self, msg: MatchmakerRemoveMsg):
        self.logger.debug("receive matchmaker_remove:%s", msg)

    def matchmakerTicket(self, msg: MatchmakerTicketMsg):
        self.logger.debug("receive matchmaker_ticket:%s", msg)

    def notifications(self, msg: NotificationsMsg):



        self.logger.debug("receive notifications:%s", msg)

    def rpc(self, msg: RpcMsg):
        self.logger.debug("receive rpc:%s", msg)

    def status(self, msg: StatusMsg):
        self.logger.debug("receive status:%s", msg)

    def statusFollow(self, msg: StatusFollowMsg):
        self.logger.debug("receive status_follow:%s", msg)

    def statusPresenceEvent(self, msg: StatusPresenceEventMsg):
        self.logger.debug("receive status_presence_event:%s", msg)

    def statusUnfollow(self, msg: StatusUnfollowMsg):
        self.logger.debug("receive status_unfollow:%s", msg)

    def statusUpdate(self, msg: StatusUpdateMsg):
        self.logger.debug("receive status_update:%s", msg)

    def streamData(self, msg: StreamDataMsg):
        self.logger.debug("receive stream_data:%s", msg)

    def streamPresenceEvent(self, msg: StreamPresenceEventMsg):
        self.logger.debug("receive stream_presence_event:%s", msg)

    def ping(self, msg: PingMsg):
        self.logger.debug("receive ping:%s", msg)

    def pong(self, msg: PongMsg):
        self.logger.debug("receive pong:%s", msg.to_json())

    def party(self, msg: PartyMsg):
        self.logger.debug("receive party:%s", msg)

    def partyCreate(self, msg: PartyCreateMsg):
        self.logger.debug("receive party_create:%s", msg)

    def partyJoin(self, msg: PartyJoinMsg):
        self.logger.debug("receive party_join:%s", msg)

    def partyLeave(self, msg: PartyLeaveMsg):
        self.logger.debug("receive party_leave:%s", msg)

    def partyPromote(self, msg: PartyPromoteMsg):
        self.logger.debug("receive party_promote:%s", msg)

    def partyLeader(self, msg: PartyLeaderMsg):
        self.logger.debug("receive party_leader:%s", msg)

    def partyAccept(self, msg: PartyAcceptMsg):
        self.logger.debug("receive party_accept:%s", msg)

    def partyRemove(self, msg: PartyRemoveMsg):
        self.logger.debug("receive party_remove:%s", msg)

    def partyClose(self, msg: PartyCloseMsg):
        self.logger.debug("receive party_close:%s", msg)

    def partyJoinRequestList(self, msg: PartyJoinRequestsMsg):
        self.logger.debug("receive party_join_request_list:%s", msg)

    def partyJoinRequest(self, msg: PartyJoinRequestMsg):
        self.logger.debug("receive party_join_request:%s", msg)

    def partyMatchmakerAdd(self, msg: PartyMatchmakerAddMsg):
        self.logger.debug("receive party_matchmaker_add:%s", msg)

    def partyMatchmakerRemove(self, msg: PartyMatchmakerRemoveMsg):
        self.logger.debug("receive party_matchmaker_remove:%s", msg)

    def partyMatchmakerTicket(self, msg: PartyMatchmakerTicketMsg):
        self.logger.debug("receive party_matchmaker_ticket:%s", msg)

    def partyData(self, msg: PartyDataMsg):
        self.logger.debug("receive party_data:%s", msg)

    def partyDataSend(self, msg: PartyDataSendMsg):
        self.logger.debug("receive party_data_send:%s", msg)

    def partyPresenceEvent(self, msg: PartyPresenceEventMsg):
        self.logger.debug("receive party_presence_event:%s", msg)
