from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.operations import Operation

router = APIRouter(prefix="/cashback")


@router.get("/categories")
async def get_cashback_categories(db: Session = Depends(get_db)):
    # Логика получения категорий с кешбэком
    return {"categories": ["АЗС", "Рестораны", "Аптеки"]}
