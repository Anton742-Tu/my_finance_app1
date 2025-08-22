from datetime import datetime, timedelta
from typing import Any, Dict, List, Literal

import pandas as pd
from fastapi import APIRouter

from src.services.excel_processor import load_operations_from_excel  # Добавляем импорт
from src.services.finance_api import get_currency_rates, get_stock_prices

router = APIRouter()


def get_date_range(date: datetime, period: str) -> tuple[datetime, datetime]:
    if period == "W":
        start = date - timedelta(days=date.weekday())
    elif period == "M":
        start = date.replace(day=1)
    elif period == "Y":
        start = date.replace(month=1, day=1)
    else:  # ALL
        start = datetime(1970, 1, 1)
    return start, date


def get_transactions(start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    """Получает транзакции для указанного периода"""
    # Загружаем операции из Excel
    operations = load_operations_from_excel("data/operations.xlsx")

    # Фильтруем по дате
    filtered_ops = [op for op in operations if start_date <= op.date <= end_date]

    # Преобразуем в список словарей для pandas
    return [op.to_dict() for op in filtered_ops]


@router.get("/events/{date_str}")
async def events_page(date_str: str, period: Literal["W", "M", "Y", "ALL"] = "M") -> Dict[str, Any]:
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date, end_date = get_date_range(date, period)

    # Теперь get_transactions возвращает реальные данные
    transactions_data = get_transactions(start_date, end_date)
    df = pd.DataFrame(transactions_data)

    # Расходы
    expenses = df[df["amount"] < 0]
    expenses_by_category = expenses.groupby("category")["amount"].sum().abs()
    top_expenses = expenses_by_category.nlargest(7)
    other_expenses = expenses_by_category.sum() - top_expenses.sum()

    # Поступления
    income = df[df["amount"] > 0]

    return {
        "expenses": {
            "total": round(expenses["amount"].abs().sum()),
            "main_categories": [{"category": k, "amount": round(v)} for k, v in top_expenses.items()],
            "other": round(other_expenses),
        },
        "income": {
            "total": round(income["amount"].sum()),
            "categories": [
                {"category": k, "amount": round(v)} for k, v in income.groupby("category")["amount"].sum().items()
            ],
        },
        "currencies": get_currency_rates(),
        "stocks": get_stock_prices(),
    }
