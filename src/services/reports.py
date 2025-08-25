import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Callable, Any, Dict, List, Optional
from functools import wraps
import os

logger = logging.getLogger(__name__)


# Декоратор для записи отчетов в файл
def report_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для записи результатов отчетов в файл.

    Args:
        filename: Имя файла для сохранения. Если None, генерируется автоматически.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Вызываем оригинальную функцию
            result = func(*args, **kwargs)

            # Генерируем имя файла если не указано
            if filename is None:
                report_name = func.__name__
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"report_{report_name}_{timestamp}.json"
            else:
                output_filename = filename

            # Создаем директорию reports если ее нет
            os.makedirs("reports", exist_ok=True)
            filepath = os.path.join("reports", output_filename)

            # Записываем результат в файл
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    if isinstance(result, (dict, list)):
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    else:
                        f.write(str(result))

                logger.info(f"Отчет сохранен в файл: {filepath}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчета: {e}")

            return result

        return wrapper

    return decorator


# 1. Траты по категории
@report_to_file()
def category_spending_report(
        df: pd.DataFrame,
        category: str,
        target_date: Optional[str] = None
) -> Dict[str, float]:
    """
    Возвращает траты по заданной категории за последние три месяца.
    """
    logger.info(f"Генерация отчета по категории: {category}")

    # Определяем целевую дату
    if target_date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(target_date, "%Y-%m-%d")

    # Вычисляем даты за последние 3 месяца
    dates = []
    for i in range(3):
        month_date = current_date - timedelta(days=30 * i)
        dates.append(month_date.strftime("%Y-%m"))

    # Фильтруем данные
    result: Dict[str, float] = {}
    for month in dates:
        monthly_data = df[df['date'].str.startswith(month)]
        category_data = monthly_data[monthly_data['category'] == category]

        # Суммируем траты (отрицательные значения)
        spending = category_data[category_data['amount'] < 0]['amount'].abs().sum()
        result[month] = round(float(spending), 2)

    return result


# 2. Траты по дням недели
@report_to_file()
def weekday_spending_report(
        df: pd.DataFrame,
        target_date: Optional[str] = None
) -> Dict[str, float]:
    """
    Возвращает средние траты по дням недели за последние три месяца.
    """
    logger.info("Генерация отчета по дням недели")

    # Определяем целевую дату
    if target_date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(target_date, "%Y-%m-%d")

    # Фильтруем данные за последние 3 месяца
    start_date_str = (current_date - timedelta(days=90)).strftime("%Y-%m-%d")
    filtered_df = df[df['date'] >= start_date_str]

    # Извлекаем день недели
    filtered_df = filtered_df.copy()
    filtered_df['weekday'] = pd.to_datetime(filtered_df['date']).dt.day_name()

    # Группируем по дням недели и вычисляем средние траты
    weekday_spending: Any = filtered_df[filtered_df['amount'] < 0].groupby('weekday')['amount'].agg(['mean', 'count'])

    result: Dict[str, float] = {}
    for day in weekday_spending.index:
        result[day] = round(abs(float(weekday_spending.loc[day, 'mean'])), 2)

    return result


# 3. Траты в рабочий/ выходной день
@report_to_file()
def workday_weekend_spending_report(
        df: pd.DataFrame,
        target_date: Optional[str] = None
) -> Dict[str, float]:
    """
    Возвращает средние траты в рабочие и выходные дни.
    """
    logger.info("Генерация отчета рабочие/выходные дни")

    # Определяем целевую дату
    if target_date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(target_date, "%Y-%m-%d")

    # Фильтруем данные за последние 3 месяца
    start_date_str = (current_date - timedelta(days=90)).strftime("%Y-%m-%d")
    filtered_df = df[df['date'] >= start_date_str]

    # Определяем рабочие и выходные дни
    filtered_df = filtered_df.copy()
    filtered_df['date_dt'] = pd.to_datetime(filtered_df['date'])
    filtered_df['is_weekend'] = filtered_df['date_dt'].dt.weekday >= 5  # 5-6 = суббота-воскресенье

    # Группируем и вычисляем средние траты
    day_type_spending: Any = filtered_df[filtered_df['amount'] < 0].groupby('is_weekend')['amount'].agg(['mean', 'count'])

    result: Dict[str, float] = {
        'workday': 0.0,
        'weekend': 0.0
    }

    if False in day_type_spending.index:
        result['workday'] = round(abs(float(day_type_spending.loc[False, 'mean'])), 2)
    if True in day_type_spending.index:
        result['weekend'] = round(abs(float(day_type_spending.loc[True, 'mean'])), 2)

    return result


# Утилита для конвертации транзакций в DataFrame
def transactions_to_dataframe(transactions: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Конвертирует список транзакций в DataFrame.
    """
    return pd.DataFrame(transactions)
