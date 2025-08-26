from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from src.services.excel_processor import filter_operations_by_date, load_operations_from_excel


@pytest.fixture
def sample_excel(tmp_path: Path) -> Path:
    """Создает тестовый Excel файл"""
    file_path = tmp_path / "test_operations.xlsx"

    data = {
        "Дата операции": ["01.01.2023 12:00:00", "02.01.2023 13:00:00"],
        "Дата платежа": ["02.01.2023", "03.01.2023"],
        "Номер карты": ["*1234", "*5678"],
        "Статус": ["OK", "OK"],
        "Сумма операции": ["-100,50", "-200,75"],
        "Валюта операции": ["RUB", "RUB"],
        "Кэшбэк": ["1,50", "2,00"],
        "Категория": ["Food", "Transport"],
        "MCC": [5411, 4121],
        "Описание": ["Lunch", "Taxi"],
        "Бонусы (включая кэшбэк)": ["2,00", "3,00"],
        "Округление на инвесткопилку": ["0,00", "0,00"],
    }

    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    return file_path


def test_load_operations_from_excel(sample_excel: Path) -> None:
    """Тест загрузки операций из Excel"""
    operations = load_operations_from_excel(str(sample_excel))

    assert len(operations) == 2
    assert operations[0].amount == 100.50
    assert operations[1].amount == 200.75
    assert operations[0].category == "Food"
    assert operations[1].category == "Transport"


def test_load_operations_file_not_found() -> None:
    """Тест обработки отсутствующего файла"""
    with pytest.raises(FileNotFoundError):
        load_operations_from_excel("nonexistent.xlsx")


def test_filter_operations_by_date(sample_excel: Path) -> None:
    """Тест фильтрации операций по дате"""
    operations = load_operations_from_excel(str(sample_excel))

    filtered = filter_operations_by_date(operations, datetime(2023, 1, 1), datetime(2023, 1, 1, 23, 59))

    assert len(filtered) == 1
    assert filtered[0].amount == 100.50
