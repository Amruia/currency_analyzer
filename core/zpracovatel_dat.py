import pandas as pd
import csv

class ZpracovatelDat:
    def vytvor_dataframe(self, data_kurzu_db):
        # Pokud je seznam prázdný, vrátíme prázdný DataFrame se správnými sloupci a indexem
        if not data_kurzu_db:
            empty_index = pd.to_datetime([]).rename('Datum')  # Prázdný časový index
            return pd.DataFrame(columns=['Kurz'], index=empty_index)

        # Vytvoření DataFrame ze seznamu záznamů (např. z databáze)
        df = pd.DataFrame(data_kurzu_db, columns=['Datum', 'Kurz'])
        df['Datum'] = pd.to_datetime(df['Datum'])  # Převedení sloupce Datum na datetime
        df = df.set_index('Datum')  # Nastavení sloupce Datum jako index
        df = df.sort_index()  # Seřazení podle datumu
        return df

    def exportuj_do_csv(self, dataframe, nazev_souboru):
        # Export DataFrame do CSV souboru
        try:
            dataframe.to_csv(nazev_souboru, index=True, date_format='%Y-%m-%d')  # Zahrne index jako sloupec
            print(f"Data úspěšně exportována do {nazev_souboru}")
            return True
        except Exception as e:
            # Ošetření chyb při zápisu do souboru
            print(f"Chyba při exportu do CSV: {e}")
            return False
