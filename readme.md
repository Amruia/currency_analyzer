# Analýza směnných kurzů měn

## Popis projektu

Jedná se o desktopovou aplikaci postavenou na knihovně PyQt, která umožňuje získávat a analyzovat směnné kurzy vybraných měn (např. USD, EUR, CNY) v reálném čase a zpětně.

Aplikace využívá veřejné API služby [Frankfurter](https://api.frankfurter.app/) pro stahování aktuálních i historických kurzů. Data jsou následně ukládána do lokální SQLite databáze a vizualizována interaktivním grafem prostřednictvím knihovny matplotlib. Pro analýzu dat je využita knihovna pandas a možnost exportu do formátu CSV zajišťuje snadné sdílení nebo další zpracování.

## Hlavní vlastnosti

- **Stahování aktuálních kurzů**: Pravidelný dotaz na API `api.frankfurter.dev` pro aktualizaci hodnot.
- **Historická data**: Uživatel si může vybrat časové období a zobrazit historický vývoj kurzu.
- **Interaktivní graf**: Zobrazení časové řady kurzů pomocí matplotlib s možností zoomování a výběru dat.
- **Export do CSV**: Ukládání filtrovanych nebo všech dat do externího CSV souboru.

## Použité technologie

- **Python 3.8+**
- **PyQt5**: Uživatelské rozhraní
- **requests**: HTTP klient pro komunikaci s API
- **sqlite3**: Lokální databáze
- **matplotlib**: Vizualizace dat v grafech
- **pandas**: Zpracování a analýza dat
- **csv**: Export dat do CSV

## Instalace

1. Naklonujte repozitář:
   ```bash
   git clone https://github.com/uzivatel/analýza-směnných-kurzů.git
   cd analýza-směnných-kurzů
   ```
2. Vytvořte a aktivujte virtuální prostředí (volitelné, ale doporučené):
   ```bash
   python -m venv venv
   source venv/bin/activate  # na Windows: venv\\Scripts\\activate
   ```
3. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

## Spuštění aplikace

```bash
python main.py
```

Po spuštění se zobrazí hlavní okno aplikace, kde lze:

1. Vybrat měnu a časové období
2. Stáhnout a zobrazit graf historických kurzů
3. Exportovat data do CSV

## Struktura projektu

Struktura hlavních adresářů a souborů projektu:

```plaintext
├── .gitignore                    # Git ignore rules
├── .gitlab-ci.yml                # CI/CD konfigurace
├── main.py                       # Vstupní bod aplikace
├── README.md                     # Tento soubor
├── requirements.txt              # Seznam Python závislostí
├── currency_analyzer/            # Hlavní balíček aplikace
│   ├── core/                     # Základní logika a datové operace
│   │   ├── __init__.py
│   │   ├── api_klient.py         # Klient pro volání API Frankfurter
│   │   ├── spravce_databaze.py   # Správa SQLite databáze
│   │   └── zpracovatel_dat.py    # Zpracování a analýza dat (pandas)
│   ├── data/                     # Surová data a databáze
│   │   └── smenne_kurzy.db       # Lokální SQLite databáze
│   ├── gui/                      # Grafické rozhraní PyQt
│   │   ├── __init__.py
│   │   ├── hlavni_okno.py        # Hlavní okno aplikace
│   │   └── widget_grafu.py       # Widget pro zobrazení grafu
│   └── tests/                    # Jednotkové testy
│       ├── __init__.py
│       ├── test_api_klient.py    # Testy API klienta
│       ├── test_spravce_databaze.py  # Testy správy databáze
│       └── test_zpracovatel_dat.py   # Testy zpracování dat

```

V menu aplikace zvolte možnost `Export CSV`. Data se uloží do souboru `export.csv` ve složce projektu. Lze specifikovat období nebo exportovat všechna dostupná data.

## Licence

Projekt je vydán pod licencí MIT. Více informací naleznete v souboru [LICENSE](LICENSE).

## Kontakt

V případě jakýchkoli dotazů či podnětů mě neváhejte kontaktovat:

- E-mail: [peleshkey123@seznam.cz](mailto\:peleshkey123@seznam.cz)
- GitHub: [github.com/Amruia](https://github.com/Amruia)

