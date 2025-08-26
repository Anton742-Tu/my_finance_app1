import json
import logging
from pathlib import Path
from typing import Dict, List

import requests


def get_currency_rates() -> Dict[str, float]:
    """Получает курсы валют"""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        response.raise_for_status()
        data = response.json()

        currencies = ["USD", "EUR", "GBP", "CNY"]
        return {curr: data["rates"].get(curr, 0.0) for curr in currencies}

    except Exception:
        return {"USD": 1.0, "EUR": 0.85, "GBP": 0.75, "CNY": 7.0}


def get_stock_prices() -> Dict[str, float]:
    """Получает цены акций"""
    try:
        stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        prices = {}

        for stock in stocks:
            try:
                response = requests.get(f"https://api.iextrading.com/1.0/stock/{stock}/price", timeout=3)
                prices[stock] = float(response.text)
            except Exception as e:
                logging.error(f"Ошибка в risky_operation: {e}")
                prices[stock] = 0.0

        return prices

    except Exception:
        return {"AAPL": 150.0, "GOOGL": 2800.0, "MSFT": 300.0, "TSLA": 250.0, "AMZN": 3300.0}


def _load_config() -> Dict[str, List[str]]:  # Добавить аннотацию
    config_paths = [
        Path("config/user_settings.json"),
        Path("src/config/user_settings.json"),
        Path("user_settings.json"),
    ]

    for path in config_paths:
        if path.exists():
            data = json.loads(path.read_text())
            return {
                "user_currencies": data.get("user_currencies", ["USD", "EUR"]),
                "user_stocks": data.get("user_stocks", ["AAPL", "GOOGL"]),
            }

    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}
