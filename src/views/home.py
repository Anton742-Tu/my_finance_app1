from datetime import datetime
from typing import Dict, Any
from urllib.request import Request

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home_page(request: Request) -> Dict[str, Any]:  # Добавлен тип возвращаемого значения
    return {"message": "Welcome"}


def get_greeting(time: datetime) -> str:
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
