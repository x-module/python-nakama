# -*- coding: utf-8 -*-
import asyncio
import json

from nakama.common.common import Common
from nakama.common.nakama import Envelope, RpcMsg, PartyCreateMsg, PartyMsg
from nakama.nk_client.request_handler import RequestHandler, RequestWaiter


class Party:
    def __init__(self, common: Common):
        self._common = common

    # client_call rpc
    async def create_party(self, open: bool, max_size: int) -> PartyMsg:
        request_waiter = RequestWaiter()
        request_handler = RequestHandler()
        cid = '%d' % request_handler.get_cid()
        request_handler.add_request(cid, request_waiter)
        params = Envelope(
            party_create=PartyCreateMsg(
                open=open,
                max_size=max_size,
            ),
            cid=str(cid),
        )
        await self._common.socket.send(params.to_json())
        res = await request_waiter
        if "error" in res:
            raise Exception(res["error"])
        result = PartyMsg()
        result.from_dict(res["party"])
        return result
