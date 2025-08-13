from datetime import datetime

from models.operations import Operation
from src.services.data_processor import get_transactions


def test_get_transactions(test_db):
    # Добавляем тестовые данные
    test_operation = Operation(date=datetime(2023, 1, 1), amount=100.0, category="Test")
    test_db.add(test_operation)
    test_db.commit()

    # Тестируем
    result = get_transactions(start_date=datetime(2023, 1, 1), end_date=datetime(2023, 1, 2), db=test_db)

    assert len(result) == 1
    assert result[0]["amount"] == 100.0
