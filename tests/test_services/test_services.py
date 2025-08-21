from datetime import datetime
from decimal import Decimal

import pytest

from src.services.services import *


@pytest.fixture
def sample_transactions() -> List[Transaction]:
    return [
        {
            "date": "2024-01-15",
            "amount": -1000.0,
            "category": "Супермаркеты",
            "description": "Пятерочка",
            "cashback": 50.0,
        },
        {
            "date": "2024-01-20",
            "amount": -500.0,
            "category": "Такси",
            "description": "Яндекс Такси +7 921 123-45-67",
            "cashback": 25.0,
        },
        {"date": "2024-02-01", "amount": -200.0, "category": "Переводы", "description": "Иван С.", "cashback": 0.0},
    ]


def test_analyze_cashback_categories(sample_transactions):
    result = analyze_cashback_categories(sample_transactions, 2024, 1)
    assert "Супермаркеты" in result
    assert result["Супермаркеты"] == 50.0
    assert "Такси" in result
    assert result["Такси"] == 25.0


def test_investment_bank():
    transactions = [{"date": "2024-01-15", "amount": -123.0}, {"date": "2024-01-20", "amount": -477.0}]
    result = investment_bank("2024-01", transactions, 100)
    assert result == 100  # (200-123) + (500-477) = 77 + 23 = 100


def test_simple_search(sample_transactions):
    result = simple_search(sample_transactions, "Такси")
    assert len(result) == 1
    assert result[0]["category"] == "Такси"


def test_find_phone_transactions(sample_transactions):
    result = find_phone_transactions(sample_transactions)
    assert len(result) == 1
    assert "921" in result[0]["description"]


def test_find_person_transfers(sample_transactions):
    result = find_person_transfers(sample_transactions)
    assert len(result) == 1
    assert result[0]["category"] == "Переводы"
