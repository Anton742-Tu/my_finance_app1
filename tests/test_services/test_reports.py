import pandas as pd
import pytest

from src.services.reports import category_spending_report, weekday_spending_report, workday_weekend_spending_report


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Тестовый DataFrame с транзакциями"""
    data = {
        "date": ["2024-01-15", "2024-01-20", "2024-02-01", "2024-02-15", "2024-03-01"],
        "amount": [-1000.0, -500.0, -200.0, -300.0, -150.0],
        "category": ["Супермаркеты", "Такси", "Супермаркеты", "Такси", "Супермаркеты"],
        "description": ["Пятерочка", "Яндекс Такси", "Магнит", "Uber", "Ашан"],
    }
    return pd.DataFrame(data)


def test_category_spending_report(sample_dataframe: pd.DataFrame) -> None:
    """Тест отчета по категории"""
    result = category_spending_report(sample_dataframe, "Супермаркеты", "2024-03-01")
    assert "2024-03" in result
    assert "2024-01" in result


def test_weekday_spending_report(sample_dataframe: pd.DataFrame) -> None:
    """Тест отчета по дням недели"""
    result = weekday_spending_report(sample_dataframe, "2024-03-01")
    assert isinstance(result, dict)
    assert len(result) > 0


def test_workday_weekend_spending_report(sample_dataframe: pd.DataFrame) -> None:
    """Тест отчета рабочие/выходные дни"""
    result = workday_weekend_spending_report(sample_dataframe, "2024-03-01")
    assert "workday" in result
    assert "weekend" in result
