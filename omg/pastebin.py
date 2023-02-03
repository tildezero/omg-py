from .api import API
from typing import List, Optional
from datetime import datetime
import time
from math import floor


class Paste:
    def __init__(self, title: str, content: str, modified_on: str, listed: Optional[int], api: API, address: str):
        self._api = api
        self.title = title
        self.content = content
        self.modified_on = datetime.fromtimestamp(int(modified_on))
        self.listed = bool(listed)
        self.address = address

    def __str__(self):
        return f"title: {self.title}, content: {self.content}, modified_on: {self.modified_on.timestamp()}, listed: {bool(self.listed)}"

    def delete(self):
        self._api.request(
            path=f"/address/{self.address}/pastebin/{self.title}",
            method="DELETE"
        )


class PasteBinRequestor:
    def __init__(self, api: API, default_username) -> None:
        self.api: API = api
        self.default_username = default_username

    def retrieve(self, paste: str, address: Optional[str] = None) -> Paste:
        un = address or self.default_username
        if paste is None:
            raise Exception("please include a paste!")
        r = self.api.request(f"/address/{un}/pastebin/{paste}")
        return Paste(**r["response"]["paste"], api=self.api,address=un)

    def retrieve_all(self, address: str=None) -> List[Paste]:
        un = address or self.default_username
        r = self.api.request(f"/address/{un}/pastebin")
        pastes = r['response']['pastebin']
        ls = [Paste(**x, api=self.api,address=un) for x in pastes]
        return ls

    def create(self, title: str, content: str, listed: bool=True, address: Optional[str]=None) -> Paste:
        un = address or self.default_username
        if title is None:
            raise Exception("Please include a title for the paste!")
        if content is None:
            raise Exception("Please provide the content of the paste!")

        r = self.api.request(
            f"/address/{un}/pastebin", method="POST", body={'title': title, 'content': content, 'listed': int(listed)})
        return Paste(
            title=r['response']['title'],
            content=content,
            listed=int(listed),
            modified_on=str(floor(time.time())),
            api=self.api,
            address=un
        )
