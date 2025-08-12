from fastapi import FastAPI

from src.services import cashback, invest
from src.views import home, events

app = FastAPI()
app.include_router(home.router)
app.include_router(events.router)
app.include_router(cashback.router)
app.include_router(invest.router)


@app.get("/")
async def root():
    return {"message": "Finance App API"}


app = FastAPI()
app.include_router(home.router)
app.include_router(events.router)