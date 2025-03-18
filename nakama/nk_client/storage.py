# -*- coding: utf-8 -*-
from nakama.common.common import Common
from nakama.common.nakama import StorageObjectsRequest, DeleteStorageObjectsRequest, WriteStorageObjectsRequest, ReadStorageObjectsRequest, StorageObjectsResponse, ReadStorageObjectsResponse, WriteStorageObjectsResponse
from nakama.utils.helper import post_request, get_request, put_request


class Storage:
    def __init__(self, common: Common):
        self._common = common

    async def list(self, req: StorageObjectsRequest) -> StorageObjectsResponse:
        params = {
            'user_id': req.user_id or 'null'
        }
        if req.limit is not None:
            params['limit'] = req.limit
        if req.cursor is not None:
            params['cursor'] = req.cursor

        uri = '/v2/storage/%s' % req.collection
        result = await get_request(common=self._common, uri=uri, params=params)
        response = StorageObjectsResponse()
        response.from_dict(result)
        return response

    async def delete(self, req: DeleteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        body = {
            'objectIds': req.object_ids
        }
        result = await put_request(common=self._common, uri='/v2/storage/delete', body=body)
        response = WriteStorageObjectsResponse()
        response.from_dict(result)
        return response

    async def write(self, req: WriteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        body = {
            'objects': req.objects
        }
        result = await put_request(common=self._common, uri='/v2/storage', body=body)
        response = WriteStorageObjectsResponse()
        response.from_dict(result)
        return response

    async def read(self, req: ReadStorageObjectsRequest) -> ReadStorageObjectsResponse:
        body = {
            'objectIds': req.object_ids
        }
        result = await post_request(common=self._common, uri='/v2/storage', body=body)
        response = ReadStorageObjectsResponse()
        response.from_dict(result)
        return response
