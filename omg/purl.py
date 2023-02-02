from .api import API
from typing import List


class Purl:
    def __init__(self, name: str, url: str, address: str, counter: int, api: API):
        self._api = api
        self.name = name
        self.address = address
        self.url = url
        self.counter = counter

    def __str__(self):
        return f"name: {self.name}, address: {self.address}, url: {self.url}"

    def delete(self):
        self._api.request(
            path=f"/address/{self.address}/purl/{self.name}",
            method="DELETE"
        )


class PurlRequestor:
    def __init__(self, api: API, default_username) -> None:
        self.api: API = api
        self.default_username = default_username

    def retrieve(self, purl, address=None) -> Purl:
        un = address or self.default_username
        if purl is None: raise Exception("please include a purl!")
        r = self.api.request(f"/address/{un}/purl/{purl}")
        return Purl(name=r['response']['purl']['name'], url=r['response']['purl']['url'], address=un, api=self.api,
                    counter=r['response']['purl']['counter'])

    def retrieve_all(self, address=None) -> List[Purl]:
        un = address or self.default_username
        r = self.api.request(f"/address/{un}/purls")
        purls = r['response']['purls']
        ls = [Purl(name=x['name'], url=x['url'], address=un, api=self.api, counter=x['counter']) for x in purls]
        return ls

    def create(self, name, url, address=None) -> Purl:
        un = address or self.default_username
        if name is None:
            raise Exception("Please include a name for the purl (the short link)")
        if url is None:
            raise Exception("Please provide a redirect url for the purl!")

        r = self.api.request(f"/address/{un}/purl", method="POST", body={'name': name, 'url': url})
        return Purl(
            name=r['response']['name'],
            url=r['response']['url'],
            counter=0,
            address=un,
            api=self.api
        )
