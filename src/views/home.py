from datetime import datetime

from src.services.analyzer import analyze_spending, calculate_cashback, get_top_transactions
from src.services.excel_processor import load_operations_from_excel
from src.services.finance_api import get_currency_rates, get_stock_prices


def get_home_data(excel_path: str, target_date: datetime) -> dict:
    """Генерирует данные для главной страницы"""
    operations = load_operations_from_excel(excel_path)

    start_date = target_date.replace(day=1)
    monthly_ops = [op for op in operations if start_date <= op.date <= target_date]

    analysis = analyze_spending(monthly_ops)

    return {
        "greeting": get_greeting(target_date),
        "total_spent": analysis["total_spent"],
        "cashback": calculate_cashback(monthly_ops),
        "top_transactions": get_top_transactions(monthly_ops, 5),
        "currencies": get_currency_rates(),
        "stocks": get_stock_prices(),
    }


def get_greeting(date: datetime) -> str:
    hour = date.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
