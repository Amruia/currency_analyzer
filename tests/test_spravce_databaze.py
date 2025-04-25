import pytest
from datetime import date
from core.spravce_databaze import SpravceDatabaze

@pytest.fixture
def spravce():
    s = SpravceDatabaze(db_soubor=":memory:")
    yield s
    s.zavri_spojeni()

def test_ulozeni_a_ziskani_zaklad(spravce):
    datum = date(2023, 11, 1)
    ulozeno = spravce.uloz_konkretni_kurz(datum, 'USD', 'CAD', 1.38)
    assert ulozeno is True # Ověříme, že se něco uložilo
    vysledky = spravce.ziskej_kurzy_z_db('USD', 'CAD', datum, datum)
    assert len(vysledky) > 0 # Ověříme, že jsme něco našli

def test_ziskani_nic_nenalezeno(spravce):
     vysledky = spravce.ziskej_kurzy_z_db('NEEXIST', 'NIC', date(2023, 1, 1), date(2023, 1, 5))
     assert len(vysledky) == 0 # Ověříme, že seznam je prázdný