import httpx
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


async def get_currency_rates(currencies: List[str]) -> Dict[str, float]:
    """Получение курсов валют через внешнее API"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.exchangerate-api.com/v4/latest/RUB")
            rates = response.json()["rates"]
            return {curr: rates[curr] for curr in currencies if curr in rates}
        except Exception as e:
            logger.error(f"Currency API error: {str(e)}")
            return {}


async def get_stock_prices(stocks: List[str]) -> Dict[str, float]:
    """Получение цен акций"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://financialmodelingprep.com/api/v3/quote/", params={"symbol": ",".join(stocks)}
            )
            return {item["symbol"]: item["price"] for item in response.json()}
        except Exception as e:
            logger.error(f"Stocks API error: {str(e)}")
            return {}
