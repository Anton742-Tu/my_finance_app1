import pytest
from datetime import datetime
import pandas as pd
from src.reports import get_category_spending, get_weekday_spending, get_workday_spending


@pytest.fixture
def sample_transactions():
    """Генерирует тестовые данные"""
    dates = pd.date_range(end=datetime.now(), periods=90).to_pydatetime().tolist()
    categories = ["Food", "Transport", "Entertainment"] * 30
    amounts = [-100, -200, -300] * 30

    return pd.DataFrame({"Дата операции": dates, "Категория": categories, "Сумма операции": amounts})


def test_category_spending(sample_transactions):
    result = get_category_spending(sample_transactions, 'Food')

    assert 'monthly_spending' in result
    assert len(result['monthly_spending']) == 3  # Ровно 3 месяца
    assert 'total' in result
    assert result['total'] > 0  # Общая сумма трат

    # Проверяем, что все значения в отчете - числа
    assert all(isinstance(v, (int, float))
               for v in result['monthly_spending'].values())


def test_weekday_spending(sample_transactions):
    result = get_weekday_spending(sample_transactions)
    assert len(result["average_spending"]) == 7  # 7 дней недели
    assert all(v >= 0 for v in result["average_spending"].values())


def test_workday_spending(sample_transactions):
    result = get_workday_spending(sample_transactions)
    assert "weekdays" in result["average_spending"]
    assert "weekends" in result["average_spending"]
