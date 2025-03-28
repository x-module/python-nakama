# -*- coding: utf-8 -*-
from nakama.common.decorator import singleton
from nakama.common.nakama import Envelope


class RequestWaiter:

    def __init__(self):
        self.res:Envelope = None

    def __await__(self)->Envelope:
        while self.res is None:
            yield
        return self.res


@singleton
class RequestHandler:
    def __init__(self):
        self.cid_count = 0
        self.requests = {}
        self.results = {}

    def get_cid(self) -> int:
        if len(self.requests.keys()) == 0:
            self.cid_count = 0
        self.cid_count += 1
        return self.cid_count

    def add_request(self, cid: str, request: RequestWaiter):
        res = self.results.get(cid)
        if res is None:
            self.requests[cid] = request
        else:
            request.res = res
            del self.results[cid]

    def handle_result(self, cid: str, result):
        waiter = self.requests[cid]
        if waiter is None:
            self.results[cid] = result
        else:
            waiter.res = result
            del self.requests[cid]
