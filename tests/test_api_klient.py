import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from core.api_klient import ApiKlient

# Fixture, která poskytuje instanci klienta pro testy
@pytest.fixture
def klient():
    return ApiKlient()

# Test aktuálního kurzu – ověřuje, že API klient správně zpracuje odpověď pro aktuální kurz
@patch('requests.get')  # Mockuje volání requests.get
def test_aktualni_kurz_ok(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {'rates': {'CZK': 25.5}}  # Simulovaná odpověď z API
    mock_get.return_value = mock_response
    kurz = klient.ziskej_aktualni_kurz('EUR', 'CZK')
    assert kurz is not None
    assert isinstance(kurz, float)  # Ověří, že výstup je číslo typu float

# Test historických kurzů – kontroluje, že se vrátí slovník s daty podle simulace
@patch('requests.get')
def test_historicke_kurzy_ok(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {'rates': {'2023-01-01': {'CZK': 25.0}}}  # Falešná historická data
    mock_get.return_value = mock_response
    data = klient.ziskej_historicke_kurzy('EUR', 'CZK', date(2023,1,1), date(2023,1,1))
    assert data is not None
    assert isinstance(data, dict)  # Ověří, že se vrací slovník

# Test seznamu měn – kontroluje, že API klient správně vrátí seznam měn ve formě listu
@patch('requests.get')
def test_seznam_men_ok(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {"EUR": "Euro", "USD": "US Dollar"}  # Falešný seznam měn
    mock_get.return_value = mock_response
    meny = klient.ziskej_seznam_men()
    assert meny is not None
    assert isinstance(meny, list)  # Ověří, že se vrací list
