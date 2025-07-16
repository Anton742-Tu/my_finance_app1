import pytest
from src.services import *
from src.models import Transaction

@pytest.fixture
def rounding_test_data():
    return [
        {"operation_date": "2023-01-01", "amount": 1712.0},
        {"operation_date": "2023-01-02", "amount": 123.0}
    ]


@pytest.fixture
def sample_transactions() -> List[Transaction]:
    return [
        {
            "operation_date": "2023-01-15",
            "amount": -1000.0,
            "category": "Supermarkets",
            "description": "Grocery",
            "cashback": 50.0
        },
        {
            "operation_date": "2023-01-20",
            "amount": -500.0,
            "category": "Restaurants",
            "description": "Cafe",
            "cashback": 25.0
        },
        {
            "operation_date": "2023-02-10",
            "amount": -1712.0,
            "category": "Electronics",
            "description": "Phone +7 921 11-22-33",
            "cashback": 0.0
        },
        {
            "operation_date": "2023-01-05",
            "amount": -2000.0,
            "category": "Transfers",
            "description": "Валерий А.",
            "cashback": 0.0
        }
    ]

def test_analyze_cashback(sample_transactions):
    result = analyze_cashback(sample_transactions, 2023, 1)
    assert result == {"Supermarkets": 50.0, "Restaurants": 25.0}

def test_investment_bank(sample_transactions):
    # Добавляем правильные данные для теста округления
    test_data = [
        {"operation_date": "2023-01-01", "amount": 1712.0},  # Округление 38 (1750-1712)
        {"operation_date": "2023-01-02", "amount": 123.0}    # Округление 27 (150-123)
    ]
    amount = investment_bank("2023-01", test_data, 50)
    assert amount == 38 + 27  # 65

def test_find_phone_transactions(sample_transactions):
    # Исправляем тестовые данные для поиска телефона
    test_data = [
        {"description": "Payment +7 921 123-45-67"},
        {"description": "No phone here"}
    ]
    result = find_phone_transactions(test_data)
    assert len(result) == 1
    assert "+7 921 123-45-67" in result[0]["description"]

def test_simple_search(sample_transactions):
    result = simple_search(sample_transactions, "Grocery")
    assert len(result) == 1
    assert result[0]["category"] == "Supermarkets"

def test_find_person_transfers(sample_transactions):
    result = find_person_transfers(sample_transactions)
    assert len(result) == 1
    assert result[0]["description"] == "Валерий А."