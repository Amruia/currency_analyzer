import requests
from datetime import date, timedelta

class ApiKlient:
    def __init__(self, base_url="https://api.frankfurter.app"):
        self.base_url = base_url  # Základní URL adresa API

    def ziskej_aktualni_kurz(self, mena_od='EUR', mena_do='CZK'):
        try:
            # Sestavení URL pro aktuální kurz mezi dvěma měnami
            url = f"{self.base_url}/latest?from={mena_od}&to={mena_do}"
            odpoved = requests.get(url)  # Odeslání GET požadavku
            odpoved.raise_for_status()  # Kontrola HTTP chyb
            data = odpoved.json()  # Získání odpovědi jako JSON
            return data['rates'][mena_do]  # Vrácení kurzu požadované měny
        except requests.exceptions.RequestException as e:
            # Ošetření chyby spojené s požadavkem
            print(f"Chyba při získávání aktuálního kurzu: {e}")
            return None
        except KeyError:
            # Ošetření chyby při přístupu k neexistujícím datům
            print(f"Chyba: Neplatná měna nebo data nejsou dostupná.")
            return None

    def ziskej_historicke_kurzy(self, mena_od, mena_do, datum_od, datum_do):
        try:
            # Převedení dat na řetězce ve formátu YYYY-MM-DD
            datum_od_str = datum_od.strftime('%Y-%m-%d')
            datum_do_str = datum_do.strftime('%Y-%m-%d')
            # Sestavení URL pro získání historických kurzů
            url = f"{self.base_url}/{datum_od_str}..{datum_do_str}?from={mena_od}&to={mena_do}"
            odpoved = requests.get(url)  # Odeslání požadavku
            odpoved.raise_for_status()  # Kontrola HTTP chyb
            data = odpoved.json()  # Získání dat jako JSON
            return data.get('rates', {})  # Vrácení historických kurzů nebo prázdného slovníku
        except requests.exceptions.RequestException as e:
            # Ošetření chyby s požadavkem
            print(f"Chyba při získávání historických kurzů: {e}")
            return {}
        except KeyError:
            # Ošetření chyby při přístupu k neexistujícím datům
            print(f"Chyba: Historická data nejsou dostupná pro dané měny/období.")
            return {}

    def ziskej_seznam_men(self):
        try:
            # URL pro seznam podporovaných měn
            url = f"{self.base_url}/currencies"
            odpoved = requests.get(url)  # Odeslání požadavku
            odpoved.raise_for_status()  # Kontrola chyb odpovědi
            data = odpoved.json()  # Parsování JSON odpovědi
            return list(data.keys())  # Vrácení seznamu měnových kódů
        except requests.exceptions.RequestException as e:
            # Ošetření chyby při komunikaci s API
            print(f"Chyba při získávání seznamu měn: {e}")
            return ['EUR', 'USD', 'CZK', 'GBP', 'PLN', 'CNY']  # Náhradní seznam měn
        except Exception as e:
            # Ošetření neočekávané chyby
            print(f"Neočekávaná chyba při získávání seznamu měn: {e}")
            return ['EUR', 'USD', 'CZK', 'GBP', 'PLN', 'CNY']
