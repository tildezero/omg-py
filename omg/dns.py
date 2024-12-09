from .api import API
from typing import Optional, List
from datetime import datetime
import dateutil.parser

class DNSRecord:
    def __init__(self, record_id: str, type: str, name: str, data: str, priority: Optional[str], ttl: str, created_at: datetime, updated_at: datetime, api: API, address: str) -> None:
        self._api = api
        self.record_id = record_id
        self.type = type
        self.name = name
        self.data = data
        self.priority = priority
        self.ttl = ttl
        self.created_at = created_at
        self.updated_at = updated_at
        self.address = address

    def edit(self, new_record_type: Optional[str] = None, new_name: Optional[str] = None, new_data: Optional[str] = None):
        r = self._api.request(
            f'/address/{self.address}/dns/{self.record_id}',
            'PATCH',
            # self.name[:-1 * len(self.address + 1)] is used since the name field has your username in the address as well (eg test.suhas)
            # so this filters that out so it doesnt keep adding the username to the end
            {"type": new_record_type or self.type, "name": new_name or self.name[:-1 * (len(self.address) + 1)], "data": new_data or self.data}
        )

        new_rec = r['response']['response_received']['data']

        self.name = new_rec['name']
        self.data = new_rec['data']
        self.ttl = new_rec['ttl']
        self.priority = new_rec['priority']
        self.type = new_rec['type']
        self.created_at = dateutil.parser.isoparse(new_rec['created_at'])
        self.updated_at = dateutil.parser.isoparse(new_rec['updated_at'])

    def delete(self):
        r = self._api.request(
            f'/address/{self.address}/dns/{self.record_id}',
            'DELETE'
        )


class DNSRequestor:
    def __init__(self, api: API, default_username: str) -> None:
        self.api = api
        self.default_username = default_username

    def retrieve(self, address: Optional[str] = None) -> List[DNSRecord]:
        un = address or self.default_username
        r = self.api.request(
            f'/address/{un}/dns'
        )
        return [ DNSRecord(
                record_id=x['id'],
                type=x['type'],
                name=x['name'],
                data=x['data'],
                priority=x['priority'],
                ttl=x['ttl'],
                created_at=dateutil.parser.isoparse(x['created_at']),
                updated_at=dateutil.parser.isoparse(x['updated_at']),
                api=self.api,
                address=un
            ) for x in r['response']['dns'] ]

    def create(self, record_type: str, name: str, data: str, address: Optional[str] = None) -> DNSRecord:
        un = address or self.default_username
        r = self.api.request(
            f'/address/{un}/dns',
            'POST',
            {"type": record_type, "name": name, "data": data}
        )
        rec = r['response']['response_received']['data']
        return DNSRecord(record_id=rec['id'], type=rec['type'], name=rec['name'],
                         data=rec['content'], ttl=rec['ttl'], priority=rec['priority'],
                         created_at=dateutil.parser.isoparse(rec['created_at']),
                         updated_at=dateutil.parser.isoparse(rec['updated_at']), api=self.api, address=un)


