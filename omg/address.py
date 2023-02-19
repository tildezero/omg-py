from api import API
from typing import Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class ExpirationTime(Enum):
	NOT_NEAR_EXPIRATION = 1
	WITHIN_SIX_MONTHS = 2
	SOMETHING_ELSE = 3

@dataclass
class PublicAddressInfo:
	address: str
	registration_time: datetime
	verified: bool
	expiration: ExpirationTime
	expired: bool

@dataclass
class PrivateAddressInfo(PublicAddressInfo):
	expiration: datetime

@dataclass
class ExpirationInfo:
	expired: bool
	expiration_time: ExpirationTime


class AddressRequestor:
	def __init__(self, api: API, default_username: Optional[str]=None) -> None:
		self.api = api
		self.default_username = default_username

	def available(self, address: str) -> bool:
		un = address or self.default_username
		r = self.api.noauth_request(
			f"/address/{un}/availability"
		)
		return r['response']['available']

	def expiration(self, address: str) -> dict:
		un = address or self.default_username
		r = self.api.noauth_request(
			f"/address/{un}/expiration"
		)
		msg = r['response']['message']
		if msg == "This address is not near expiration.":
			return ExpirationInfo(expired=r['response']['expired'], expiration_time=ExpirationTime.NOT_NEAR_EXPIRATION)
		elif msg == "This address expires within the next six months.":
			return ExpirationInfo(expired=r['response']['expired'], expiration_time=ExpirationTime.WITHIN_SIX_MONTHS)
		else:
			return ExpirationInfo(expired=r['response']['expired'], expiration_time=ExpirationTime.SOMETHING_ELSE)

	def public_info(self, address: str) -> PublicAddressInfo:
		un = address or self.default_username
		r = self.api.noauth_request(
			f"/address/{un}/info"
		)
		expiry_dict = {"This address is not near expiration.": ExpirationTime.NOT_NEAR_EXPIRATION, "This address expires within the next six months.": ExpirationTime.WITHIN_SIX_MONTHS}
		rsp = r['response']
		return PublicAddressInfo(
			address=rsp['address'],
			registration_time=datetime.fromtimestamp(float(rsp['registration']['unix_epoch_time'])),
			verified=rsp['verification']['verified'],
			expiration=expiry_dict.get(rsp['expiration']['message'], ExpirationTime.SOMETHING_ELSE),
			expired=rsp['expired'],
		)

	def private_info(self, address: str) -> PrivateAddressInfo:
		un = address or self.default_username
		r = self.api.request(
			f"/address/{un}/info"
		)
		expiry_dict = {"This address is not near expiration.": ExpirationTime.NOT_NEAR_EXPIRATION, "This address expires within the next six months.": ExpirationTime.WITHIN_SIX_MONTHS}
		rsp = r['response']
		return PrivateAddressInfo(
			address=rsp['address'],
			registration_time=datetime.fromtimestamp(float(rsp['registration']['unix_epoch_time'])),
			verified=rsp['verification']['verified'],
			expiration=datetime.fromtimestamp(float(rsp['expiration']['unix_epoch_time'])),
			expired=rsp['expired']
		)
