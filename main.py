import time
import hashlib
import hmac
import base64
import httpx
import os
from enum import Enum

API_TOKEN = os.getenv("API_TOKEN")
API_SECRET = os.getenv("API_SECRET")
BOT_API_HOST = "https://api.switch-bot.com"


def create_auth_headers():
    token = API_TOKEN
    secret = API_SECRET

    nonce = ""
    t = int(round(time.time() * 1000))
    string_to_sign = "{}{}{}".format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, "utf-8")
    secret = bytes(secret, "utf-8")

    sign = base64.b64encode(
        hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
    )

    return {
        "Authorization": token,
        "t": str(t),
        "sign": str(sign, "utf-8"),
        "nonce": nonce,
    }


class Method(Enum):
    GET = 1
    POST = 2


def request_bot_api(path: str, method: Method, param: dict = {}):
    headers = create_auth_headers()
    res = None
    if method == Method.GET:
        res = httpx.get(BOT_API_HOST + path, headers=headers, params=param)
    elif method == Method.POST:
        headers["Content-Type"] = "application/json; charset=utf8"
        res = httpx.post(BOT_API_HOST + path, headers=headers, json=param)
    return res.json()


resp = request_bot_api("/v1.1/devices", Method.GET)
devices = resp["body"]["deviceList"]
for device in devices:
    print(device)
