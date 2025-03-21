# -*- coding: utf-8 -*-
class RequestWaiter:

    def __init__(self):
        self.res = None

    def __await__(self):
        while self.res is None:
            yield
        return self.res


class RequestHandler:
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RequestHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

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
