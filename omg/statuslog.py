from .api import API
from datetime import datetime
from typing import Optional, List
from emoji import is_emoji
import time

class Status:
    def __init__(self, status_id: str, emoji: str, content: str, created: str, api: API, address: str, external_url: Optional[str]=None) -> None:
        self._api = api
        self.emoji = emoji
        self.content = content
        self.created = datetime.fromtimestamp(int(created))
        self.address = address
        self.status_id = status_id
        self.external_url = external_url


    def update(self, emoji: str, content: str):
        if not is_emoji(emoji):
            raise ValueError("emoji must be an emoji!")
        if len(emoji) > 1:
            raise ValueError("emoji must be exactly 1 valid emoji!")
        if len(content) < 2:
            raise ValueError("content must be greater than 1")
        self._api.request(
            path=f"/address/{self.address}/statuses",
            body={"id": self.status_id, "emoji": emoji, "content": content},
            method="PATCH"
        )

class StatusBio:
    def __init__(self, bio: str, css: str, address: str, api: API):
        self.bio = bio
        self.css = css
        self.address = address,
        self._api = api

    def update(self, new_bio: str):
        self._api.request(
            path=f"/address/{self.address}/statuses/bio",
            method="POST",
            body={"content": new_bio}
        )

class StatuslogRequestor:
    def __init__(self, api: API, default_username: str) -> None:
        self.api: API = api
        self.default_username: str = default_username

    def retrieve(self, status_id: str, address: Optional[str] = None) -> Status:
        un = address or self.default_username
        r = self.api.noauth_request(
            f"/address/{un}/statuses/{status_id}"
        )
        resp = r['response']['status']
        return Status(
            status_id=resp['id'],
            emoji=resp['emoji'],
            content=resp['content'],
            created=resp['created'],
            external_url=resp['external_url'],
            api=self.api,
            address=un
        )

    def retrieve_all(self, address: Optional[str] = None) -> List[Status]:
        un = address or self.default_username
        r = self.api.noauth_request(
            f"/address/{un}/statuses"
        )
        lst = [ Status(
            status_id=resp['id'],
            emoji=resp['emoji'],
            content=resp['content'],
            created=resp['created'],
            external_url=resp['external_url'],
            api=self.api,
            address=un
        ) for resp in r['response']['statuses'] ]
        return lst

    def share(self, emoji: str, content: str, external_url: Optional[str] = None, address: Optional[str]=None) -> Status:
        if not is_emoji(emoji):
            raise ValueError("emoji must be an emoji!")
        if len(emoji) > 1:
            raise ValueError("emoji must be exactly 1 valid emoji!")
        if len(content) < 2:
            raise ValueError("content must be greater than 1")
        un = address or self.default_username
        r = self.api.request(
            f"/address/{un}/statuses",
            method="POST",
            body={
                "emoji": emoji,
                "content": content,
                "external_url": external_url
            }
        )

        return Status(
            status_id=r['response']['id'],
            emoji=emoji,
            content=content,
            external_url=external_url,
            created=str(int(time.time())),
            api=self.api,
            address=un
        )

    def share_single_string(self, status: str, external_url: Optional[str], address: Optional[str] = None) -> Status:
        if not is_emoji(status[0]):
            raise ValueError("the first character of the status must be an emoji!")

        return self.share(
            emoji=status[0],
            content=status[1:],
            external_url=external_url,
            address=address
        )

    def retrieve_bio(self, address: str) -> StatusBio:
        un = address or self.default_username
        r = self.api.request(
            path=f"/address/{un}/statuses/bio"
        )
        return StatusBio(bio=r['response']['bio'], css=r['response']['css'], address=un, api=self.api)

    def retrieve_entire_statuslog(self) -> List[Status]:
        r = self.api.noauth_request('/statuslog')
        return [ Status(
            status_id=resp['id'],
            emoji=resp['emoji'],
            content=resp['content'],
            created=resp['created'],
            address=resp['address'],
            api=self.api,
        ) for resp in r['response']['statuses'] ]

    def retrieve_entire_latest(self) -> List[Status]:
        r = self.api.noauth_request('/statuslog/latest')
        return [ Status(
            status_id=resp['id'],
            emoji=resp['emoji'],
            content=resp['content'],
            created=resp['created'],
            address=resp['address'],
            api=self.api,
        ) for resp in r['response']['statuses'] ]
