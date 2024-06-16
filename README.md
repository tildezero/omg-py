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

note: i think every api path is implemented, feel free to create an issue if i'm missing something though
