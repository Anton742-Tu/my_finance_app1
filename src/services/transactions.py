from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.operation import Operation
from src.utils.database import get_db
from typing import List, Dict, Any

router = APIRouter()


@router.get("/by-category/{category}")
def get_by_category(
    category: str, db: Session = Depends(get_db)  # Исправлено: убраны лишние аргументы
) -> List[Dict[str, Any]]:
    return [
        {
            "id": op.id,
            "amount": float(op.amount),
            "category": op.category,
            "date": op.date.isoformat() if op.date else None,
        }
        for op in db.query(Operation).filter(Operation.category == category).all()
    ]


@router.get("/last/{limit}")
def get_last_transactions(
    limit: int = 10, db: Session = Depends(get_db)  # Исправлено: убраны лишние аргументы
) -> List[Dict[str, Any]]:
    return [
        {
            "id": op.id,
            "amount": float(op.amount),
            "category": op.category,
            "date": op.date.isoformat() if op.date else None,
            "operation_date": op.date.isoformat() if op.date else None,  # Добавлено поле operation_date
        }
        for op in db.query(Operation)
        .order_by(Operation.date.desc())  # Исправлено: используем date вместо operation_date
        .limit(limit)
        .all()
    ]
