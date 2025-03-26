import requests
import urllib.parse  # Do kodowania nazwy przedmiotu w URL

# API URL
GAMMA = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name=Gamma%20Case"
#https://github.com/Revadike/InternalSteamWebAPI/wiki
# Wysłanie zapytania
response = requests.get(GAMMA)

# Obsługa odpowiedzi
if response.status_code == 200:
    data = response.json()  # Konwersja odpowiedzi na JSON
    print(data)
else:
    print(f"Błąd: {response.status_code}, Treść odpowiedzi: {response.text}")
