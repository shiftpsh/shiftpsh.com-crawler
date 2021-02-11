from decouple import config
import requests

SHIFTPSH_API_URL = "https://shiftpsh.com/api/table/set_single"


def update(key, value):
    print(f"Requesting update: {key} <- {value}")
    r = requests.post(SHIFTPSH_API_URL, data={"key": key, "value": value},
                  headers={"shiftpsh-secret": config("SHIFTPSH_API_SECRET")})
    return r
