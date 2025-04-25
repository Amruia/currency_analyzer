import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from core.api_klient import ApiKlient

@pytest.fixture
def klient():
    return ApiKlient()

@patch('requests.get')
def test_aktualni_kurz_ok(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {'rates': {'CZK': 25.5}}
    mock_get.return_value = mock_response
    kurz = klient.ziskej_aktualni_kurz('EUR', 'CZK')
    assert kurz is not None
    assert isinstance(kurz, float)

@patch('requests.get')
def test_historicke_kurzy_ok(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {'rates': {'2023-01-01': {'CZK': 25.0}}}
    mock_get.return_value = mock_response
    data = klient.ziskej_historicke_kurzy('EUR', 'CZK', date(2023,1,1), date(2023,1,1))
    assert data is not None
    assert isinstance(data, dict)

@patch('requests.get')
def test_seznam_men_ok(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {"EUR": "Euro", "USD": "US Dollar"}
    mock_get.return_value = mock_response
    meny = klient.ziskej_seznam_men()
    assert meny is not None
    assert isinstance(meny, list)