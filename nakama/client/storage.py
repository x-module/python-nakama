# -*- coding: utf-8 -*-
from nakama.common.nakama import StorageObjectsRequest, DeleteStorageObjectsRequest, WriteStorageObjectsRequest, ReadStorageObjectsRequest, StorageObjectsResponse, ReadStorageObjectsResponse, WriteStorageObjectsResponse, Envelope


class Storage:
    def __init__(self, client):
        self._client = client

    def list(self, params: StorageObjectsRequest) -> StorageObjectsResponse:
        endpoint = f'/v2/storage/{params.collection}'
        result = self._client.request(method="GET", endpoint=endpoint, params=params.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return StorageObjectsResponse().from_dict(result)

    def delete(self, params: DeleteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        endpoint = '/v2/storage/delete'
        result = self._client.request(method="PUT", endpoint=endpoint, json=params.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return WriteStorageObjectsResponse().from_dict(result)

    def write(self, params: WriteStorageObjectsRequest) -> WriteStorageObjectsResponse:
        endpoint = '/v2/storage'
        result = self._client.request(method="PUT", endpoint=endpoint, json=params.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return WriteStorageObjectsResponse().from_dict(result)

    def read(self, params: ReadStorageObjectsRequest) -> ReadStorageObjectsResponse:
        endpoint = '/v2/storage'
        result = self._client.request(method="POST", endpoint=endpoint, json=params.to_dict())
        envelope = Envelope().from_dict(result)
        if envelope.error.code != 0:
            raise envelope.error
        return ReadStorageObjectsResponse().from_dict(result)
