from .api import API


class Purl:
    def __init__(self, api: API, default_username) -> None:
        self.api: API = api
        self.default_username = default_username

    def retrieve(self, purl, address=None) -> str:
        r = self.api.request(f"/address/{address}/purl/{purl}")
        return r['response']
