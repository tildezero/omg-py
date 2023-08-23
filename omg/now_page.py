from .api import API
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class NowPage:
    content: str
    updated: datetime
    listed: bool

@dataclass
class NowGardenListing:
    address: str
    url: str
    updated: datetime

class NowPageRequestor:
    def __init__(self, api: API, default_username: str):
        self.api = api
        self.default_username = default_username

    def retrieve(self, address: Optional[str] = None) -> NowPage:
        un = address or self.default_username
        r = self.api.noauth_request(
            f'/address/{un}/now'
        )
        return NowPage(content=r['response']['now']['content'],
                       updated=datetime.fromtimestamp(int(r['response']['now']['updated'])),
                       listed=bool(int(r['response']['now']['listed'])))

    def retrieve_now_garden(self) -> List[NowGardenListing]:
        r = self.api.noauth_request(
            '/now/garden'
        )
        return [NowGardenListing(address=x['address'], url=x['url'], updated=datetime.fromtimestamp(int(x['updated']['unix_epoch_time']))) for x in r['response']['garden']]

    def update(self, content: str, listed: bool = True, address: Optional[str] = None):
        un = address or self.default_username
        r = self.api.request(
            f'/address/{un}/now',
            'POST',
            {"content": content, "listed": str(int(listed))}
        )
