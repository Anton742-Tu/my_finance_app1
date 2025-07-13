import pandas as pd
from .models import Transaction

class FinanceAnalyzer:
    @staticmethod
    def load_transactions(file_path: str) -> list[Transaction]:
        df = pd.read_excel(file_path)
        return [Transaction(**row) for row in df.to_dict("records")]

    def calculate_stats(self, transactions: list[Transaction]) -> dict:
        # Анализ суммы, категорий и т.д.
        pass