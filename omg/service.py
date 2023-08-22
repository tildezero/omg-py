from .api import API
from dataclasses import dataclass

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
