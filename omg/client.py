from .api import API
from .purl import PurlRequestor


class Client:
    def __init__(self, key, email, default_username):
        self.key = key
        self.email = email
        self.default_username = default_username
        self.api = API(key=key, email=email)

    @property
    def purl(self) -> PurlRequestor:
        return PurlRequestor(self.api, self.default_username)
