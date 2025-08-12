import logging
from datetime import datetime
from fastapi import APIRouter
import pandas as pd
from src.services.finance_api import get_currency_rates, get_stock_prices
from src.services.data_processor import get_transactions

router = APIRouter()
logger = logging.getLogger(__name__)


def get_greeting(time: datetime) -> str:
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


@router.get("/home/{date_str}")
async def home_page(date_str: str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        start_date = date.replace(day=1, hour=0, minute=0, second=0)

        # Получаем данные
        transactions = get_transactions(start_date, date)
        currencies = get_currency_rates()
        stocks = get_stock_prices()

        # Обработка транзакций
        df = pd.DataFrame(transactions)
        card_stats = df.groupby('card_number').agg(
            total_spent=('amount', 'sum'),
            cashback=('amount', lambda x: sum(x) // 100)
        ).reset_index()

        top_transactions = df.nlargest(5, 'amount')

        return {
            "greeting": get_greeting(date),
            "cards": [
                {
                    "last_digits": str(card)[-4:],
                    "total_spent": round(total),
                    "cashback": cashback
                } for card, total, cashback in card_stats.itertuples(index=False)
            ],
            "top_transactions": top_transactions.to_dict('records'),
            "currencies": currencies,
            "stocks": stocks
        }

    except Exception as e:
        logger.error(f"Error in home_page: {e}")
        raise