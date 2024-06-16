from typing import IO, Optional
from .api import API
from base64 import b64encode

class Pic:
    def __init__(self, pic_id: str, size: int, mime: str, url: str, some_pics_url: str, api: API, un: str):
        self.pic_id = pic_id
        self.size = size
        self.mime = mime
        self.url = url
        self.some_pics_url = some_pics_url
        self._api = api
        self._un = un
    
    def set_description(self, description: str) -> None:
        r = self._api.request(f'/address/{self._un}/pics/{self.pic_id}', method='POST', body={'description': description})

class PicsRequestor:
    def __init__(self, api: API, default_username: str):
        self.default_username = default_username
        self.api = api
    
    def upload(self, pic: IO, address: Optional[str] = None) -> Pic:
        un = address or self.default_username
        pic_data = pic.read()
        base64_pic = b64encode(pic_data)
        r = self.api.request(
            f'/address/{un}/pics/upload',
            method='POST',
            body={'pic': base64_pic.decode()} 
        )
        pd = r['response']
        return Pic(pic_id=pd['id'], size=pd['size'], mime=pd['mime'], url=pd['url'], some_pics_url=pd['some_pics_url'], api=self.api, un=un)

