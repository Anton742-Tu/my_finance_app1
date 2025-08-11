from datetime import datetime
from typing import List, Dict


async def get_card_stats(start: datetime, end: datetime) -> List[Dict]:
    """Статистика по картам"""
    transactions = await load_transactions(start, end)
    # Реальная реализация будет зависеть от структуры данных
    return [...]


async def get_top_transactions(start: datetime, end: datetime, limit: int = 5) -> List[Dict]:
    transactions = await load_transactions(start, end)
    return sorted(transactions, key=lambda x: abs(x["amount"]), reverse=True)[:limit]


async def get_spending_analysis(start: datetime, end: datetime) -> Dict:
    """Анализ расходов"""
    transactions = await load_transactions(start, end)
    expenses = [t for t in transactions if t["amount"] < 0]
    # Дополнительная логика анализа
    return {...}


async def load_transactions(start: datetime, end: datetime) -> List[Dict]:
    """Загрузка транзакций за период"""
    # Реализация зависит от источника данных
    return [...]


def get_income_analysis():
    return None
