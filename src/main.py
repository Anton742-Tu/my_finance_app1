from fastapi import FastAPI
from datetime import datetime
from src.views.home import get_home_data
from src.views.events import get_events_data

app = FastAPI()

@app.get("/")
async def home(date: str = "2024-01-15 12:00:00"):
    target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    data = get_home_data("data/operations.xlsx", target_date)
    return data

@app.get("/events")
async def events(date: str, period: str = "M"):
    target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    data = get_events_data("data/operations.xlsx", target_date, period)
    return data
