from datetime import datetime, timedelta
from fastapi import APIRouter
import pandas as pd
from typing import Literal
from src.services.finance_api import get_currency_rates, get_stock_prices
from src.services.data_processor import get_transactions

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


@router.get("/events/{date_str}")
async def events_page(date_str: str, period: Literal["W", "M", "Y", "ALL"] = "M"):
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date, end_date = get_date_range(date, period)

    df = pd.DataFrame(get_transactions(start_date, end_date))

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
