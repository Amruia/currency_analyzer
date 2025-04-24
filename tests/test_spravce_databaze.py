import pytest
import sqlite3
from datetime import date
import os
from core.spravce_databaze import SpravceDatabaze

@pytest.fixture
def db_soubor_test():
    return ":memory:"

@pytest.fixture
def spravce(db_soubor_test):
    s = SpravceDatabaze(db_soubor=db_soubor_test)
    yield s
    s.zavri_spojeni()

def test_inicializace_databaze(spravce):
    conn = spravce._ziskej_spojeni()
    kurzor = conn.cursor()
    kurzor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kurzy';")
    vysledek = kurzor.fetchone()
    assert vysledek is not None
    assert vysledek[0] == 'kurzy'

def test_uloz_konkretni_kurz_novy(spravce):
    datum = date(2023, 10, 26)
    uspech = spravce.uloz_konkretni_kurz(datum, 'EUR', 'USD', 1.05)
    assert uspech is True

    conn = spravce._ziskej_spojeni()
    kurzor = conn.cursor()
    kurzor.execute("SELECT datum, mena_od, mena_do, kurz FROM kurzy WHERE datum = ?", (datum,))
    vysledek = kurzor.fetchone()
    assert vysledek is not None
    assert isinstance(vysledek[0], date)
    assert vysledek[0] == datum
    assert vysledek[1] == 'EUR'
    assert vysledek[2] == 'USD'
    assert vysledek[3] == 1.05

def test_uloz_konkretni_kurz_duplicita(spravce):
    datum = date(2023, 10, 27)
    uspech1 = spravce.uloz_konkretni_kurz(datum, 'GBP', 'JPY', 180.5)
    assert uspech1 is True
    uspech2 = spravce.uloz_konkretni_kurz(datum, 'GBP', 'JPY', 180.5)
    assert uspech2 is False

    conn = spravce._ziskej_spojeni()
    kurzor = conn.cursor()
    kurzor.execute("SELECT COUNT(*) FROM kurzy WHERE datum = ? AND mena_od = ? AND mena_do = ?", (datum, 'GBP', 'JPY'))
    pocet = kurzor.fetchone()[0]
    assert pocet == 1

def test_ziskej_kurzy_z_db(spravce):
    datum1 = date(2023, 11, 1)
    datum2 = date(2023, 11, 2)
    datum3 = date(2023, 11, 3)
    datum_mimo = date(2023, 10, 31)

    assert spravce.uloz_konkretni_kurz(datum1, 'USD', 'CAD', 1.38) is True
    assert spravce.uloz_konkretni_kurz(datum2, 'USD', 'CAD', 1.39) is True
    assert spravce.uloz_konkretni_kurz(datum3, 'USD', 'CAD', 1.385) is True
    assert spravce.uloz_konkretni_kurz(datum2, 'EUR', 'CAD', 1.50) is True
    assert spravce.uloz_konkretni_kurz(datum_mimo, 'USD', 'CAD', 1.37) is True

    vysledky = spravce.ziskej_kurzy_z_db('USD', 'CAD', date(2023, 11, 1), date(2023, 11, 3))

    assert len(vysledky) == 3
    assert vysledky[0]['datum'] == datum1
    assert vysledky[0]['kurz'] == 1.38
    assert vysledky[1]['datum'] == datum2
    assert vysledky[1]['kurz'] == 1.39
    assert vysledky[2]['datum'] == datum3
    assert vysledky[2]['kurz'] == 1.385

def test_ziskej_kurzy_z_db_zadna_data(spravce):
     vysledky = spravce.ziskej_kurzy_z_db('XYZ', 'ABC', date(2023, 1, 1), date(2023, 1, 5))
     assert len(vysledky) == 0
     assert vysledky == []