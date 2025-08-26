from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

import numpy as np
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
                "Дата операции": _handle_nan_value(row.get("Дата операции")),
                "Дата платежа": _handle_nan_value(row.get("Дата платежа")),
                "Номер карты": _handle_nan_value(row.get("Номер карты", "")),
                "Статус": _handle_nan_value(row.get("Статус", "OK")),
                "Сумма операции": _handle_nan_value(row.get("Сумма операции")),
                "Валюта операции": _handle_nan_value(row.get("Валюта операции", "RUB")),
                "Кэшбэк": _handle_nan_value(row.get("Кэшбэк", "0")),
                "Категория": _handle_nan_value(row.get("Категория", "")),
                "MCC": _handle_nan_value(row.get("MCC")),
                "Описание": _handle_nan_value(row.get("Описание", "")),
                "Бонусы (включая кэшбэк)": _handle_nan_value(row.get("Бонусы (включая кэшбэк)", "0")),
                "Округление на инвесткопилку": _handle_nan_value(row.get("Округление на инвесткопилку", "0")),
            }

            if operation_data["Дата операции"] in [None, "nan", ""]:
                continue

            operation = Operation.from_dict(operation_data)
            operations.append(operation)

        except Exception as e:
            print(f"Ошибка обработки строки: {e}")
            continue

    return operations


def _handle_nan_value(value: Any) -> Optional[str]:
    """Обрабатывает NaN значения из pandas"""
    if pd.isna(value) or value in [None, np.nan, "nan", "NaN", "NAN"]:
        return None
    return str(value) if value is not None else None


def filter_operations_by_date(
    operations: List[Operation], start_date: datetime, end_date: datetime
) -> List[Operation]:
    """Фильтрует операции по дате"""
    return [op for op in operations if start_date <= op.date <= end_date]
