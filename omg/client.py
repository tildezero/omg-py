from .api import API
from .purl import PurlRequestor
from .pastebin import PasteBinRequestor
from .statuslog import StatuslogRequestor
from typing import Optional


class Client:
    def __init__(self, key: Optional[str]=None, email: Optional[str]=None, default_username=None):
        self.key = key
        self.email = email
        self.default_username = default_username
        self.api = API(key=key, email=email)

    @property
    def purl(self) -> PurlRequestor:
        return PurlRequestor(self.api, self.default_username)

    @property
    def pastebin(self) -> PasteBinRequestor:
        return PasteBinRequestor(self.api, self.default_username)

    @property
    def statuslog(self) -> StatuslogRequestor:
        return StatuslogRequestor(self.api, self.default_username)

    @property
    def service(self) -> ServiceRequestor:
        return ServiceRequestor(self.api)
