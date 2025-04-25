import pytest
import pandas as pd
from datetime import datetime
from core.zpracovatel_dat import ZpracovatelDat

@pytest.fixture
def zpracovatel():
    return ZpracovatelDat()

def test_vytvor_dataframe_data(zpracovatel):
    data_db = [(datetime(2023, 1, 1).date(), 25.0)]
    df = zpracovatel.vytvor_dataframe(data_db)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty # Není prázdný

def test_vytvor_dataframe_prazdny(zpracovatel):
    df = zpracovatel.vytvor_dataframe([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty # Je prázdný