# -*- coding: utf-8 -*-
from nakama.common.nakama import LeaderboardRecordsRequest, LeaderboardRecordsResponse, WriteLeaderboardRecordRequest, Envelope
from nakama.inter.nakama_client_inter import WriteLeaderboardRecordResponse


class Leaderboard:
    def __init__(self, client):
        self._client = client

    def get(self, params: LeaderboardRecordsRequest) -> LeaderboardRecordsResponse:
        endpoint = '/v2/leaderboard/%s' % params.leaderboard_id
        result = self._client.request(method="GET", endpoint=endpoint, params=params.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return LeaderboardRecordsResponse().from_dict(result)

    def write(self, params: WriteLeaderboardRecordRequest) -> WriteLeaderboardRecordResponse:
        endpoint = '/v2/leaderboard/%s' % params.leaderboard_id
        result = self._client.request(method="POST", endpoint=endpoint, payload=payload.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return WriteLeaderboardRecordResponse().from_dict(result)
