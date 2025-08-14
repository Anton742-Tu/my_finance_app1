import json
from pathlib import Path
from typing import Dict
import requests


def _get_config_path():
    # Пробуем найти конфиг в разных местах
    paths = [
        Path("config/user_settings.json"),
        Path("tests/test_config/user_settings.json"),
        Path("src/config/user_settings.json"),
    ]
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("Не найден файл конфигурации")


CONFIG = json.loads(_get_config_path().read_text(encoding="utf-8"))


def get_currency_rates() -> Dict[str, float]:
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        response.raise_for_status()
        return {curr: float(response.json()["rates"][curr]) for curr in CONFIG["user_currencies"]}
    except Exception:
        return {curr: 0.0 for curr in CONFIG["user_currencies"]}
