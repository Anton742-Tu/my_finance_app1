from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime


def get_transactions(
        start_date: datetime,
        end_date: datetime,
        db: Session
) -> List[Dict[str, Any]]:
    """Получает транзакции за период"""
    from src.models.operations import Operation  # Ленивый импорт

    operations = db.query(Operation).filter(
        Operation.date >= start_date,
        Operation.date <= end_date
    ).all()

    return [
        {
            "id": op.id,
            "date": op.date.isoformat(),
            "amount": float(op.amount),
            "category": op.category,
            "description": op.description
        }
        for op in operations
    ]
