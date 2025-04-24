import sqlite3
import os
from datetime import date

class SpravceDatabaze:
    def __init__(self, db_soubor='data/smenne_kurzy.db'):
        self.db_soubor = db_soubor
        self.spojeni = None
        if self.db_soubor == ':memory:':
            self.spojeni = self._vytvor_spojeni()
            self.inicializuj_databazi()
        else:
            db_dir = os.path.dirname(self.db_soubor)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            self.inicializuj_databazi()

    def _vytvor_spojeni(self):
        return sqlite3.connect(self.db_soubor, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    def _ziskej_spojeni(self):
        if self.spojeni:
            return self.spojeni
        else:
            return self._vytvor_spojeni()

    def inicializuj_databazi(self):
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
                        UNIQUE(datum, mena_od, mena_do)
                    )
                ''')
        finally:
            if self.db_soubor != ':memory:' and conn:
                 conn.close()


    def uloz_konkretni_kurz(self, datum_obj, mena_od, mena_do, kurz):
         conn = self._ziskej_spojeni()
         try:
            with conn:
                kurzor = conn.cursor()
                try:
                    kurzor.execute('''
                        INSERT OR IGNORE INTO kurzy (datum, mena_od, mena_do, kurz)
                        VALUES (?, ?, ?, ?)
                    ''', (datum_obj, mena_od, mena_do, kurz))
                    return kurzor.rowcount > 0
                except sqlite3.Error as e:
                    print(f"Chyba při ukládání kurzu do databáze: {e}")
                    return False
         finally:
             if self.db_soubor != ':memory:' and conn:
                  conn.close()


    def ziskej_kurzy_z_db(self, mena_od, mena_do, datum_od, datum_do):
        conn = self._ziskej_spojeni()
        conn.row_factory = sqlite3.Row
        kurzor = conn.cursor()
        try:
            kurzor.execute('''
                SELECT datum, kurz FROM kurzy
                WHERE mena_od = ? AND mena_do = ? AND datum BETWEEN ? AND ?
                ORDER BY datum ASC
            ''', (mena_od, mena_do, datum_od, datum_do))
            return kurzor.fetchall()
        except sqlite3.Error as e:
             print(f"Chyba při získávání kurzů z databáze: {e}")
             return []
        finally:
             if self.db_soubor != ':memory:' and conn:
                  conn.close()

    def zavri_spojeni(self):
         if self.spojeni:
              self.spojeni.close()
              self.spojeni = None