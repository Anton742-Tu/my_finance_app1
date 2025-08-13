from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.models.operations import Operation
from src.utils.database import get_db


def get_transactions(start_date: datetime, end_date: datetime, db: Session = next(get_db())) -> List[Dict[str, Any]]:
    operations = (
        db.query(Operation)
        .filter(
            Operation.date >= start_date,  # Исправлено: используем date вместо operation_date
            Operation.date <= end_date,  # Исправлено: используем date вместо operation_date
        )
        .all()
    )

    return [
        {
            "id": op.id,
            "amount": float(op.amount),
            "category": op.category,
            "date": op.date.isoformat() if op.date else None,
            "operation_date": op.date.isoformat() if op.date else None,  # Добавлено для совместимости
        }
        for op in operations
    ]
