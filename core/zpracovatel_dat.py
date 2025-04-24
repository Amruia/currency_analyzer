import pandas as pd
import csv

class ZpracovatelDat:
    def vytvor_dataframe(self, data_kurzu_db):
        if not data_kurzu_db:
            empty_index = pd.to_datetime([]).rename('Datum')
            return pd.DataFrame(columns=['Kurz'], index=empty_index)

        df = pd.DataFrame(data_kurzu_db, columns=['Datum', 'Kurz'])
        df['Datum'] = pd.to_datetime(df['Datum'])
        df = df.set_index('Datum')
        df = df.sort_index()
        return df

    def exportuj_do_csv(self, dataframe, nazev_souboru):
        try:
            dataframe.to_csv(nazev_souboru, index=True, date_format='%Y-%m-%d')
            print(f"Data úspěšně exportována do {nazev_souboru}")
            return True
        except Exception as e:
            print(f"Chyba při exportu do CSV: {e}")
            return False