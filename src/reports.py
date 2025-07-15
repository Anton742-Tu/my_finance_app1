import json
import pandas as pd
from datetime import datetime, timedelta
from functools import wraps
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)


# Декоратор для сохранения отчетов
def report_to_file(default_filename: str = None):
    def decorator(report_func: Callable):
        @wraps(report_func)
        def wrapper(*args, filename: str = None, **kwargs):
            result = report_func(*args, **kwargs)

            output_filename = filename or default_filename
            if not output_filename:
                # Генерируем имя файла по умолчанию
                func_name = report_func.__name__
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{func_name}_{timestamp}.json"

            try:
                with open(output_filename, "w", encoding="utf-8") as f:
                    if isinstance(result, (dict, list)):
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    else:
                        f.write(str(result))
                logger.info(f"Отчет сохранен в файл: {output_filename}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")

            return result

        return wrapper

    # Если декоратор вызывается без параметров
    if callable(default_filename):
        func = default_filename
        default_filename = None
        return decorator(func)

    return decorator


# 1. Траты по категории
@report_to_file("category_spending.json")
def get_category_spending(
        df: pd.DataFrame,
        category: str,
        target_date: Optional[datetime] = None
) -> dict:
    """Возвращает траты по категории за последние 3 месяца"""
    target_date = target_date or datetime.now()
    three_months_ago = target_date - timedelta(days=90)

    # Фильтрация данных с учетом отрицательных сумм (траты)
    filtered = df[
        (df['Категория'] == category) &
        (df['Дата операции'] >= three_months_ago) &
        (df['Дата операции'] <= target_date) &
        (df['Сумма операции'] < 0)  # Только траты
        ]

    # Группировка по месяцам с абсолютными значениями
    monthly = filtered.groupby(
        filtered['Дата операции'].dt.to_period('M')
    )['Сумма операции'].sum().abs()

    # Нормализуем до ровно 3 месяцев
    all_months = pd.period_range(
        start=three_months_ago,
        end=target_date,
        freq='M'
    )[-3:]  # Берем последние 3 месяца

    result = {
        month: float(monthly.get(month, 0))
        for month in all_months
    }

    return {
        'category': category,
        'period': f"{three_months_ago.date()} - {target_date.date()}",
        'monthly_spending': {str(k): v for k, v in result.items()},
        'total': float(monthly.sum())
    }


# 2. Траты по дням недели
@report_to_file("weekday_spending.json")
def get_weekday_spending(df: pd.DataFrame, target_date: Optional[datetime] = None) -> dict:
    """Возвращает средние траты по дням недели"""
    target_date = target_date or datetime.now()
    three_months_ago = target_date - timedelta(days=90)

    filtered = df[(df["Дата операции"] >= three_months_ago) & (df["Дата операции"] <= target_date)]

    # Добавляем день недели (0 - понедельник, 6 - воскресенье)
    filtered["weekday"] = filtered["Дата операции"].dt.weekday
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    result = filtered.groupby("weekday")["Сумма операции"].mean().abs().to_dict()

    return {
        "period": f"{three_months_ago.date()} - {target_date.date()}",
        "average_spending": {weekdays[k]: round(v, 2) for k, v in result.items()},
    }


# 3. Траты в рабочие/выходные дни
@report_to_file("workday_spending.json")
def get_workday_spending(df: pd.DataFrame, target_date: Optional[datetime] = None) -> dict:
    """Сравнивает траты в рабочие и выходные дни"""
    target_date = target_date or datetime.now()
    three_months_ago = target_date - timedelta(days=90)

    filtered = df[(df["Дата операции"] >= three_months_ago) & (df["Дата операции"] <= target_date)]

    # Определяем рабочие дни (0-4 - пн-пт)
    filtered["is_weekend"] = filtered["Дата операции"].dt.weekday >= 5
    result = filtered.groupby("is_weekend")["Сумма операции"].mean().abs().to_dict()

    return {
        "period": f"{three_months_ago.date()} - {target_date.date()}",
        "average_spending": {"weekdays": round(result.get(False, 0), 2), "weekends": round(result.get(True, 0), 2)},
    }
