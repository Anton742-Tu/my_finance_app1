import requests
import json
from pathlib import Path

CONFIG = json.loads(Path("config/user_settings.json").read_text())

def get_currency_rates() -> dict:
    try:
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/USD"
        )
        return {
            curr: response.json()['rates'][curr]
            for curr in CONFIG['user_currencies']
        }
    except Exception:
        return {curr: 0 for curr in CONFIG['user_currencies']}

def get_stock_prices() -> dict:
    try:
        return {
            stock: requests.get(
                f"https://api.iextrading.com/1.0/stock/{stock}/price"
            ).json()
            for stock in CONFIG['user_stocks']
        }
    except Exception:
        return {stock: 0 for stock in CONFIG['user_stocks']}