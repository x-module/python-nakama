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
from nakama.socket.notice import BaseNoticeHandler
from nakama.utils.logger import Logger


class NoticeHandler(BaseNoticeHandler):
    def __init__(self):
        super(NoticeHandler, self).__init__()
        self.logger = Logger(__name__)

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
