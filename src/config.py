from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Пути к файлам
    excel_file_path: str = "data/operations.xlsx"
    user_settings_path: str = "user_settings.json"
    report_dir: str = "reports"

    # API endpoints
    currency_api_url: str = "https://api.exchangerate-api.com/v4/latest/USD"
    stock_api_base: str = "https://api.iextrading.com/1.0/stock"

    # Списки данных
    supported_currencies: List[str] = ["USD", "EUR", "GBP", "CNY"]
    supported_stocks: List[str] = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

    # Форматы
    default_date_format: str = "%Y-%m-%d %H:%M:%S"

    # Логирование
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_prefix = "FINANCE_"
        case_sensitive = False


settings = Settings()
