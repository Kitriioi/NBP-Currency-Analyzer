import requests
import csv
from datetime import datetime


def fetch_exchange_rates():
    
    url = "http://api.nbp.pl/api/exchangerates/tables/a/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]['rates']
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return []


def save_to_csv(rates, filename="kursy_walut.csv"):
    if not rates:
        return


    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(["Kod", "Waluta", "Kurs"])

        for rate in rates:
            writer.writerow([rate['code'], rate['currency'], rate['mid']])
    print(f"Dane zapisano pomyślnie do pliku {filename}")


def analyze_rates(rates):
    if not rates:
        return


    most_expensive = max(rates, key=lambda x: x['mid'])
    print(f"\nRAPORT Z DNIA {datetime.now().strftime('%Y-%m-%d')}:")
    print(f"Najdroższa waluta: {most_expensive['currency']} ({most_expensive['code']}) - {most_expensive['mid']} PLN")


if __name__ == "__main__":
    print("Pobieranie danych z NBP...")
    rates_data = fetch_exchange_rates()
    save_to_csv(rates_data)
    analyze_rates(rates_data)