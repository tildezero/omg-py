from .api import API
from typing import Optional, IO
from datetime import datetime
from urllib.parse import quote_plus


class WebPage:
    def __init__(
        self,
        address: str,
        content: str,
        page_type: str,
        theme: str,
        css: str,
        head: str,
        verified: int,
        pfp: str,
        metadata: str,
        branding: str,
        modified: str,
        api: API,
    ):
        pass
        self._address = address
        self._api = api
        self.content = content
        self.page_type = page_type
        self.theme = theme
        self.css = css
        self.head = head
        self.verified: bool = bool(verified)
        self.pfp = pfp
        self.metadata = metadata
        self.branding = branding
        self.modified: datetime = datetime.fromtimestamp(int(modified))

    def update(self, content: str, publish: bool = True) -> None:
        r = self._api.request(
            f"/address/{self._address}/web",
            "POST",
            {"publish": publish, "content": content},
        )
        self.content = content
        self.modified = datetime.now()


class WebPageRequestor:
    def __init__(self, api: API, default_username: str):
        self.api = api
        self.default_username = default_username

    def retrieve(self, address: Optional[str] = None) -> WebPage:
        un = address or self.default_username
        r = self.api.request(f"/address/{un}/web")
        pg = r["response"]
        return WebPage(
            address=un,
            **pg,
            api=self.api
        )

    # UNTESTED
    def upload_pfp(self, pfp: IO, address: Optional[str] = None) -> None:
        un = address or self.default_username
        img = quote_plus(pfp.read())
        r = self.api.http.post(
            f"/address/{un}/pfp",
            headers={"Authorization": f"Bearer {self.api.key}"},
            content=img.encode(),
        )
