from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from src.services import FinanceAnalyzer
from src.models import Transaction
from src.reports import generate_excel_report
import tempfile
import os

app = FastAPI()
analyzer = FinanceAnalyzer()


@app.post("/upload/")
async def upload_transactions(file: UploadFile):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            content = await file.read()
            if not content.startswith(b'PK'):
                raise HTTPException(status_code=400, detail="Invalid file format")
            tmp.write(content)
            tmp_path = tmp.name

        transactions = analyzer.load_transactions(tmp_path)
        stats = analyzer.get_stats(transactions)
        os.unlink(tmp_path)

        return {
            "message": "Файл успешно обработан",
            "stats": stats,
            "count": len(transactions),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/report/")
async def generate_report():
    example_data = [
        Transaction(
            operation_date="31.12.2021 16:44:00",
            payment_date="31.12.2021",
            card_number="*7197",
            status="OK",
            operation_amount=-160.89,
            operation_currency="RUB",
            payment_amount=-160.89,
            payment_currency="RUB",
            category="Супермаркеты",
            mcc="5411",
            description="Колхоз",
            bonuses=3.00,
            rounding=0.00,
            rounded_amount=160.89
        )
    ]

    report_path = "data/output/report.xlsx"
    generate_excel_report(example_data, report_path)
    return FileResponse(
        report_path,
        filename="financial_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )