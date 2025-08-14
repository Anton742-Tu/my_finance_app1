from datetime import datetime
from src.services.data_processor import get_transactions

def test_get_transactions(db, test_operations):
    """Тест получения операций за период"""
    result = get_transactions(
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 1, 31),
        db=db
    )
    assert len(result) == 2
    assert {op["amount"] for op in result} == {100.0, 200.0}

def test_get_transactions_empty_period(db, test_operations):
    """Тест пустого периода"""
    result = get_transactions(
        start_date=datetime(2023, 2, 1),
        end_date=datetime(2023, 2, 28),
        db=db
    )
    assert len(result) == 0

def test_get_transactions_all_data(db, test_operations):
    """Тест получения всех данных"""
    result = get_transactions(
        start_date=datetime(2022, 1, 1),
        end_date=datetime(2024, 1, 1),
        db=db
    )
    assert len(result) == 2
