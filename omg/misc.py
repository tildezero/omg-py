# This file contains API sections that are only 1 endpoint and I thought it would be easier to just put them in 1 file
from .api import API
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus

@dataclass
class AccessToken:
    access_token: str
    token_type: str
    scope: str

class OAuth:
    def __init__(self, api: API):
        self.api = api

    def exchange_auth_code(self, client_id: str, client_secret: str, redirect_uri: str, scope: str, code: Optional[str] = None) -> AccessToken:
        params_array = {"client_id": client_id, "client_secret": client_secret, "redirect_uri": quote_plus(redirect_uri), scope: scope}
        if code is not None:
            params_array['code'] = code
        r = self.api.request(
            '/oauth',
            'GET',
            params=params_array
        )
        return AccessToken(**r)

class Preferences:
    def __init__(self, default_username: str, api: API):
        self.default_username = default_username
        self.api = api

    def save_preference(self, key: str, value: str, address: Optional[str] = None) -> None:
        un = address or self.default_username
        r = self.api.request(
            f'/preferences/{un}',
            'POST',
            body={'item': key, 'value': value}
        )

