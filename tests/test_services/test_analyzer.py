from datetime import datetime
from decimal import Decimal
from typing import List

import pytest

from src.models.operation import Operation
from src.services.analyzer import analyze_spending, calculate_cashback, get_top_transactions


@pytest.fixture
def sample_operations() -> List[Operation]:
    """Тестовые операции: 2 расхода и 1 доход"""
    return [
        Operation(
            date=datetime(2023, 1, 1, 12, 0),
            payment_date=datetime(2023, 1, 2),
            card_number="*1234",
            status="OK",
            amount=Decimal("100.00"),  # Расход
            currency="RUB",
            cashback=Decimal("1.00"),
            category="Food",
            mcc=5411,
            description="Lunch",
            bonuses=Decimal("2.00"),
            rounding=Decimal("0.00"),
        ),
        Operation(
            date=datetime(2023, 1, 2, 13, 0),
            payment_date=datetime(2023, 1, 3),
            card_number="*5678",
            status="OK",
            amount=Decimal("200.00"),  # Расход
            currency="RUB",
            cashback=Decimal("2.00"),
            category="Transport",
            mcc=4121,
            description="Taxi",
            bonuses=Decimal("3.00"),
            rounding=Decimal("0.00"),
        ),
        Operation(
            date=datetime(2023, 1, 3, 14, 0),
            payment_date=datetime(2023, 1, 4),
            card_number="*9012",
            status="OK",
            amount=Decimal("-50.00"),
            currency="RUB",
            cashback=Decimal("0.00"),
            category="Income",
            mcc=None,
            description="Salary",
            bonuses=Decimal("0.00"),
            rounding=Decimal("0.00"),
        ),
    ]


def test_analyze_spending(sample_operations: List[Operation]) -> None:
    """Тест анализа расходов (должны учитываться только положительные суммы)"""
    result = analyze_spending(sample_operations)

    assert result["total_spent"] == Decimal("300.00")  # 100 + 200
    assert result["by_category"]["Food"] == Decimal("100.00")
    assert result["by_category"]["Transport"] == Decimal("200.00")
    assert "Income" not in result["by_category"]


def test_get_top_transactions(sample_operations: List[Operation]) -> None:
    """Тест получения топ операций по сумме"""
    top_ops = get_top_transactions(sample_operations, 2)

    assert len(top_ops) == 2
    assert top_ops[0].amount == Decimal("200.00")
    assert top_ops[1].amount == Decimal("100.00")


def test_calculate_cashback(sample_operations: List[Operation]) -> None:
    """Тест расчета кешбэка"""
    cashback = calculate_cashback(sample_operations)
    assert cashback == Decimal("3.00")  # 1.00 + 2.00 + 0.00
