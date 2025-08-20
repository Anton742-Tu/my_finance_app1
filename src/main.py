from datetime import datetime

from fastapi import FastAPI

from src.views.events import get_date_range
from src.views.home import get_home_data

app = FastAPI()


@app.get("/")
async def home(date: str = "2024-01-15 12:00:00"):
    target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    data = get_home_data("data/operations.xlsx", target_date)
    return data


@app.get("/events")
async def events(date: str):
    target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    data = get_date_range("data/operations.xlsx", target_date)
    return data
