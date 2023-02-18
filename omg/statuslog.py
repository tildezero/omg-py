from .api import API
from datetime import datetime

class Status:
    def __init__(self, id: str, emoji: str, content: str, created: str, api: API, address: str) -> None:
        self._api = api
        self.emoji = emoji
        self.content = content
        self.created = datetime.fromtimestamp(int(created))
        self.address = address

    def update(self, emoji: str, content: str):
        pass

class StatuslogRequestor:
    def __init__(self, api: API, default_username: str) -> None:
        self.api: API = api
        self.default_username: str = default_username

    def retrieve(self, address: str = None, id: str) -> Status:
        un = address or self.default_username
        r = self.api.noauth_request(
            f"/address/{un}/statuses/{id}"
        )
        return Status(**r['response']['status'], api=self.api)
