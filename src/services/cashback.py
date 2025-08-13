from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db

router = APIRouter(prefix="/cashback", tags=["cashback"])


@router.get("/categories")
async def get_cashback_categories(db: Session = Depends(get_db)) -> dict[str, list[str]]:
    return {"categories": ["АЗС", "Рестораны", "Аптеки"]}
