import requests
import json
import os
import time
import datetime
import urllib.parse
#https://github.com/Revadike/InternalSteamWebAPI/wiki

FILENAME = "prices.json"

cookies = {
    "sessionid": "secret",
    "steamLoginSecure": "secret"
}

PRICE_URL = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="
PRICE_HISTORY_URL = "https://steamcommunity.com/market/pricehistory?appid=730&market_hash_name="

cases = [
    "Gamma%20Case", "Falchion%20Case", "Huntsman%20Weapon%20Case", "Chroma%20Case",
    "Glove%20Case", "Revolver%20Case", "Fracture%20Case", "Recoil%20Case",
    "Revolution%20Case", "Kilowatt%20Case", "Gallery%20Case", "Shadow%20Case",
    "Spectrum%20Case", "Winter%20Offensive%20Weapon%20Case", "Operation%20Hydra%20Case",
    "Operation%20Vanguard%20Weapon%20Case", "CS%3AGO%20Weapon%20Case", "Horizon%20Case",
    "Clutch%20Case", "Operation%20Bravo%20Case", "Operation%20Riptide%20Case",
    "Operation%20Breakout%20Weapon%20Case", "Operation%20Phoenix%20Weapon%20Case",
    "CS20%20Case", "Chroma%202%20Case", "Spectrum%202%20Case", "Prisma%202%20Case",
    "Prisma%20Case", "Snakebite%20Case", "CS%3AGO%20Weapon%20Case%203",
    "Operation%20Broken%20Fang%20Case", "CS%3AGO%20Weapon%20Case%202",
    "Dreams%20%26%20Nightmares%20Case", "Shattered%20Web%20Case", "Chroma%203%20Case"
]

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def update_prices():
    data = load_data()
    now = datetime.datetime.now().strftime("%b %d %Y %H: +0")  # Timestamp w formacie, który masz

    for case in cases:
        response = requests.get(PRICE_URL + case)
        if response.status_code == 200:
            result = response.json()
            if "prices" in result:
                price = result["prices"][0][1]  # Cena (float)
                transactions = result["prices"][0][2]  # Liczba transakcji (lub liczba przedmiotów)

                # Dodanie do pliku JSON
                if case not in data:
                    data[case] = []

                data[case].append([now, price, transactions])
                print(f"Zaktualizowano: {case} -> {price} PLN")

    save_data(data)
    print("Aktualizacja zakończona!")


# Wywołanie funkcji aktualizującej ceny
update_prices()
