from .api import API
from dataclasses import dataclass
from typing import List

@dataclass
class ServiceInfo:
	members: int
	addresses: int
	profiles: int

class ServiceRequestor:
	def __init__(self, api: API) -> None:
		self.api = api

	def info(self) -> dict:
		r = self.api.noauth_request('/service/info')
		resp = r['response']
		return ServiceInfo(members=resp['members'], addresses=resp['addresses'], profiles=resp['profiles'])

	def directory(self) -> List[str]:
		r = self.api.noauth_request('/directory')
		return r['response']['directory']
