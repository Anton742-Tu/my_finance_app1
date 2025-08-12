from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from requests.sessions import Session

from src.services.transactions import get_last_transactions

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    transactions = get_last_transactions(5, db)
    return templates.TemplateResponse("home.html", {"request": request, "transactions": transactions})
