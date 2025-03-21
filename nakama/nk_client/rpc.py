# -*- coding: utf-8 -*-
import asyncio
import json

from nakama.common.common import Common
from nakama.common.nakama import Envelope, RpcMsg
from nakama.nk_client.request_handler import RequestHandler, RequestWaiter


# RPC 调用
class RPC:
    def __init__(self, common: Common):
        self._common = common

    # client_call rpc
    async def client_call(self, func_id, **kwargs):
        assert self._common is not None, "The current account is not logged in, please log in first"
        url_path = self._common.http_url + '/v2/rpc/' + func_id
        result = await self._common.http_session.post(url_path, json=json.dumps(kwargs), headers=self._common.auth_header)
        return await result.json()

    # client_call rpc
    async def socket_call(self, id, **kwargs):
        request_waiter = RequestWaiter()
        request_handler = RequestHandler()
        cid = '%d' % request_handler.get_cid()
        request_handler.add_request(cid, request_waiter)

        kwargs["playerId"] = self._common.user_id
        params = Envelope(
            rpc=RpcMsg(
                id=id,
                payload=json.dumps(kwargs),
            ),
            cid=str(cid),
        )
        await self._common.socket.send(params.to_json())
        res = await request_waiter
        if "error" in res:
            raise Exception(res["error"])

        result = Envelope()
        result.from_dict(res)
        return result.rpc.payload
