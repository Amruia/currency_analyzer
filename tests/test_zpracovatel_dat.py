import pytest
import pandas as pd
from datetime import datetime
import os
from core.zpracovatel_dat import ZpracovatelDat

@pytest.fixture
def zpracovatel():
    return ZpracovatelDat()

@pytest.fixture
def ukazkova_data_db():
    return [
        (datetime(2023, 1, 2).date(), 25.1),
        (datetime(2023, 1, 1).date(), 25.0),
        (datetime(2023, 1, 3).date(), 25.2)
    ]

@pytest.fixture
def prazdna_data_db():
    return []

def test_vytvor_dataframe_uspech(zpracovatel, ukazkova_data_db):
    df = zpracovatel.vytvor_dataframe(ukazkova_data_db)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ['Kurz']
    assert isinstance(df.index, pd.DatetimeIndex)
    assert len(df) == 3

    assert df.index[0] == pd.Timestamp('2023-01-01')
    assert df.index[1] == pd.Timestamp('2023-01-02')
    assert df.index[2] == pd.Timestamp('2023-01-03')
    assert df.loc['2023-01-01']['Kurz'] == 25.0
    assert df.loc['2023-01-02']['Kurz'] == 25.1
    assert df.loc['2023-01-03']['Kurz'] == 25.2

def test_vytvor_dataframe_prazdna_data(zpracovatel, prazdna_data_db):
    df = zpracovatel.vytvor_dataframe(prazdna_data_db)

    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert list(df.columns) == ['Kurz']
    assert df.index.name == 'Datum'

def test_exportuj_do_csv(zpracovatel, ukazkova_data_db, tmp_path):
    df = zpracovatel.vytvor_dataframe(ukazkova_data_db)
    nazev_souboru = tmp_path / "export_test.csv"

    uspech = zpracovatel.exportuj_do_csv(df, str(nazev_souboru))

    assert uspech is True
    assert os.path.exists(nazev_souboru)

    df_nacteny = pd.read_csv(nazev_souboru, index_col='Datum', parse_dates=True)
    pd.testing.assert_frame_equal(df.sort_index(), df_nacteny.sort_index())

def test_exportuj_do_csv_chyba(zpracovatel, ukazkova_data_db):
    df = zpracovatel.vytvor_dataframe(ukazkova_data_db)
    neplatna_cesta = "/nejaka/neexistujici/cesta/export.csv"

    uspech = zpracovatel.exportuj_do_csv(df, neplatna_cesta)

    assert uspech is False