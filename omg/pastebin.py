from .api import API
from typing import List, Optional
from datetime import datetime


class Paste:
    def __init__(self, title: str, content: str, modified_on: str, counter: int, api: API):
        self._api = api
        self.title = title
        self.content = content
        self.modified_on = datetime.fromtimestamp(modified_on)

    def __str__(self):
        return f"title: {self.title}, content: {self.content}, modified_on: {self.modified_on.timestamp()}"

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
        return Paste(**r["response"]["paste"])

    def retrieve_all(self, address=None) -> List[Paste]:
        un = address or self.default_username
        r = self.api.request(f"/address/{un}/pastebin")
        pastes = r['response']['pastes']
        ls = [Paste(**x) for x in pastes]
        return ls

    def create(self, title, content, address=None) -> Paste:
        un = address or self.default_username
        if title is None:
            raise Exception("Please include a title for the paste!")
        if content is None:
            raise Exception("Please provide the content of the paste!")

        r = self.api.request(
            f"/address/{un}/paste", method="POST", body={'title': title, 'content': content})
        return Paste(
            name=r['response']['title'],
            url=r['response']['content'],
            modified_on=r['response']['modified_on'],
            api=self.api
        )
