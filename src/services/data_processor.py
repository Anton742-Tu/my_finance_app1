from datetime import datetime
from sqlalchemy.orm import Session
from src.models.operations import Operation
from src.utils.database import get_db

def get_transactions(
    start_date: datetime,
    end_date: datetime,
    db: Session = next(get_db())
) -> list[dict]:
    return db.query(Operation).filter(
        Operation.operation_date >= start_date,
        Operation.operation_date <= end_date
    ).all()