from .api import API
from typing import List, Optional

class EmailRequestor:
	def __init__(self, api: API, default_username: str):
		self.api = api
		self.default_username = default_username

	def retrieve_addresses(self, address: Optional[str] = None) -> List[str]:
		un = address or self.default_username
		r = self.api.request(
			f'/address/{un}/email'
		)
		return r['response']['destination_array']

	def set_addresses(self, new_addresses: List[str], address: Optional[str] = None) -> List[str]:
		un = address or self.default_username
		r = self.api.request(
			f'/address/{un}/email',
			'POST',
			{"destination": ", ".join(new_addresses)}
		)
		return r['response']['destination_array']

