import json
import logging
import re
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from functools import reduce
from typing import Any, Dict, List, TypedDict

logger = logging.getLogger(__name__)


# Типы для TypeScript-like разработки
class Transaction(TypedDict):
    """Типизированная транзакция"""

    date: str
    amount: float
    category: str
    description: str
    cashback: float


# 1. Сервис выгодных категорий повышенного кешбэка
def analyze_cashback_categories(transactions: List[Transaction], year: int, month: int) -> Dict[str, float]:
    """
    Анализирует выгодность категорий для повышенного кешбэка.

    Args:
        transactions: Список транзакций
        year: Год для анализа
        month: Месяц для анализа (1-12)

    Returns:
        Словарь с категориями и суммами кешбэка
    """
    logger.info(f"Анализ кешбэка за {month}/{year}")

    def filter_by_date(txn: Transaction) -> bool:
        """Фильтрует транзакции по дате"""
        try:
            txn_date = datetime.strptime(txn["date"], "%Y-%m-%d")
            return txn_date.year == year and txn_date.month == month
        except ValueError:
            return False

    def calculate_category_cashback(acc: Dict[str, float], txn: Transaction) -> Dict[str, float]:
        """Аккумулирует кешбэк по категориям"""
        if txn["cashback"] > 0:
            acc[txn["category"]] = acc.get(txn["category"], 0.0) + txn["cashback"]
        return acc

    # Функциональный pipeline
    result = reduce(calculate_category_cashback, filter(filter_by_date, transactions), {})

    logger.debug(f"Результат анализа кешбэка: {result}")
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


# 2. Сервис инвесткопилки
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для инвесткопилки через округление трат.

    Args:
        month: Месяц в формате 'YYYY-MM'
        transactions: Список транзакций
        limit: Предел округления (10, 50, 100)

    Returns:
        Сумма для инвесткопилки
    """
    logger.info(f"Расчет инвесткопилки за {month} с лимитом {limit}")

    def filter_by_month(txn: Dict[str, Any]) -> bool:
        """Фильтрует транзакции по месяцу"""
        try:
            return txn["date"].startswith(month)
        except (KeyError, AttributeError):
            return False

    def calculate_rounding(txn: Dict[str, Any]) -> float:
        """Рассчитывает округление для одной транзакции"""
        try:
            amount = abs(txn["amount"])  # Берем абсолютное значение для расходов
            rounded = ((amount + limit - 1) // limit) * limit
            return rounded - amount
        except (KeyError, TypeError):
            return 0.0

    # Функциональный подход
    monthly_transactions = filter(filter_by_month, transactions)
    roundings = map(calculate_rounding, monthly_transactions)
    total_savings = sum(roundings)

    logger.debug(f"Сумма инвесткопилки: {total_savings:.2f}")
    return round(total_savings, 2)


# 3. Простой поиск
def simple_search(transactions: List[Transaction], search_query: str) -> List[Transaction]:
    """
    Поиск транзакций по описанию или категории.

    Args:
        transactions: Список транзакций
        search_query: Строка для поиска

    Returns:
        Отфильтрованные транзакции
    """
    logger.info(f"Поиск по запросу: '{search_query}'")

    def matches_query(txn: Transaction) -> bool:
        """Проверяет совпадение с запросом"""
        query_lower = search_query.lower()
        return query_lower in txn.get("description", "").lower() or query_lower in txn.get("category", "").lower()

    result = list(filter(matches_query, transactions))
    logger.debug(f"Найдено транзакций: {len(result)}")
    return result


# 4. Поиск по телефонным номерам
def find_phone_transactions(transactions: List[Transaction]) -> List[Transaction]:
    """
    Находит транзакции с телефонными номерами в описании.

    Args:
        transactions: Список транзакций

    Returns:
        Транзакции с телефонными номерами
    """
    logger.info("Поиск транзакций с телефонными номерами")

    # Регулярное выражение для российских номеров
    phone_pattern = re.compile(r"(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}")

    def has_phone_number(txn: Transaction) -> bool:
        """Проверяет наличие телефонного номера"""
        description = txn.get("description", "")
        return bool(phone_pattern.search(description))

    result = list(filter(has_phone_number, transactions))
    logger.debug(f"Найдено транзакций с телефонами: {len(result)}")
    return result


# 5. Поиск переводов физическим лицам
def find_person_transfers(transactions: List[Transaction]) -> List[Transaction]:
    """
    Находит переводы физическим лицам.

    Args:
        transactions: Список транзакций

    Returns:
        Транзакции-переводы физлицам
    """
    logger.info("Поиск переводов физическим лицам")

    # Паттерн для имени и фамилии с точкой
    name_pattern = re.compile(r"[А-Я][а-я]+\s[А-Я]\.")

    def is_person_transfer(txn: Transaction) -> bool:
        """Проверяет, является ли транзакция переводом физлицу"""
        category = txn.get("category", "")
        description = txn.get("description", "")

        return category == "Переводы" and bool(name_pattern.search(description))

    result = list(filter(is_person_transfer, transactions))
    logger.debug(f"Найдено переводов физлицам: {len(result)}")
    return result


# Утилиты для конвертации
def convert_operations_to_transactions(operations: List[Any]) -> List[Transaction]:
    """Конвертирует операции в транзакции для сервисов"""
    return [
        {
            "date": op.date.isoformat(),
            "amount": float(op.amount),
            "category": op.category,
            "description": op.description,
            "cashback": float(op.cashback),
        }
        for op in operations
    ]
