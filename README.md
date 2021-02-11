# shiftpsh.com-crawler

This python script crawls available data to regularly update values used by [shiftpsh.com](https://github.com/shiftpsh/shiftpsh.com).

## Run

1. Set API secret (defined [here](https://github.com/shiftpsh/shiftpsh.com)): `nano .env`

```
SHIFTPSH_API_SECRET=<api secret>
```

2. Set API endpoint:  `nano api.py`

```
# ...
SHIFTPSH_API_URL = <api endpoint>
# ...
```


3. `python main.py`
