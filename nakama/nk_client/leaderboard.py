# -*- coding: utf-8 -*-
from nakama.common.common import Common
from nakama.common.nakama import StorageObjectsRequest, DeleteStorageObjectsRequest, WriteStorageObjectsRequest, ReadStorageObjectsRequest, StorageObjectsResponse, ReadStorageObjectsResponse, WriteStorageObjectsResponse, LeaderboardRecordsRequest, LeaderboardRecordsResponse, WriteLeaderboardRecordRequest
from nakama.nk_client.interface.nakama_client_inter import WriteLeaderboardRecordResponse
from nakama.utils.helper import post_request, get_request, put_request


class Leaderboard:
    def __init__(self, common: Common):
        self._common = common

    async def get_records(self, req: LeaderboardRecordsRequest) -> LeaderboardRecordsResponse:
        params = {}
        if req.owner_ids is not None:
            params['owner_ids'] = req.owner_ids
        if req.limit is not None:
            params['limit'] = req.limit
        if req.expiry is not None:
            params['expiry'] = req.expiry
        if req.cursor is not None:
            params['cursor'] = req.cursor

        uri = '/v2/leaderboard/%s' % req.leaderboard_id
        result = await get_request(common=self._common, uri=uri, params=params)
        response = LeaderboardRecordsResponse()
        response.from_dict(result)
        return response

    async def write_record(self, req: WriteLeaderboardRecordRequest) -> WriteLeaderboardRecordResponse:
        body = {
            'score': req.record.score
        }
        if req.record.subscore is not None:
            body['subscore'] = req.record.subscore
        if req.record.operator is not None:
            body['operator'] = req.record.operator
        if req.record.metadata is not None:
            body['metadata'] = req.record.metadata

        uri = '/v2/leaderboard/%s' % req.leaderboard_id
        result = await post_request(common=self._common, uri=uri, body=body)
        response = WriteLeaderboardRecordResponse()
        response.from_dict(result)
        return response
