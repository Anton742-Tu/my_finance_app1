import logging
from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Optional, Literal

from fastapi import APIRouter

from .api_client import get_currency_rates, get_stock_prices
from .config import load_user_settings
from .services import get_card_stats, get_top_transactions, get_spending_analysis, get_income_analysis

router = APIRouter()
logger = logging.getLogger(__name__)


def get_time_greeting(current_time: datetime) -> str:
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


@router.get("/dashboard")
async def dashboard_view(date_time: str):
    """Главная страница"""
    try:
        current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        start_date = current_time.replace(day=1, hour=0, minute=0, second=0)

        # Получаем данные
        greeting = get_time_greeting(current_time)
        cards_data = await get_card_stats(start_date, current_time)
        top_transactions = await get_top_transactions(start_date, current_time, limit=5)

        # Внешние API
        settings = load_user_settings()
        currencies = await get_currency_rates(settings["user_currencies"])
        stocks = await get_stock_prices(settings["user_stocks"])

        return {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "currencies": currencies,
            "stocks": stocks,
        }

    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        raise HTTPException(detail=str(e))


@router.get("/events")
async def events_view(date_time: str, period: Optional[Literal["W", "M", "Y", "ALL"]] = "M"):
    """Страница событий"""
    try:
        end_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

        # Определяем диапазон дат
        if period == "W":
            start_date = end_date - timedelta(days=end_date.weekday())
        elif period == "M":
            start_date = end_date.replace(day=1)
        elif period == "Y":
            start_date = end_date.replace(month=1, day=1)
        else:  # ALL
            start_date = datetime.min

        # Анализ данных
        spending = await get_spending_analysis(start_date, end_date)
        income = await get_income_analysis(start_date, end_date)

        # Внешние данные
        settings = load_user_settings()
        currencies = await get_currency_rates(settings["user_currencies"])
        stocks = await get_stock_prices(settings["user_stocks"])

        return {"spending": spending, "income": income, "currencies": currencies, "stocks": stocks}

    except Exception as e:
        logger.error(f"Events error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


def app():
    return None
