from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from src.services import FinanceAnalyzer
from src.reports import get_category_spending, get_weekday_spending, get_workday_spending
import pandas as pd
import tempfile
import os
from datetime import datetime
from typing import Optional

app = FastAPI()
analyzer = FinanceAnalyzer()


@app.post("/upload/")
async def upload_transactions(file: UploadFile):
    """Загрузка и обработка файла с транзакциями"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            content = await file.read()
            if not content.startswith(b"PK"):
                raise HTTPException(status_code=400, detail="Invalid file format")
            tmp.write(content)
            tmp_path = tmp.name

        transactions = analyzer.load_transactions(tmp_path)
        df = pd.DataFrame([t.model_dump(by_alias=True) for t in transactions])
        os.unlink(tmp_path)

        return JSONResponse(
            {
                "message": "Файл успешно обработан",
                "count": len(transactions),
                "columns": list(df.columns),  # Для отладки
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/report/")
async def generate_report():
    """Генерация стандартного отчета"""
    transactions = analyzer.load_transactions("data/operations.xlsx")
    report_path = "data/output/report.xlsx"

    # Конвертируем в DataFrame для совместимости с reports.py
    df = pd.DataFrame([t.model_dump(by_alias=True) for t in transactions])
    generate_excel_report(df, report_path)

    return FileResponse(
        report_path,
        filename="financial_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# Новые endpoints для отчетов
@app.get("/reports/category/")
async def category_report(category: str, date: Optional[str] = None):
    """Отчет по тратам в категории"""
    transactions = analyzer.load_transactions("data/operations.xlsx")
    df = pd.DataFrame([t.model_dump(by_alias=True) for t in transactions])

    target_date = datetime.strptime(date, "%Y-%m-%d") if date else None
    result = get_category_spending(df, category, target_date)

    return JSONResponse(result)


@app.get("/reports/weekdays/")
async def weekdays_report(date: Optional[str] = None):
    """Отчет по тратам по дням недели"""
    transactions = analyzer.load_transactions("data/operations.xlsx")
    df = pd.DataFrame([t.model_dump(by_alias=True) for t in transactions])

    target_date = datetime.strptime(date, "%Y-%m-%d") if date else None
    result = get_weekday_spending(df, target_date)

    return JSONResponse(result)


@app.get("/reports/workdays/")
async def workdays_report(date: Optional[str] = None):
    """Сравнение трат в рабочие/выходные дни"""
    transactions = analyzer.load_transactions("data/operations.xlsx")
    df = pd.DataFrame([t.model_dump(by_alias=True) for t in transactions])

    target_date = datetime.strptime(date, "%Y-%m-%d") if date else None
    result = get_workday_spending(df, target_date)

    return JSONResponse(result)


# Добавляем функцию для генерации Excel (из предыдущей версии)
def generate_excel_report(transactions: list, output_path: str):
    """Генерация Excel-отчета (совместимость со старым кодом)"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(transactions)

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Транзакции", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Транзакции"]

        header_format = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "bg_color": "#D7E4BC",
            }
        )
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
