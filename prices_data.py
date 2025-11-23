import requests
import json
import os
import time
import datetime
import urllib.parse
#https://github.com/Revadike/InternalSteamWebAPI/wiki

FILENAME = "prices.json"
LATEST_PRICES_FILE = "latest_prices.json"

PRICE_URL = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="
PRICE_HISTORY_URL = "https://steamcommunity.com/market/pricehistory?appid=730&market_hash_name="

cases = {
    "Gamma Case": {
        "code": "Gamma%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFYznarJJjkQ6ovjw4SPlfP3auqEl2oBuJB1j--WoY322QziqkdpZGr3IteLMlhpw4RJCv8/360fx360f"
    },
    "Falchion Case": {
        "code": "Falchion%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FF8ugPDMIWpAuIq1w4KIlaChZOyFwzgJuZNy3-2T89T0jlC2rhZla2vwIJjVLFHz75yKpg/360fx360f"
    },
    "Huntsman Weapon Case": {
        "code": "Huntsman%20Weapon%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFQu0PaQIm9DtY6wzYaIxKWtN7iJwW8G6Z0h2LqWoY6s2Qy2-0Q_Nzv7IJjVLFGZqUbjlQ/360fx360f"
    },
    "Chroma Case": {
        "code": "Chroma%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFEuh_KQJTtEuI63xIXbxqOtauyClTMEsJV1jruS89T3iQKx_BBqa2j3JpjVLFH1xpp0EQ/360fx360f"
    },
    "Glove Case": {
        "code": "Glove%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFY1naTMdzwTtNrukteIkqT2MO_Uwz5Q6cYhibyXo4rw2ALsrkRoYjuncNCLMlhpEV4XDTk/360fx360f"
    },
    "Revolver Case": {
        "code": "Revolver%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFYwnfKfcG9HvN7iktaOkqD1auLTxD5SvZYgiLvFpo7xjVLh-kdrYWnzcoGLMlhpsyM-5vg/360fx360f"
    },
    "Fracture Case": {
        "code": "Fracture%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU2nfGaJG0btN2wwYHfxa-hY-uFxj4Dv50nj7uXpI7w3AewrhBpMWH6d9CLMlhpEbAe-Zk/360fx360f"
    },
    "Recoil Case": {
        "code": "Recoil%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFQxnaecIT8Wv9rilYTYkfTyNuiFwmhUvpZz3-2Z9oqg0Vew80NvZzuiJdeLMlhpwFO-XdA/360fx360f"
    },
    "Revolution Case": {
        "code": "Revolution%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFQynaHMJT9B74-ywtjYxfOmMe_Vx28AucQj3brAoYrz3Fay_kY4MG_wdYeLMlhpLMaM-1U/360fx360f"
    },
    "Kilowatt Case": {
        "code": "Kilowatt%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFQznaKdID5D6d23ldHSwKOmZeyEz21XvZZ12LzE9t6nigbgqkplNjihJIaLMlhpF1ZeR5c/360fx360f"
    },
    "Gallery Case": {
        "code": "Gallery%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFQ0naTKJjhHu92ywoSIlq_3Zu7Vxm0CuMFwi-2Wpojw0APnqBBuYW31JY6LMlhpMMztXwM/360fx360f"
    },
    "Shadow Case": {
        "code": "Shadow%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FF4u1qubIW4Su4mzxYHbzqGtZ-KGlz8EuJcg3rnE9NiijVe3_UY-Zzr2JJjVLFEEeiQRtg/360fx360f"
    },
    "Spectrum Case": {
        "code": "Spectrum%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFY2nfKadD4U7Y7lwYXexaGlYb3QzjlUvZ0k0ujHptug2VbirkRrNW2md4SLMlhph09hpX0/360fx360f"
    },
    "Winter Offensive Weapon Case": {
        "code": "Winter%20Offensive%20Weapon%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFYu0aKfJz8a793gxNLfzvOkMunUwWgH7JIjj-qW8d7x2VXt_UBuMT3zIpjVLFEGDSGUSQ/360fx360f"
    },
    "Operation Hydra Case": {
        "code": "Operation%20Hydra%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFY3navMJWgQtNm1ldLZzvOiZr-BlToIsZcoi-yTpdutiVW2-Es4NWjwIo-LMlhpinMS53M/360fx360f"
    },
    "Operation Vanguard Weapon Case": {
        "code": "Operation%20Vanguard%20Weapon%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFIuh6rJImVGvtjllYaNka6la7rUxWkE65BzibvD9N7z0Q22-0Fka2GlJ5jVLFHqavWW2g/360fx360f"
    },
    "CS:GO Weapon Case": {
        "code": "CS%3AGO%20Weapon%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsRVx4MwFo5_T3eAQ3i6DMIW0X7ojiwoHax6egMOKGxj4G68Nz3-jCp4itjFWx-ktqfSmtcwqVx6sT/360fx360f"
    },
    "Horizon Case": {
        "code": "Horizon%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUwnfbOdDgavYXukYTZkqf2ZbrTwmkE6scgj7CY94ml3FXl-ENkMW3wctOLMlhpVHKV9YA/360fx360f"
    },
    "Clutch Case": {
        "code": "Clutch%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFY5naqQIz4R7Yjix9bZkvKiZrmAzzlTu5AoibiT8d_x21Wy8hY_MWz1doSLMlhpM3FKbNs/360fx360f"
    },
    "Operation Bravo Case": {
        "code": "Operation%20Bravo%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsXE1xNwVDv7WrFA5pnabNJGwSuN3gxtnawKOlMO6HzzhQucAm0uvFo4n2iw3h_UM-ZmilJNeLMlhpjfjxEoE/360fx360f"
    },
    "Operation Riptide Case": {
        "code": "Operation%20Riptide%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU5narKKW4SvIrhw9PZlaPwNuqAxmgBucNz2L3C8dyj31Xn-0VtMW3wdY6LMlhplna0TPI/360fx360f"
    },
    "Operation Breakout Weapon Case": {
        "code": "Operation%20Breakout%20Weapon%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFMu1aPMI24auITjxteJwPXxY72AkGgIvZAniLjHpon2jlbl-kpvNjz3JJjVLFG9rl1YLQ/360fx360f"
    },
    "Operation Phoenix Weapon Case": {
        "code": "Operation%20Phoenix%20Weapon%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUuh6qZJmlD7tiyl4OIlaGhYuLTzjhVupJ12urH89ii3lHlqEdoMDr2I5jVLFFSv_J2Rg/360fx360f"
    },
    "CS20 Case": {
        "code": "CS20%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU0naHKIj9D7oTgl4LelaGnMuqIwDgFusR337HCpYmhiwzm8ktqMjv2INKLMlhprbp6CTE/360fx360f"
    },
    "Chroma 2 Case": {
        "code": "Chroma%202%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFAuhqSaKWtEu43mxtbbk6b1a77Twm4Iu8Yl3bCU9Imii1Xt80M5MmD7JZjVLFH-6VnQJQ/360fx360f"
    },
    "Spectrum 2 Case": {
        "code": "Spectrum%202%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFY4naeaJGhGtdnmx4Tek_bwY-iFlGlUsJMp3LuTot-mjFGxqUttZ2r3d4eLMlhpnZPxZK0/360fx360f"
    },
    "Prisma 2 Case": {
        "code": "Prisma%202%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU1nfbOIj8W7oWzkYLdlPOsMOmIk2kGscAj2erE99Sn2AGw_0M4NW2hIYOLMlhpcmY0CRM/360fx360f"
    },
    "Prisma Case": {
        "code": "Prisma%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUynfWaI25G6Ijkl9iPw_SnNrjXw2oBu8cj3b2Qo4_33QbnrUdlYD37ddCLMlhpvs0XIz0/360fx360f"
    },
    "Snakebite Case": {
        "code": "Snakebite%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU4naLOJzgUuYqyzIaIxa6jMOLXxGkHvcMjibmU99Sg3Qaw-hA_ZWrzLISLMlhpgJJUhGE/360fx360f"
    },
    "CS:GO Weapon Case 3": {
        "code": "CS%3AGO%20Weapon%20Case%203",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsRVx4MwFo5fSnf15k0KGacG0UtYXnzdTdkq-gariGlDgHvMcmjryZotqg2wCxrUVtfSmtc20v4quI/360fx360f"
    },
    "Operation Broken Fang Case": {
        "code": "Operation%20Broken%20Fang%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU3naeZIWUStYjgxdnewfGmZb6DxW8AupMp27yT9IqiilCxqkRkZGyldoaLMlhp6IQjKcg/360fx360f"
    },
    "CS:GO Weapon Case 2": {
        "code": "CS%3AGO%20Weapon%20Case%202",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsRVx4MwFo5PT8elUwgKKZJmtEvo_kxITZk6StNe-Fz2pTu8Aj3eqVpIqgjVfjrRI9fSmtc1Nw-Kh3/360fx360f"
    },
    "Dreams & Nightmares Case": {
        "code": "Dreams%20%26%20Nightmares%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFQwnfCcJmxDv9rhwIHZwqP3a-uGwz9Xv8F0j-qQrI3xiVLkrxVuZW-mJoWLMlhpWhFkc9M/360fx360f"
    },
    "Shattered Web Case": {
        "code": "Shattered%20Web%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA/360fx360f"
    },
    "Chroma 3 Case": {
        "code": "Chroma%203%20Case",
        "image": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFYynaSdJGhE74y0wNWIw_OlNuvXkDpSuZQmi--SrN-h3gey-Uo6YWmlIoCLMlhplhFFvwI/360fx360f"
    },
    "Danger Zone Case": {
        "code": "Danger%20Zone%20Case",
        "image": "https://community.fastly.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUxnaPLJz5H74y1xtTcz6etNumIx29U6Zd3j7yQoYih3lG1-UJqY27xJIeLMlhpaD9Aclo/360fx360f"
    },
    "Operation Wildfire Case": {
        "code": "Operation%20Wildfire%20Case",
        "image": "https://community.fastly.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFYxnaeQImRGu4S1x9TawfSmY-iHkmoD7cEl2LiQpIjz3wPl_ERkYWHwLY-LMlhp9pkR_UQ/360fx360f"
    }
}

def load_latest_prices():
    if os.path.exists(LATEST_PRICES_FILE):
        with open(LATEST_PRICES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_latest_prices_for_all_cases(cases, prices_file="prices.json", output_file="latest_prices.json"):
    try:
        with open(prices_file, 'r') as f:
            prices_data = json.load(f)

        latest_prices = {}

        for case_name, case_info in cases.items():
            case_code = case_info["code"]

            if case_code in prices_data and prices_data[case_code]:
                latest_price = prices_data[case_code][-1][1]
                latest_prices[case_name] = latest_price
            else:
                latest_prices[case_name] = None

        with open(output_file, 'w') as f:
            json.dump(latest_prices, f, indent=4)

        print("✅ Zaktualizowano latest_prices.json!")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Błąd: {e}")


def value_change(cases, prices_file="prices.json"):
    try:
        with open(prices_file, 'r') as f:
            prices_data = json.load(f)

        latest_prices = {}

        for case_name, case_info in cases.items():
            case_code = case_info["code"]

            if case_code in prices_data and len(prices_data[case_code]) >= 2:
                latest_price = prices_data[case_code][-1][1]
                previous_price = prices_data[case_code][-2][1]
                change = ((latest_price - previous_price) / previous_price) * 100

                latest_prices[case_name] = {
                    "latest": latest_price,
                    "previous": previous_price,
                    "change": round(change, 2)
                }
            else:
                latest_prices[case_name] = None

        return latest_prices

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Błąd: {e}")
        return {}



def update_prices(data):
    prices = data
    for case_name, case_data in cases.items():
        market_code = case_data['code']
        url = PRICE_URL + market_code
        print(f"Przetwarzam skrzynkę: {case_name} ({market_code})")
        try:
            response = requests.get(url)
            data = response.json()
            if data and 'lowest_price' in data:
                lowest_price = data['lowest_price']
                cleaned_price = lowest_price.replace('zł', '').replace(',', '.').strip()
                today = time.strftime("%b %d %Y %H: +0")
                prices[market_code].append([today, float(cleaned_price)])
                print(f"Zaktualizowano {case_name}: {cleaned_price} zł")
            else:
                print(f"Nie znaleziono ceny dla {case_name}.")
        except Exception as e:
            print(f"Błąd podczas aktualizacji {case_name}: {e}")

        time.sleep(3)

    with open('prices.json', 'w') as file:
        json.dump(prices, file, indent=4)

    print("Aktualizacja pliku prices.json zakończona.")

    get_latest_prices_for_all_cases(cases)
