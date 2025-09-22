# -*- coding: utf-8 -*-
import time

from nakama.common.nakama import Envelope


class RequestWaiter:

    def __init__(self):
        self.res: Envelope = None

    def result(self):
        while not self.res:
            time.sleep(0.01)
        return self.res

class RequestHandler:
    def __init__(self):
        self.cidCount = 0
        self.requests = {}
        self.results = {}

    def getCid(self) -> int:
        if len(self.requests.keys()) == 0:
            self.cidCount = 0
        self.cidCount += 1
        return self.cidCount

    def addRequest(self, cid: str, request: RequestWaiter):
        res = self.results.get(cid)
        if res is None:
            self.requests[cid] = request
        else:
            request.res = res
            del self.results[cid]

    def handleResult(self, cid: str, result):
        waiter = self.requests[cid]
        if waiter is None:
            self.results[cid] = result
        else:
            waiter.res = result
            del self.requests[cid]


requestHandler = RequestHandler()
