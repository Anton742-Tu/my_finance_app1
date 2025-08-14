import pytest
from unittest.mock import patch, Mock
from src.services.finance_api import get_currency_rates


@pytest.fixture
def mock_config(tmp_path):
    config = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL"]}
    config_file = tmp_path / "user_settings.json"
    config_file.write_text(
        """{
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL"]
    }"""
    )
    return config_file


@patch("requests.get")
def test_get_currency_rates(mock_get, monkeypatch, tmp_path):
    # Мокаем конфиг
    test_config = tmp_path / "config" / "user_settings.json"
    test_config.parent.mkdir()
    test_config.write_text(
        """{
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL"]
    }"""
    )

    # Мокаем API ответ
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.9, "RUB": 75.0}}
    mock_get.return_value = mock_response

    result = get_currency_rates()
    assert result["USD"] == 1.0
    assert result["EUR"] == 0.9
