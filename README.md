# omg-py
#### an api wrapper for [the omg.lol api](https://api.omg.lol)

## use
```shell
pip install git+https://github.com/tildezero/omg-py.git
```

```python
from omg import Client
client = Client(key="asdf", email="suhas@omg.lol")
client.purl.retrieve("sus")
```

## endpoints that need to be implemented
- exchange an oauth code for an access token
- save a preference
- retrieve weblog entries
- create a weblog entry
- retrieve a weblog entry
- retrieve the latest weblog post
- delete a weblog entry
- retrieve weblog configuration
- update weblog configuration
- retrieve weblog template
- update weblog template
- upload some.pics picture
- set description for some.pics picture

