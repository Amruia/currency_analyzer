import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QDateEdit, QFileDialog, QMessageBox,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont

from core.api_klient import ApiKlient  # Zajišťuje komunikaci s měnovým API
from core.spravce_databaze import SpravceDatabaze  # Zajišťuje práci s databází
from core.zpracovatel_dat import ZpracovatelDat  # Pomáhá se zpracováním a exportem dat
from gui.widget_grafu import WidgetGrafu  # Vlastní widget pro vykreslení grafu
import pandas as pd
from datetime import datetime, timedelta

class HlavniOkno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Analyzer")  # Název hlavního okna
        self.setGeometry(100, 100, 800, 600)  # Výchozí rozměry a pozice

        # Inicializace komponent
        self.api_klient = ApiKlient()
        self.spravce_db = SpravceDatabaze()
        self.zpracovatel_dat = ZpracovatelDat()
        self.aktualni_dataframe = pd.DataFrame()  # Pro uložení aktuálně zobrazených dat

        self.dostupne_meny = self.api_klient.ziskej_seznam_men()  # Načtení seznamu měn

        self.init_ui()  # Sestavení uživatelského rozhraní

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Sekce výběru měn a zobrazení aktuálního kurzu
        mena_layout = QHBoxLayout()
        mena_layout.addWidget(QLabel("Základní měna:"))
        self.combo_mena_od = QComboBox()
        self.combo_mena_od.addItems(self.dostupne_meny)
        self.combo_mena_od.setCurrentText("EUR")  # Výchozí hodnota
        mena_layout.addWidget(self.combo_mena_od)

        mena_layout.addWidget(QLabel("Cílová měna:"))
        self.combo_mena_do = QComboBox()
        self.combo_mena_do.addItems(self.dostupne_meny)
        self.combo_mena_do.setCurrentText("CZK")  # Výchozí hodnota
        mena_layout.addWidget(self.combo_mena_do)

        self.tlacitko_aktualni_kurz = QPushButton("Získat aktuální kurz")
        self.tlacitko_aktualni_kurz.clicked.connect(self.zobraz_aktualni_kurz)
        mena_layout.addWidget(self.tlacitko_aktualni_kurz)

        self.label_aktualni_kurz = QLabel("Aktuální kurz: -")
        font = QFont()
        font.setBold(True)
        self.label_aktualni_kurz.setFont(font)
        mena_layout.addWidget(self.label_aktualni_kurz)
        mena_layout.addStretch()  # Posune obsah doleva

        main_layout.addLayout(mena_layout)

        # Sekce pro výběr období historie kurzů
        historie_layout = QHBoxLayout()
        historie_layout.addWidget(QLabel("Od data:"))
        self.datum_od = QDateEdit()
        self.datum_od.setCalendarPopup(True)
        self.datum_od.setDate(QDate.currentDate().addMonths(-1))  # Výchozí datum je měsíc zpět
        historie_layout.addWidget(self.datum_od)

        historie_layout.addWidget(QLabel("Do data:"))
        self.datum_do = QDateEdit()
        self.datum_do.setCalendarPopup(True)
        self.datum_do.setDate(QDate.currentDate())  # Výchozí datum je dnešek
        historie_layout.addWidget(self.datum_do)

        self.tlacitko_zobrazit_historii = QPushButton("Zobrazit historii")
        self.tlacitko_zobrazit_historii.clicked.connect(self.zobraz_historii)
        historie_layout.addWidget(self.tlacitko_zobrazit_historii)
        historie_layout.addStretch()

        main_layout.addLayout(historie_layout)

        # Sekce grafu – zabírá většinu okna
        self.widget_grafu = WidgetGrafu()
        main_layout.addWidget(self.widget_grafu, 1)

        # Sekce pro export do CSV
        export_layout = QHBoxLayout()
        self.tlacitko_export = QPushButton("Exportovat do CSV")
        self.tlacitko_export.clicked.connect(self.exportovat_data)
        self.tlacitko_export.setEnabled(False)  # Povolit až po načtení historie
        export_layout.addWidget(self.tlacitko_export)
        export_layout.addStretch()
        main_layout.addLayout(export_layout)

    # Získání a zobrazení aktuálního kurzu z API
    def zobraz_aktualni_kurz(self):
        mena_od = self.combo_mena_od.currentText()
        mena_do = self.combo_mena_do.currentText()

        # Kontrola na stejnou měnu
        if mena_od == mena_do:
             QMessageBox.warning(self, "Chyba", "Základní a cílová měna nemohou být stejné.")
             self.label_aktualni_kurz.setText("Aktuální kurz: Chyba")
             return

        # Získání kurzu z API
        kurz = self.api_klient.ziskej_aktualni_kurz(mena_od, mena_do)
        if kurz is not None:
            self.label_aktualni_kurz.setText(f"Aktuální kurz ({mena_od}/{mena_do}): {kurz:.4f}")
            dnes = datetime.now().date()
            self.spravce_db.uloz_konkretni_kurz(dnes, mena_od, mena_do, kurz)  # Uložení do DB
        else:
            self.label_aktualni_kurz.setText("Aktuální kurz: Chyba")
            QMessageBox.warning(self, "Chyba API", "Nepodařilo se získat aktuální kurz z API.")

    # Zobrazení historických dat a jejich načtení z DB nebo API
    def zobraz_historii(self):
        mena_od = self.combo_mena_od.currentText()
        mena_do = self.combo_mena_do.currentText()
        datum_od = self.datum_od.date().toPyDate()
        datum_do = self.datum_do.date().toPyDate()

        # Kontrola na stejnou měnu
        if mena_od == mena_do:
             QMessageBox.warning(self, "Chyba", "Základní a cílová měna nemohou být stejné.")
             self.widget_grafu.vykresli_data(pd.DataFrame(), mena_od, mena_do)
             self.aktualni_dataframe = pd.DataFrame()
             self.tlacitko_export.setEnabled(False)
             return

        # Kontrola validnosti dat
        if datum_od >= datum_do:
            QMessageBox.warning(self, "Chyba data", "Datum 'Od' musí být před datem 'Do'.")
            self.widget_grafu.vykresli_data(pd.DataFrame(), mena_od, mena_do)
            self.aktualni_dataframe = pd.DataFrame()
            self.tlacitko_export.setEnabled(False)
            return

        # Pokus získat data z DB
        data_z_db = self.spravce_db.ziskej_kurzy_z_db(mena_od, mena_do, datum_od, datum_do)

        # Pokud chybí data, stáhnout z API
        if not data_z_db or len(data_z_db) < (datum_do - datum_od).days + 1:
            print("Data nejsou kompletní v DB, stahuji z API...")
            historicka_data_api = self.api_klient.ziskej_historicke_kurzy(mena_od, mena_do, datum_od, datum_do)
            if historicka_data_api:
                 pocet_ulozenych = 0
                 for datum_str, kurzy_dict in historicka_data_api.items():
                      kurz = kurzy_dict.get(mena_do)
                      if kurz is not None:
                          datum_obj = datetime.strptime(datum_str, '%Y-%m-%d').date()
                          if self.spravce_db.uloz_konkretni_kurz(datum_obj, mena_od, mena_do, kurz):
                              pocet_ulozenych += 1
                 if pocet_ulozenych > 0:
                     print(f"Uloženo {pocet_ulozenych} nových záznamů z API do DB.")
                 data_z_db = self.spravce_db.ziskej_kurzy_z_db(mena_od, mena_do, datum_od, datum_do)
            else:
                 QMessageBox.warning(self, "Chyba API", "Nepodařilo se získat historická data z API.")
                 if not data_z_db:
                     self.widget_grafu.vykresli_data(pd.DataFrame(), mena_od, mena_do)
                     self.aktualni_dataframe = pd.DataFrame()
                     self.tlacitko_export.setEnabled(False)
                     return

        # Zpracování a zobrazení grafu
        if data_z_db:
            self.aktualni_dataframe = self.zpracovatel_dat.vytvor_dataframe(data_z_db)
            self.widget_grafu.vykresli_data(self.aktualni_dataframe, mena_od, mena_do)
            self.tlacitko_export.setEnabled(True)
        else:
            QMessageBox.information(self, "Žádná data", f"Nebyly nalezeny žádné historické kurzy pro {mena_od}/{mena_do} v daném období.")
            self.widget_grafu.vykresli_data(pd.DataFrame(), mena_od, mena_do)
            self.aktualni_dataframe = pd.DataFrame()
            self.tlacitko_export.setEnabled(False)

    # Export dat do CSV souboru
    def exportovat_data(self):
        if self.aktualni_dataframe.empty:
            QMessageBox.warning(self, "Chyba exportu", "Nejsou žádná data k exportu. Nejprve zobrazte historii.")
            return

        mena_od = self.combo_mena_od.currentText()
        mena_do = self.combo_mena_do.currentText()
        vychozi_nazev = f"kurzy_{mena_od}_{mena_do}_{datetime.now().strftime('%Y%m%d')}.csv"

        # Dialog pro výběr umístění a názvu souboru
        cesta_souboru, _ = QFileDialog.getSaveFileName(
            self,
            "Exportovat data do CSV",
            vychozi_nazev,
            "CSV soubory (*.csv);;Všechny soubory (*)"
        )

        # Export do souboru
        if cesta_souboru:
            if self.zpracovatel_dat.exportuj_do_csv(self.aktualni_dataframe, cesta_souboru):
                QMessageBox.information(self, "Export úspěšný", f"Data byla úspěšně exportována do:\n{cesta_souboru}")
            else:
                QMessageBox.critical(self, "Chyba exportu", "Nepodařilo se exportovat data do souboru.")
