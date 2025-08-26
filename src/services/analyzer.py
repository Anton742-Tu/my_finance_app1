from decimal import Decimal
from typing import Any, Dict, List

from src.models.operation import Operation


def analyze_spending(operations: List[Operation]) -> Dict[str, Any]:
    """Анализирует расходы по категориям"""
    expenses = [op for op in operations if op.amount > 0]

    by_category: Dict[str, Decimal] = {}
    for op in expenses:
        by_category[op.category] = by_category.get(op.category, Decimal("0")) + op.amount

    total_spent = Decimal("0")
    for op in expenses:
        total_spent += op.amount

    return {
        "total_spent": total_spent,
        "by_category": dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True)),
    }


def get_top_transactions(operations: List[Operation], limit: int = 5) -> List[Operation]:
    """Возвращает топ операций по сумме"""
    return sorted(operations, key=lambda x: x.amount, reverse=True)[:limit]


def calculate_cashback(operations: List[Operation]) -> Decimal:
    """Рассчитывает общий кешбэк"""
    total = Decimal("0")
    for op in operations:
        total += op.cashback
    return total
