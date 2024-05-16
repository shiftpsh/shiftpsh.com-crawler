# shiftpsh.com-crawler

This python script crawls available data to regularly update values used by [shiftpsh.com](https://github.com/shiftpsh/shiftpsh.com) (2021).

The 2024 version of the site does not use this crawler; instead, it crawls for data on build time to statically generate needed pages.

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

3. `pip install -r reqirements.txt && python main.py`
