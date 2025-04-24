import pytest
from unittest.mock import patch, MagicMock
from datetime import date
import requests
from core.api_klient import ApiKlient

@pytest.fixture
def klient():
    return ApiKlient(base_url="http://test.com")

@patch('requests.get')
def test_ziskej_aktualni_kurz_uspech(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {'rates': {'CZK': 25.5}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    kurz = klient.ziskej_aktualni_kurz('EUR', 'CZK')
    assert kurz == 25.5
    mock_get.assert_called_once_with("http://test.com/latest?from=EUR&to=CZK")

@patch('requests.get')
def test_ziskej_aktualni_kurz_chyba_api(mock_get, klient):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Chyba sítě")
    mock_get.return_value = mock_response

    kurz = klient.ziskej_aktualni_kurz('EUR', 'CZK')
    assert kurz is None

@patch('requests.get')
def test_ziskej_historicke_kurzy_uspech(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'rates': {
            '2023-01-01': {'CZK': 25.0},
            '2023-01-02': {'CZK': 25.1}
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    datum_od = date(2023, 1, 1)
    datum_do = date(2023, 1, 2)
    data = klient.ziskej_historicke_kurzy('EUR', 'CZK', datum_od, datum_do)

    assert '2023-01-01' in data
    assert data['2023-01-01']['CZK'] == 25.0
    assert '2023-01-02' in data
    assert data['2023-01-02']['CZK'] == 25.1
    mock_get.assert_called_once_with("http://test.com/2023-01-01..2023-01-02?from=EUR&to=CZK")

@patch('requests.get')
def test_ziskej_historicke_kurzy_chyba_api(mock_get, klient):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Chyba sítě")
    mock_get.return_value = mock_response

    datum_od = date(2023, 1, 1)
    datum_do = date(2023, 1, 2)
    data = klient.ziskej_historicke_kurzy('EUR', 'CZK', datum_od, datum_do)
    assert data == {}

@patch('requests.get')
def test_ziskej_seznam_men_uspech(mock_get, klient):
    mock_response = MagicMock()
    mock_response.json.return_value = {"EUR": "Euro", "USD": "US Dollar", "CZK": "Czech Koruna"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    meny = klient.ziskej_seznam_men()
    assert sorted(meny) == sorted(["EUR", "USD", "CZK"])
    mock_get.assert_called_once_with("http://test.com/currencies")

@patch('requests.get')
def test_ziskej_seznam_men_chyba_api(mock_get, klient):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Chyba sítě")
    mock_get.return_value = mock_response

    meny = klient.ziskej_seznam_men()
    assert meny == ['EUR', 'USD', 'CZK', 'GBP', 'PLN', 'CNY']