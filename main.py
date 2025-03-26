import requests
import urllib.parse  # Do kodowania nazwy przedmiotu w URL
#https://github.com/Revadike/InternalSteamWebAPI/wiki
# API URL
PRICE_URL = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="
PRICE_HISTORY_URL = "https://steamcommunity.com/market/pricehistory?appid=730&market_hash_name="
gamma = "Gamma%20Case"
falchion = "Falchion%20Case"
huntsman = "Huntsman%20Weapon%20Case"
chroma = "Chroma%20Case"
glove = "Glove%20Case"
revolver = "Revolver%20Case"
fracture = "Fracture%20Case"
recoil = "Recoil%20Case"
revolution = "Revolution%20Case"
kilowatt = "Kilowatt%20Case"
gallery = "Gallery%20Case"
shadow = "Shadow%20Case"
spectrum = "Spectrum%20Case"
winter_offensive = "Winter%20Offensive%20Weapon%20Case"
hydra = "Operation%20Hydra%20Case"
vanguard = "Operation%20Vanguard%20Weapon%20Case"
csgo = "CS%3AGO%20Weapon%20Case"
horizon = "Horizon%20Case"
clutch = "Clutch%20Case"
bravo = "Operation%20Bravo%20Case"
riptide = "Operation%20Riptide%20Case"
breakout = "Operation%20Breakout%20Weapon%20Case"
phoenix = "Operation%20Phoenix%20Weapon%20Case"
cs20 = "CS20%20Case"
chroma2 = "Chroma%202%20Case"
spectrum2 = "Spectrum%202%20Case"
prisma2 = "Prisma%202%20Case"
prisma = "Prisma%20Case"
snakebite = "Snakebite%20Case"
csgo3 = "CS%3AGO%20Weapon%20Case%203"
brokenfang = "Operation%20Broken%20Fang%20Case"
csgo2 = "CS%3AGO%20Weapon%20Case%202"
dreamsnightmares = "Dreams%20%26%20Nightmares%20Case"
shatteredweb = "Shattered%20Web%20Case"
chroma3 = "Chroma%203%20Case"
# Wysłanie zapytania
response = requests.get(PRICE_HISTORY_URL + gamma)

# Obsługa odpowiedzi
if response.status_code == 200:
    data = response.json()  # Konwersja odpowiedzi na JSON
    print(data)
else:
    print(f"Błąd: {response.status_code}, Treść odpowiedzi: {response.text}")
