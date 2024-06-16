from .api import API
from typing import Optional, List, Dict, Any
from datetime import datetime

class WeblogEntry:
    def __init__(self, address: str, location: str, title: str, date: int, type: str, status: str, source: str, body: str, output: str, metadata: str, entry: str, api: Optional[API] = None, relative_date: Optional[str] = None) -> None:
        self.address = address
        self.location = location
        self.title = title
        self.date = datetime.fromtimestamp(date)
        self.type = type
        self.status = status
        self.source = source
        self.body = body
        self.output = output
        self.metadata = metadata
        self.entry = entry
        self.relative_date = relative_date
        self._api = api

    def delete(self) -> None:
        if self._api is None:
            raise Exception('you cannot delete this entry!')
        r = self._api.request(
            f'/address/{self.address}/weblog/delete/{self.entry}',
            'DELETE'
        )

class WeblogRequestor:
    def __init__(self, api: API, default_username: str) -> None:
        self.default_username = default_username
        self.api = api

    def retrieve_all(self, address: Optional[str] = None) -> List[WeblogEntry]:
        un = address or self.default_username
        r = self.api.request(
            f'/address/{un}/weblog/entries'
        )
        return [WeblogEntry(**e) for e in r['response']['entries']]

    def create(self, post_body: str, entry: str, address: Optional[str] = None) -> WeblogEntry:
        un = address or self.default_username
        r = self.api.request(
            f'/address/{un}/weblog/entry/{entry}',
            'POST',
            body=None,
            data=post_body
        )
        return WeblogEntry(**r['response']['entry'], address=un)

    def retrieve_one(self, entry: str, address: Optional[str] = None) -> WeblogEntry:
        un = address or self.default_username
        r = self.api.request(
            f'/address/{un}/weblog/entry/{entry}'
        )
        return WeblogEntry(**r['response']['entry'])

    def retrieve_latest_post(self, address: Optional[str] = None) -> WeblogEntry:
        un = address or self.default_username
        r = self.api.noauth_request(f'/address/{un}/weblog/post/latest')
        return WeblogEntry(**r['response']['post'])

    def retrieve_config(self, address: Optional[str] = None) -> Dict[str, Any]:
        un = address or self.default_username
        r = self.api.request(f'/address/{un}/weblog/configuration')
        return r['response']['configuration']
    
    def update_config(self, config: str, address: Optional[str] = None) -> None:
        un = address or self.default_username
        r = self.api.request(f'/address/{un}/weblog/configuration', method='POST', content=str.encode(config))

    def retrieve_template(self, address: Optional[str] = None) -> str:
        un = address or self.default_username
        r = self.api.request(f'/address/{un}/weblog/template')
        return r['response']['template']
    
    def update_template(self, template: str, address: Optional[str] = None) -> None:
        un = address or self.default_username
        r = self.api.request(f'/address/{un}/weblog/template', method='POST', content=str.encode(template))





