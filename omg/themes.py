from .api import API
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Theme:
    theme_id: str
    name: str
    created: datetime
    updated: datetime
    author: str
    author_url: str
    version: str
    theme_license: str
    description: str
    preview_css: str
    sample_profile: str



class ThemeRequestor:
    def __init__(self, api: API):
        self.api = api

    def list(self) -> List[Theme]:
        r = self.api.noauth_request('/theme/list')
        themes = [r['response']['themes'][x] for x in r['response']['themes']]
        return [Theme(
            theme_id=theme['id'],
            name=theme['name'],
            created=datetime.fromtimestamp(int(theme['created'])),
            updated=datetime.fromtimestamp(int(theme['updated'])),
            author=theme['author'],
            author_url=theme['author_url'],
            version=theme['version'],
            theme_license=theme['licnese'],
            description=theme['description'],
            preview_css=theme['preview_css'],
            sample_profile=theme['sample_profile']
            ) for theme in themes]

    def theme_info(self, theme_id: str) -> Theme:
        r = self.api.noauth_request(f'/theme/{theme_id}/info')
        theme = r['response']['theme']
        return Theme(
            theme_id=theme['id'],
            name=theme['name'],
            created=datetime.fromtimestamp(int(theme['created'])),
            updated=datetime.fromtimestamp(int(theme['updated'])),
            author=theme['author'],
            author_url=theme['author_url'],
            version=theme['version'],
            theme_license=theme['licnese'],
            description=theme['description'],
            preview_css=theme['preview_css'],
            sample_profile=theme['sample_profile']
        )

    def theme_preview(self, theme_id: str) -> str:
        r = self.api.noauth_request(f'/theme/{theme_id}/preview')
        return r['response']['html']


