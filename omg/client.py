from .api import API
from .purl import PurlRequestor
from .pastebin import PasteBinRequestor
from .statuslog import StatuslogRequestor
from .service import ServiceRequestor
from .address import AddressRequestor
from .account import Account
from .dns import DNSRequestor
from typing import Optional


class Client:
    def __init__(self, default_username: str, key: Optional[str]=None, email: Optional[str]=None):
        if not default_username:
            raise ValueError("you must provide a default username to use! (If you know you will be adding a username to every request, just put some gibberish in/a blank string)")
        self.default_username = default_username
        self.key = key
        self.email = email
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

    @property
    def address(self) -> AddressRequestor:
        return AddressRequestor(self.api, self.default_username)

    @property
    def account(self) -> Account:
        if not self.email:
            raise Exception("You need an email parameter to use this class!")
        return Account(self.api, self.email)

    @property
    def dns(self) -> DNSRequestor:
        return DNSRequestor(self.api, self.default_username)

