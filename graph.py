import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from prices_data import load_data, cases


# Funkcja do rysowania wykresu
def plot_prices(case_name):
    data = load_data()
    if case_name not in data:
        print(f"Brak danych dla {case_name}")
        return

    timestamps = []
    prices = []

    # Pobieranie dat i cen z historii
    for entry in data[case_name]:
        timestamp = datetime.strptime(entry[0], "%b %d %Y %H: +0")
        price = entry[1]
        timestamps.append(timestamp)
        prices.append(price)

    # Rysowanie wykresu
    plt.figure(figsize=(16, 10))
    plt.plot(timestamps, prices, marker='o', color='b', label="Cena")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Data", fontsize=14)
    plt.ylabel("Cena", fontsize=14)
    plt.title(f"Cena {case_name} w czasie")
    plt.show()

# Rysowanie wykresu dla "Gamma%20Case"
plot_prices("Gamma%20Case")