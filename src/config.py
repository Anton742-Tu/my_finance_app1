from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    excel_file_path: str = "data/operations.xlsx"
    supported_currencies: List[str] = ["USD", "EUR", "GBP", "CNY"]
    supported_stocks: List[str] = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

    class Config:
        env_file = ".env"


settings = Settings()
