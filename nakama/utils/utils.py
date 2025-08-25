#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/5/21 16:05
# @Author Tudou <244395692@qq.com>
# @file   utils.py
# @desc   utils.py
import base64

from nakama.common.nakama import Envelope, SessionResponse


def GetErrEnvelope(errMsg: dict) -> Envelope:
    return Envelope().from_dict({
        "error": errMsg
    })


def GetRpcHeaders(serverKey: str) -> dict:
    return {"Authorization": f"Basic {base64.b64encode(serverKey.encode()).decode()}"}
