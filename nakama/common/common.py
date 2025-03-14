# -*- coding: utf-8 -*-
import base64
import json
import re

import aiohttp

JWT_REG = re.compile('^([A-Za-z0-9-_=]+)\.([A-Za-z0-9-_=]+)\.?([A-Za-z0-9-_.+/=]*)$')


class Common:
    def __init__(self, http_url, server_key: str):
        self._auth_header = None
        self.expires = None
        self.user_id = None
        self.vars = None
        self.username = None
        self._token = None
        self._http_url = http_url
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self._http_session = aiohttp.ClientSession(headers=headers)
        self.set_basic(server_key)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self.set_token(token)

    def set_token(self, token):
        p1, p2, p3 = JWT_REG.match(token).groups()
        assert p1 and p2 and p3, 'JWT is not valid'

        p2 = p2.encode()
        pad = len(p2) % 4
        p2 += b"=" * pad  # correct padding
        decoded_token = json.loads(base64.b64decode(p2))

        self._token = token
        self.expires = decoded_token['exp']
        self.username = decoded_token['usn']
        self.user_id = decoded_token['uid']
        self.vars = decoded_token.get('vrs')

        self._auth_header = {
            'Authorization': 'Bearer %s' % token
        }

    def set_basic(self, server_key: str):
        server_key = '%s:' % server_key
        self._auth_header = {
            'Authorization': 'Basic %s' % base64.b64encode(server_key.encode()).decode()
        }

    @property
    def http_url(self):
        return self._http_url

    @property
    def http_session(self):
        return self._http_session

    @property
    def auth_header(self):
        return self._auth_header