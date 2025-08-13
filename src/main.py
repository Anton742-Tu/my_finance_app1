from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.views import home, events

app = FastAPI()
app.include_router(home.router)
app.include_router(events.router)


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"message": "Finance App API"})
