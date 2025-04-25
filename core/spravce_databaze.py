import sqlite3
import os
from datetime import date

class SpravceDatabaze:
    def __init__(self, db_soubor='data/smenne_kurzy.db'):
        self.db_soubor = db_soubor  # Cesta k databázovému souboru
        self.spojeni = None  # Uložené spojení s databází (pro paměťové DB)
        if self.db_soubor == ':memory:':
            # Pokud používáme databázi v paměti, vytvoříme spojení ihned
            self.spojeni = self._vytvor_spojeni()
            self.inicializuj_databazi()
        else:
            # Pokud je zadán soubor, vytvoříme složku pokud neexistuje
            db_dir = os.path.dirname(self.db_soubor)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            self.inicializuj_databazi()

    def _vytvor_spojeni(self):
        # Vytvoření spojení s databází
        return sqlite3.connect(self.db_soubor, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    def _ziskej_spojeni(self):
        # Vrácení existujícího nebo nového spojení s databází
        if self.spojeni:
            return self.spojeni
        else:
            return self._vytvor_spojeni()

    def inicializuj_databazi(self):
        # Inicializace databáze – vytvoření tabulky pokud ještě neexistuje
        conn = self._ziskej_spojeni()
        try:
            with conn:
                kurzor = conn.cursor()
                kurzor.execute('''
                    CREATE TABLE IF NOT EXISTS kurzy (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        datum DATE NOT NULL,
                        mena_od TEXT NOT NULL,
                        mena_do TEXT NOT NULL,
                        kurz REAL NOT NULL,
                        UNIQUE(datum, mena_od, mena_do)  -- Unikátní záznam pro každou kombinaci měn a datumu
                    )
                ''')
        finally:
            # Uzavření spojení, pokud nejde o paměťovou databázi
            if self.db_soubor != ':memory:' and conn:
                 conn.close()

    def uloz_konkretni_kurz(self, datum_obj, mena_od, mena_do, kurz):
         # Uložení jednoho konkrétního kurzu do databáze
         conn = self._ziskej_spojeni()
         try:
            with conn:
                kurzor = conn.cursor()
                try:
                    kurzor.execute('''
                        INSERT OR IGNORE INTO kurzy (datum, mena_od, mena_do, kurz)
                        VALUES (?, ?, ?, ?)
                    ''', (datum_obj, mena_od, mena_do, kurz))
                    return kurzor.rowcount > 0  # Vrací True, pokud byl kurz vložen
                except sqlite3.Error as e:
                    print(f"Chyba při ukládání kurzu do databáze: {e}")
                    return False
         finally:
             if self.db_soubor != ':memory:' and conn:
                  conn.close()

    def ziskej_kurzy_z_db(self, mena_od, mena_do, datum_od, datum_do):
        # Získání historických kurzů z databáze v daném rozsahu
        conn = self._ziskej_spojeni()
        conn.row_factory = sqlite3.Row  # Umožňuje přístup k datům přes názvy sloupců
        kurzor = conn.cursor()
        try:
            kurzor.execute('''
                SELECT datum, kurz FROM kurzy
                WHERE mena_od = ? AND mena_do = ? AND datum BETWEEN ? AND ?
                ORDER BY datum ASC
            ''', (mena_od, mena_do, datum_od, datum_do))
            return kurzor.fetchall()  # Vrací seznam řádků s datem a kurzem
        except sqlite3.Error as e:
             print(f"Chyba při získávání kurzů z databáze: {e}")
             return []
        finally:
             if self.db_soubor != ':memory:' and conn:
                  conn.close()

    def zavri_spojeni(self):
         # Uzavření spojení s databází (používáno u paměťové varianty)
         if self.spojeni:
              self.spojeni.close()
              self.spojeni = None
