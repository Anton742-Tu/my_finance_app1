from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.operations import Operation
from src.utils.database import get_db

router = APIRouter(prefix="/transactions")


@router.get("/by-category/{category}")
def get_by_category(category: str, db: Session = Depends(get_db)):
    return db.query(Operation).filter(Operation.category == category).all()


@router.get("/last/{limit}")
def get_last_transactions(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Operation).order_by(Operation.operation_date.desc()).limit(limit).all()
