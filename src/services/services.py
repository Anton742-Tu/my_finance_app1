import logging
import re
from datetime import datetime
from functools import reduce
from typing import Any, Dict, List, TypedDict

logger = logging.getLogger(__name__)


class Transaction(TypedDict):
    """Типизированная транзакция"""

    date: str
    amount: float
    category: str
    description: str
    cashback: float


def analyze_cashback_categories(transactions: List[Transaction], year: int, month: int) -> Dict[str, float]:
    """
    Анализирует выгодность категорий для повышенного кешбэка.
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

    result: Dict[str, float] = reduce(calculate_category_cashback, filter(filter_by_date, transactions), {})

    logger.debug(f"Результат анализа кешбэка: {result}")
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для инвесткопилки через округление трат.
    """
    logger.info(f"Расчет инвесткопилки за {month} с лимитом {limit}")

    def filter_by_month(txn: Dict[str, Any]) -> bool:
        """Фильтрует транзакции по месяцу"""
        try:
            txn_date = txn.get("date", "")
            if isinstance(txn_date, str):
                return txn_date.startswith(month)
            return False
        except (KeyError, AttributeError):
            return False

    def calculate_rounding(txn: Dict[str, Any]) -> float:
        """Рассчитывает округление для одной транзакции"""
        try:
            amount = abs(float(txn.get("amount", 0)))
            rounded = ((amount + limit - 1) // limit) * limit
            return float(rounded - amount)
        except (KeyError, TypeError, ValueError):
            return 0.0

    monthly_transactions = filter(filter_by_month, transactions)
    roundings = map(calculate_rounding, monthly_transactions)
    total_savings = sum(roundings)

    logger.debug(f"Сумма инвесткопилки: {total_savings:.2f}")
    return round(total_savings, 2)


def simple_search(transactions: List[Transaction], search_query: str) -> List[Dict[str, Any]]:
    """
    Поиск транзакций по описанию или категории.
    """
    logger.info(f"Поиск по запросу: '{search_query}'")

    def matches_query(txn: Transaction) -> bool:
        """Проверяет совпадение с запросом"""
        query_lower = search_query.lower()
        description = txn.get("description", "")
        category = txn.get("category", "")

        return query_lower in description.lower() or query_lower in category.lower()

    result = list(filter(matches_query, transactions))
    logger.debug(f"Найдено транзакций: {len(result)}")
    return [dict(txn) for txn in result]


def find_phone_transactions(transactions: List[Transaction]) -> List[Dict[str, Any]]:
    """
    Находит транзакции с телефонными номерами в описании.
    """
    logger.info("Поиск транзакций с телефонными номерами")

    phone_pattern = re.compile(r"(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}")

    def has_phone_number(txn: Transaction) -> bool:
        """Проверяет наличие телефонного номера"""
        description = txn.get("description", "")
        return bool(phone_pattern.search(description))

    result = list(filter(has_phone_number, transactions))
    logger.debug(f"Найдено транзакций с телефонами: {len(result)}")
    return [dict(txn) for txn in result]


def find_person_transfers(transactions: List[Transaction]) -> List[Dict[str, Any]]:
    """
    Находит переводы физическим лицам.
    """
    logger.info("Поиск переводов физическим лицам")

    name_pattern = re.compile(r"[А-Я][а-я]+\s[А-Я]\.")

    def is_person_transfer(txn: Transaction) -> bool:
        """Проверяет, является ли транзакция переводом физлицу"""
        category = txn.get("category", "")
        description = txn.get("description", "")

        return category == "Переводы" and bool(name_pattern.search(description))

    result = list(filter(is_person_transfer, transactions))
    logger.debug(f"Найдено переводов физлицам: {len(result)}")
    return [dict(txn) for txn in result]


def convert_operations_to_transactions(operations: List[Any]) -> List[Transaction]:
    """Конвертирует операции в транзакции для сервисов"""
    transactions_list: List[Transaction] = []

    for op in operations:
        transaction: Transaction = {
            "date": op.date.isoformat(),
            "amount": float(op.amount),
            "category": op.category,
            "description": op.description,
            "cashback": float(op.cashback),
        }
        transactions_list.append(transaction)

    return transactions_list
