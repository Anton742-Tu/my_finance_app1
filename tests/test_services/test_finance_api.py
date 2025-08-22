from typing import Any, Dict  # Добавляем импорты для типов
from unittest.mock import Mock, patch

from src.services.finance_api import get_currency_rates, get_stock_prices


@patch("requests.get")
def test_get_currency_rates_success(mock_get: Mock) -> None:
    """Тест успешного получения курсов валют"""
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85, "GBP": 0.75, "CNY": 7.0}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_currency_rates()

    assert result["USD"] == 1.0
    assert result["EUR"] == 0.85
    assert result["GBP"] == 0.75
    assert result["CNY"] == 7.0


@patch("requests.get")
def test_get_currency_rates_failure(mock_get: Mock) -> None:
    """Тест обработки ошибки при получении курсов"""
    mock_get.side_effect = Exception("API error")

    result = get_currency_rates()

    # Должны вернуться заглушки
    assert result["USD"] == 1.0
    assert result["EUR"] == 0.85


@patch("requests.get")
def test_get_stock_prices_success(mock_get: Mock) -> None:
    """Тест успешного получения цен акций"""
    mock_get.return_value.text = "150.0"

    result = get_stock_prices()

    # Проверяем, что возвращаются значения (мок срабатывает только на первый вызов)
    assert len(result) > 0
