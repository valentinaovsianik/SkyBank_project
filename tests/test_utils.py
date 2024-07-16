import pytest
import os
from datetime import datetime
import json
from unittest.mock import patch
from src.utils import get_exchange_rates, get_stock_prices

@pytest.fixture
def mock_api_key():
    """Мок для API ключа"""
    return "dummy_api_key"

@pytest.fixture
def mock_settings_file(tmp_path):
    """Фикстура для временного файла с настройками для теста"""
    settings = {
        "user_stocks": ["AAPL", "MSFT", "GOOGL"]
    }
    settings_file = tmp_path / "settings.json"
    with open(settings_file, "w") as f:
        json.dump(settings, f)
    return settings_file


def test_get_exchange_rates(mock_api_key, mock_settings_file):
    """Тест для функции get_exchange_rates"""
    to_currency = "RUB"
    from_currency = "EUR"
    expected_result = {"rates": {"RUB": 1.2, "EUR": 0.8}}

    with patch("src.utils.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_result

    result = get_exchange_rates(to_currency, from_currency, 100.0)
    assert result == expected_result

def test_get_stock_prices(mock_api_key, mock_settings_file):
    """Тест для функции get_stock_prices"""
    date = "2023-01-01"
    expected_result = {"AAPL": 150.0, "MSFT": 200.0, "GOOGL": 300.0}
    with patch("src.utils.requests.get") as mock_get:
        for symbol in ["AAPL", "MSFT", "GOOGL"]:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"results": [{"c": expected_result[symbol]}]}

        result = get_stock_prices(mock_api_key, mock_settings_file, date)
        assert result[symbol] == expected_result[symbol]
