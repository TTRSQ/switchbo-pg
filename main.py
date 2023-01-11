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


"""
下記のコードでやっていること
- デバイス一覧から湿度計のIDを取得
- 取得したIDを用いて湿度計から湿度や気温の値を取得
- アプリで作成したシーン一覧を取得
- 必要なシーンを名前で絞り込んで実行
"""

devices = request_bot_api("/v1.1/devices", Method.GET)["body"]["deviceList"]
remote_devices = request_bot_api("/v1.1/devices", Method.GET)["body"][
    "infraredRemoteList"
]

# 湿度計のidを取得
meter_plus_device_id = ""
for device in devices:
    if device["deviceType"] == "MeterPlus":
        meter_plus_device_id = device["deviceId"]
        break

print(meter_plus_device_id)
print(request_bot_api(f"/v1.1/devices/{meter_plus_device_id}/status", Method.GET))
scenes = request_bot_api("/v1.1/scenes", Method.GET)["body"]

# 加湿器をコントロールするsceneの取得
humidifier_on_scene_id = ""
humidifier_off_scene_id = ""
for scene in scenes:
    if scene["sceneName"] == "加湿器ON":
        humidifier_on_scene_id = scene["sceneId"]
    if scene["sceneName"] == "加湿器OFF":
        humidifier_off_scene_id = scene["sceneId"]

print(humidifier_on_scene_id)
print(humidifier_off_scene_id)

# 加湿器をONにする
print(request_bot_api(f"/v1.1/scenes/{humidifier_on_scene_id}/execute", Method.POST))

time.sleep(60)
# 加湿器をOFFにする
print(request_bot_api(f"/v1.1/scenes/{humidifier_off_scene_id}/execute", Method.POST))
