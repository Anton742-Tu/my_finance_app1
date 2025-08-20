from datetime import datetime
from decimal import Decimal

from src.models.operation import Operation


def test_operation_creation() -> None:
    """Тест создания операции"""
    op = Operation(
        date=datetime(2023, 1, 1, 12, 0),
        payment_date=datetime(2023, 1, 2),
        card_number="*1234",
        status="OK",
        amount=Decimal("100.50"),
        currency="RUB",
        cashback=Decimal("1.50"),
        category="Food",
        mcc=5411,
        description="Lunch",
        bonuses=Decimal("2.00"),
        rounding=Decimal("0.00"),
    )

    assert op.amount == Decimal("100.50")
    assert op.category == "Food"
    assert op.mcc == 5411


def test_operation_from_dict() -> None:
    """Тест создания операции из словаря"""
    data = {
        "Дата операции": "01.01.2023 12:00:00",
        "Дата платежа": "02.01.2023",
        "Номер карты": "*1234",
        "Статус": "OK",
        "Сумма операции": "-100,50",
        "Валюта операции": "RUB",
        "Кэшбэк": "1,50",
        "Категория": "Food",
        "MCC": "5411",
        "Описание": "Lunch",
        "Бонусы (включая кэшбэк)": "2,00",
        "Округление на инвесткопилку": "0,00",
    }

    op = Operation.from_dict(data)
    assert op.amount == Decimal("100.50")
    assert op.cashback == Decimal("1.50")
    assert op.category == "Food"


def test_operation_to_dict() -> None:
    """Тест преобразования операции в словарь"""
    op = Operation(
        date=datetime(2023, 1, 1, 12, 0),
        payment_date=datetime(2023, 1, 2),
        card_number="*1234",
        status="OK",
        amount=Decimal("100.50"),
        currency="RUB",
        cashback=Decimal("1.50"),
        category="Food",
        mcc=5411,
        description="Lunch",
        bonuses=Decimal("2.00"),
        rounding=Decimal("0.00"),
    )

    result = op.to_dict()
    assert result["amount"] == 100.50
    assert result["category"] == "Food"
    assert result["date"] == "2023-01-01T12:00:00"


def test_operation_missing_data() -> None:
    """Тест обработки отсутствующих данных"""
    data = {
        "Дата операции": "01.01.2023 12:00:00",
        "Дата платежа": "02.01.2023",
        "Сумма операции": "-100,50",
        # Остальные поля отсутствуют
    }

    op = Operation.from_dict(data)
    assert op.amount == Decimal("100.50")
    assert op.currency == "RUB"  # Значение по умолчанию
    assert op.cashback == Decimal("0")  # Значение по умолчанию
    assert op.category == ""  # Значение по умолчанию
