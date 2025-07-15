import pytest
from datetime import datetime
from src.models import Transaction


@pytest.fixture
def valid_transaction_data():
    return {
        "Дата операции": datetime(2023, 1, 1, 12, 0),
        "Дата платежа": datetime(2023, 1, 1),
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -100.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -100.0,
        "Валюта платежа": "RUB",
        "Категория": "Food",
        "MCC": "5411",
        "Описание": "Test",
        "Бонусы (включая кэшбэк)": 1.0,
        "Округление на инвесткопилку": 0.0,
        "Сумма операции с округлением": 100.0,
    }


@pytest.fixture
def sample_transaction(valid_transaction_data):
    return Transaction(**valid_transaction_data)
