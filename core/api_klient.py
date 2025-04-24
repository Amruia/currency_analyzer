import requests
from datetime import date, timedelta

class ApiKlient:
    def __init__(self, base_url="https://api.frankfurter.app"):
        self.base_url = base_url

    def ziskej_aktualni_kurz(self, mena_od='EUR', mena_do='CZK'):
        try:
            url = f"{self.base_url}/latest?from={mena_od}&to={mena_do}"
            odpoved = requests.get(url)
            odpoved.raise_for_status() #Kontrola HTTP chyb
            data = odpoved.json()
            return data['rates'][mena_do]
        except requests.exceptions.RequestException as e:
            print(f"Chyba při získávání aktuálního kurzu: {e}")
            return None
        except KeyError:
            print(f"Chyba: Neplatná měna nebo data nejsou dostupná.")
            return None

    def ziskej_historicke_kurzy(self, mena_od, mena_do, datum_od, datum_do):
        try:
            datum_od_str = datum_od.strftime('%Y-%m-%d')
            datum_do_str = datum_do.strftime('%Y-%m-%d')
            url = f"{self.base_url}/{datum_od_str}..{datum_do_str}?from={mena_od}&to={mena_do}"
            odpoved = requests.get(url)
            odpoved.raise_for_status()
            data = odpoved.json()
            return data.get('rates', {})
        except requests.exceptions.RequestException as e:
            print(f"Chyba při získávání historických kurzů: {e}")
            return {}
        except KeyError:
            print(f"Chyba: Historická data nejsou dostupná pro dané měny/období.")
            return {}

    def ziskej_seznam_men(self):
        try:
            url = f"{self.base_url}/currencies"
            odpoved = requests.get(url)
            odpoved.raise_for_status()
            data = odpoved.json()
            return list(data.keys())
        except requests.exceptions.RequestException as e:
            print(f"Chyba při získávání seznamu měn: {e}")
            return ['EUR', 'USD', 'CZK', 'GBP', 'PLN', 'CNY'] # Záložní seznam
        except Exception as e:
            print(f"Neočekávaná chyba při získávání seznamu měn: {e}")
            return ['EUR', 'USD', 'CZK', 'GBP', 'PLN', 'CNY']