from .api import API
from .purl import Purl


class Client():
    def __init__(self, key, email, default_username=None):
        self.key = key
        self.email = email
        self.default_username = default_username
        self.api = API(key=key, email=email)

    @property
    def purl(self) -> Purl:
        return Purl(self.api, self.default_username)
