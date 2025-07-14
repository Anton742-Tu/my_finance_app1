from fastapi import APIRouter, UploadFile
from src.services import FinanceAnalyzer

router = APIRouter()
analyzer = FinanceAnalyzer()

@router.post("/upload")
async def upload_transactions(file: UploadFile):
    transactions = analyzer.load_transactions(file.file)
    return {"count": len(transactions)}