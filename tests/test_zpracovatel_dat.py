import pytest
import pandas as pd
from datetime import datetime
from core.zpracovatel_dat import ZpracovatelDat

# Fixture pro vytvoření instance zpracovatele dat
@pytest.fixture
def zpracovatel():
    return ZpracovatelDat()

# Test vytvoření DataFrame z neprázdných dat
def test_vytvor_dataframe_data(zpracovatel):
    data_db = [(datetime(2023, 1, 1).date(), 25.0)]  # Jeden řádek s datem a kurzem
    df = zpracovatel.vytvor_dataframe(data_db)
    assert isinstance(df, pd.DataFrame)  # Výstup je DataFrame
    assert not df.empty  # DataFrame není prázdný

# Test vytvoření DataFrame z prázdného seznamu
def test_vytvor_dataframe_prazdny(zpracovatel):
    df = zpracovatel.vytvor_dataframe([])  # Prázdný vstup
    assert isinstance(df, pd.DataFrame)  # Výstup je DataFrame
    assert df.empty  # DataFrame je prázdný
