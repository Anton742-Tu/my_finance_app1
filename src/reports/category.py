from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.models.operation import Operation  # Исправлен импорт

router = APIRouter(prefix="/reports")


@router.get("/spending-by-category")
def spending_by_category(db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = db.query(Operation.category, func.sum(Operation.amount).label("total")).group_by(Operation.category).all()

    return {item[0]: float(item[1]) for item in result}
