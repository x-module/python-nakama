# -*- coding: utf-8 -*-
from nakama.common.common import Common
from nakama.common.nakama import SessionResponse


async def get_request(common: Common, uri, params=None):
    url_path = common.http_url + uri
    resp = await common.http_session.get(url_path, params=params, headers=common.auth_header)
    return await resp.json()


async def post_request(common: Common, uri, params=None, body=None):
    url_path = common.http_url + uri
    result = await common.http_session.post(url_path, params=params, json=body, headers=common.auth_header)
    return await result.json()

async def put_request(common: Common, uri, params=None, body=None):
    url_path = common.http_url + uri
    result = await common.http_session.put(url_path, params=params, json=body, headers=common.auth_header)
    return await result.json()


async def link(common: Common, uri, body):
    url_path = common.http_url + uri
    result = await common.http_session.post(url_path, json=body, headers=common.auth_header)
    return await result.json()


async def authenticate(common: Common, uri, params, body, vars=None):
    if vars:
        body["vars"] = vars
    result = await post_request(common, uri, params, body)
    session = SessionResponse()
    session.from_dict(result)
    common.session = session
    return session
