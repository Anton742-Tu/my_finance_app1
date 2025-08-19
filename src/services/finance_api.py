import requests
from typing import Dict
from src.config import settings
import json
from pathlib import Path


def get_currency_rates() -> Dict[str, float]:
    """Получает курсы валют"""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        response.raise_for_status()
        data = response.json()

        return {curr: data['rates'].get(curr, 0.0) for curr in settings.supported_currencies}

    except Exception:
        return {curr: 0.0 for curr in settings.supported_currencies}


def get_stock_prices() -> Dict[str, float]:
    """Получает цены акций"""
    try:
        prices = {}
        for stock in settings.supported_stocks:
            try:
                response = requests.get(f"https://api.iextrading.com/1.0/stock/{stock}/price", timeout=3)
                prices[stock] = float(response.text)
            except:
                prices[stock] = 0.0
        return prices

    except Exception:
        return {stock: 0.0 for stock in settings.supported_stocks}


def _load_config():
    config_paths = [
        Path("config/user_settings.json"),
        Path("src/config/user_settings.json"),
        Path("user_settings.json")
    ]

    for path in config_paths:
        if path.exists():
            return json.loads(path.read_text())

    # Конфиг по умолчанию
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "GOOGL"]
    }


CONFIG = _load_config()
