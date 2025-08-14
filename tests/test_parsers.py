import pandas as pd
import pytest
from src.utils.parsers import parse_excel_to_db
from src.models.operations import Operation

@pytest.fixture
def valid_excel(tmp_path):
    """Создает корректный тестовый Excel файл"""
    file_path = tmp_path / "valid_operations.xlsx"
    data = {
        'Дата операции': ['01.01.2023 12:00:00'],
        'Дата платежа': ['02.01.2023'],
        'Номер карты': ['*1234'],
        'Статус': ['OK'],
        'Сумма операции': ['-100,50'],
        'Валюта операции': ['RUB'],
        'Кэшбэк': ['1,50'],
        'Категория': ['Супермаркеты'],
        'MCC': [5411],
        'Описание': ['Покупка продуктов'],
        'Бонусы (включая кэшбэк)': ['2,00'],
        'Округление на инвесткопилку': ['0,00']
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    return file_path

@pytest.fixture
def invalid_excel(tmp_path):
    """Создает файл с неполными данными"""
    file_path = tmp_path / "invalid_operations.xlsx"
    df = pd.DataFrame({'Некорректная колонка': [1, 2, 3]})
    df.to_excel(file_path, index=False)
    return file_path

def test_parse_valid_excel(db, valid_excel):
    """Тест с корректными данными"""
    parse_excel_to_db(str(valid_excel))
    op = db.query(Operation).first()
    assert op is not None
    assert op.amount == 100.50
    assert op.category == "Супермаркеты"

def test_parse_invalid_excel(db, invalid_excel):
    """Тест с некорректными данными"""
    with pytest.raises(KeyError):
        parse_excel_to_db(str(invalid_excel))
    assert db.query(Operation).count() == 0
