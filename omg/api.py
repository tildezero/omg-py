import httpx
from .constants import API_URL
from httpx import Client

class API:
    def __init__(self, key, email):
        self.http: Client = httpx.Client(base_url=API_URL)
        self.key = key
        self.email = email

    def request(self, path, method="GET", body=None):
        req = self.http.request(
            method=method,
            url=path,
            json=body,
            headers={
                "Authorization": f"Bearer {self.key}"
            }
        )

        return req.json()
