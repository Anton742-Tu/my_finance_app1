from datetime import datetime
from typing import Any, Dict  # добавим для аннотаций

from fastapi import FastAPI

from src.views.events import events_page, get_date_range  # добавим импорт
from src.views.home import get_home_data

app = FastAPI()


@app.get("/")
async def home(date: str = "2024-01-15 12:00:00") -> Dict[str, Any]:  # добавили возвращаемый тип
    """Главная страница с финансовой аналитикой"""
    target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    data = get_home_data("data/operations.xlsx", target_date)
    return data


@app.get("/events")
async def events(date: str) -> Dict[str, Any]:  # добавили возвращаемый тип
    """Страница событий с фильтрацией по дате"""
    target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Исправляем вызов get_date_range - передаем правильные аргументы
    start_date, end_date = get_date_range(target_date, "M")  # период по умолчанию

    # Вызываем events_page с правильными параметрами
    data = await events_page(date, "M")  # передаем date_str и период
    return data
