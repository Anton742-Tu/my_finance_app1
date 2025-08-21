from datetime import datetime  # Добавляем импорт datetime
from pathlib import Path
from typing import List

import pandas as pd

from src.models.operation import Operation


def load_operations_from_excel(file_path: str) -> List[Operation]:
    """Загружает операции из Excel файла"""
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    df = pd.read_excel(file_path)
    operations = []

    for _, row in df.iterrows():
        try:
            operation_data = {
                "Дата операции": str(row["Дата операции"]),
                "Дата платежа": str(row["Дата платежа"]),
                "Номер карты": str(row.get("Номер карты", "")),
                "Статус": str(row.get("Статус", "OK")),
                "Сумма операции": str(row["Сумма операции"]),
                "Валюта операции": str(row.get("Валюта операции", "RUB")),
                "Кэшбэк": str(row.get("Кэшбэк", 0)),
                "Категория": str(row.get("Категория", "")),
                "MCC": row.get("MCC"),
                "Описание": str(row.get("Описание", "")),
                "Бонусы (включая кэшбэк)": str(row.get("Бонусы (включая кэшбэк)", 0)),
                "Округление на инвесткопилку": str(row.get("Округление на инвесткопилку", 0)),
            }

            operation = Operation.from_dict(operation_data)
            operations.append(operation)

        except Exception as e:
            print(f"Ошибка обработки строки: {e}")
            continue

    return operations


def filter_operations_by_date(
    operations: List[Operation], start_date: datetime, end_date: datetime
) -> List[Operation]:
    """Фильтрует операции по дате"""
    return [op for op in operations if start_date <= op.date <= end_date]
