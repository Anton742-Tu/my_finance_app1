from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from src.models.operation import Operation
from src.views.home import get_greeting, get_home_data


@pytest.fixture
def mock_operation() -> Operation:
    """Создает тестовую операцию"""
    return Operation(
        date=datetime(2023, 1, 10, 12, 0),
        payment_date=datetime(2023, 1, 11),
        card_number="*1234",
        status="OK",
        amount=Decimal("100.00"),
        currency="RUB",
        cashback=Decimal("1.00"),
        category="Food",
        mcc=5411,
        description="Lunch",
        bonuses=Decimal("2.00"),
        rounding=Decimal("0.00"),
    )


@patch("src.views.home.load_operations_from_excel")
@patch("src.views.home.analyze_spending")
@patch("src.views.home.calculate_cashback")
@patch("src.views.home.get_top_transactions")
@patch("src.views.home.get_currency_rates")
@patch("src.views.home.get_stock_prices")
def test_get_home_data(
    mock_stocks: Mock,
    mock_currency: Mock,
    mock_top: Mock,
    mock_cashback: Mock,
    mock_analyze: Mock,
    mock_load: Mock,
    mock_operation: Operation,
) -> None:
    """Тест получения данных для главной страницы"""
    mock_load.return_value = [mock_operation]
    mock_analyze.return_value = {"total_spent": Decimal("100.00"), "by_category": {"Food": Decimal("100.00")}}
    mock_cashback.return_value = Decimal("1.00")
    mock_top.return_value = [mock_operation]
    mock_currency.return_value = {"USD": 75.0, "EUR": 85.0}
    mock_stocks.return_value = {"AAPL": 150.0, "GOOGL": 2800.0}

    result = get_home_data("dummy_path.xlsx", datetime(2023, 1, 15, 12, 0))

    assert result["greeting"] == "Добрый день"
    assert result["total_spent"] == Decimal("100.00")
    assert result["cashback"] == Decimal("1.00")
    assert len(result["top_transactions"]) == 1
    assert result["top_transactions"][0].amount == Decimal("100.00")
    assert "USD" in result["currencies"]
    assert "AAPL" in result["stocks"]

    mock_load.assert_called_once_with("dummy_path.xlsx")
    mock_analyze.assert_called_once()


def test_get_greeting() -> None:
    """Тест приветствия в зависимости от времени"""
    assert get_greeting(datetime(2023, 1, 1, 6, 0)) == "Доброе утро"  # 6:00
    assert get_greeting(datetime(2023, 1, 1, 12, 0)) == "Добрый день"  # 12:00
    assert get_greeting(datetime(2023, 1, 1, 18, 0)) == "Добрый вечер"  # 18:00
    assert get_greeting(datetime(2023, 1, 1, 2, 0)) == "Доброй ночи"  # 2:00
