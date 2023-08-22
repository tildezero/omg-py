from .api import API
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

class Session:
	def __init__(self, api: API, email: str, session_id: str, user_agent: int, created_ip: str, created_on: int, expires_on: int) -> None:

		self._api = api
		self.session_id = session_id
		self.user_agent = user_agent
		self.created_ip = created_ip
		self.created_on = datetime.fromtimestamp(float(created_on))
		self.expires_on = datetime.fromtimestamp(float(expires_on))
		self.email = email

	def delete(self) -> None:
		self._api.request(f'/account/{self.email}/sessions/{self.session_id}', method='DELETE')

@dataclass
class Address:
	address: str
	registration_time: datetime
	expiration: Optional[datetime]
	expired: bool
	preferences: dict
	will_expire: bool


class Account:
	def __init__(self, api: API, email: str) -> None:
		self.api = api
		self.email = email

		r = self.api.request(
			f'/account/{self.email}/info'
		)

		self.created: datetime = datetime.fromtimestamp(float(r['response']['created']['unix_epoch_time']))
		self._settings: dict = r['response']['settings']
		self._name: str = r['response']['name']
		self._sessions = None

	@property
	def settings(self) -> dict:
		return self._settings

	@settings.setter
	def set_settings(self, new_settings: dict) -> dict:
		r = self.api.request(
			f'/account/{self.email}/settings',
			method='POST',
			body=new_settings
		)
		self._settings = new_settings
		return new_settings

	@property
	def addresses(self) -> List[Address]:
		r = self.api.request(
			f'/account/{self.email}/addresses'
		)
		return [
			Address(
				address=x['address'],
				registration_time=datetime.fromtimestamp(float(x['registration']['unix_epoch_time'])),
				will_expire=x['expiration']['will_expire'],
				expired=x['expiration']['expired'],
				expiration=datetime.fromtimestamp(x['expiration'].get("unix_epoch_time", None)) or None,
				preferences=x['preferences']
			) for x in r['response']
		]

	@property
	def name(self) -> str:
		return self._name

	@name.setter
	def set_name(self, new_name: str) -> str:
		r = self.api.request(
			f'/account/{self.email}/name',
			method='POST',
			body={"name": new_name}
		)
		self._name = r['response']['name']
		return r['response']['name']

	@property
	def sessions(self) -> List[Session]:
		r = self.api.request(
			f'/account/{self.email}/sessions'
		)

		lst = [Session(**x, api=self.api, email=self.email) for x in r['response']]
		self._sessions = lst
		return lst



