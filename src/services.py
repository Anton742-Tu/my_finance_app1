import pandas as pd
from src.models import Transaction
from typing import List
import logging

logger = logging.getLogger(__name__)


class FinanceAnalyzer:
    @staticmethod
    def load_transactions(file_path: str) -> List[Transaction]:
        try:
            df = pd.read_excel(file_path)

            # Преобразуем числовые поля
            numeric_cols = [
                "Сумма операции",
                "Сумма платежа",
                "Кэшбэк",
                "Бонусы (включая кэшбэк)",
                "Округление на инвесткопилку",
                "Сумма операции с округлением",
            ]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")

            # Заменяем NaN в текстовых полях
            text_cols = ["Номер карты", "MCC", "Описание"]
            for col in text_cols:
                if col in df.columns:
                    df[col] = df[col].fillna("").astype(str)

            transactions = []
            for _, row in df.iterrows():
                try:
                    transactions.append(Transaction(**row.to_dict()))
                except Exception as e:
                    logger.warning(f"Ошибка в строке {row.to_dict()}: {str(e)}")
            return transactions

        except Exception as e:
            logger.error(f"Ошибка загрузки файла: {str(e)}")
            raise []

    def to_dataframe(self, transactions):
        pass

    def get_stats(self, transactions):
        pass
