from fastapi import FastAPI
from src.config import Settings
from src.web import home, events
from src.services import cashback, invest

app = FastAPI()
app.include_router(home.router)
app.include_router(events.router)
app.include_router(cashback.router)
app.include_router(invest.router)


@app.get("/")
async def root():
    return {"message": "Finance App API"}
