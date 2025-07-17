import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd

# Импорт сервисов
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from .services import (
    analyze_cashback,
    investment_bank,
    load_transactions_from_excel,
    simple_search,
    find_phone_transactions,
    find_person_transfers,
)
from src.models import Transaction  # Модель данных


# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Конфигурация
DATA_DIR = Path("data")
OPERATIONS_FILE = DATA_DIR / "operations.xlsx"
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
async def startup_event() -> None:
    """Инициализация при запуске"""
    logger.info("Starting Finance Analyzer API")
    if not OPERATIONS_FILE.exists():
        logger.warning("Operations file not found, creating empty template")
        pd.DataFrame(columns=["operation_date", "amount", "category", "description", "cashback"]).to_excel(
            OPERATIONS_FILE, index=False
        )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Инициализация приложения"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not OPERATIONS_FILE.exists():
        pd.DataFrame(columns=["operation_date", "amount", "category", "description", "cashback"]).to_excel(
            OPERATIONS_FILE, index=False
        )
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/report/")
async def generate_report():
    try:
        df = pd.read_excel(OPERATIONS_FILE)
        report_path = DATA_DIR / "financial_report.xlsx"
        df.to_excel(report_path, index=False)
        return FileResponse(
            report_path,
            filename="financial_report.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        raise HTTPException(500, detail=str(e))


@app.post("/upload/", response_model=Dict[str, Any])
async def upload_transactions(file: UploadFile) -> JSONResponse:
    """
    Загрузка файла с транзакциями

    Args:
        file: Excel файл с транзакциями

    Returns:
        Статистика по загруженным данным
    """
    try:
        # Валидация файла
        if not file.filename.endswith((".xlsx", ".xls")):
            raise HTTPException(400, "Only Excel files accepted")

        # Сохранение во временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Загрузка и обработка транзакций
        transactions = load_transactions_from_excel(tmp_path)
        Path(tmp_path).unlink()  # Удаление временного файла

        # Сохранение в основной файл
        pd.DataFrame(transactions).to_excel(OPERATIONS_FILE, index=False)

        # Анализ данных
        cashback_stats = analyze_cashback(transactions, datetime.now().year, datetime.now().month)

        return JSONResponse(
            {
                "status": "success",
                "transactions_loaded": len(transactions),
                "cashback_by_category": cashback_stats,
                "investment_opportunity": investment_bank(
                    f"{datetime.now().year}-{datetime.now().month:02d}", transactions
                ),
            }
        )

    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(500, f"Processing error: {str(e)}")


@app.get("/analysis/cashback/", response_model=Dict[str, float])
async def get_cashback_analysis(
    year: int = Query(..., description="Год для анализа"),
    month: int = Query(..., description="Месяц для анализа (1-12)"),
) -> JSONResponse:
    """
    Анализ выгодных категорий для кешбэка

    Args:
        year: Год анализа
        month: Месяц анализа

    Returns:
        Словарь с категориями и суммами кешбэка
    """
    try:
        transactions = load_transactions_from_excel(OPERATIONS_FILE)
        result = analyze_cashback(transactions, year, month)
        return JSONResponse(result)
    except Exception as e:
        logger.error(f"Cashback analysis failed: {str(e)}")
        raise HTTPException(500, "Analysis error")


@app.get("/analysis/investment/", response_model=Dict[str, float])
async def get_investment_analysis(
    month: str = Query(..., regex=r"^\d{4}-\d{2}$", description="Месяц в формате YYYY-MM"),
    limit: int = Query(50, enum=[10, 50, 100], description="Шаг округления (10, 50, 100)"),
) -> JSONResponse:
    """
    Расчет суммы для инвесткопилки

    Args:
        month: Месяц анализа
        limit: Шаг округления

    Returns:
        Сумма для инвесткопилки
    """
    try:
        transactions = load_transactions_from_excel(OPERATIONS_FILE)
        amount = investment_bank(month, transactions, limit)
        return JSONResponse({"investment_amount": amount})
    except Exception as e:
        logger.error(f"Investment analysis failed: {str(e)}")
        raise HTTPException(500, "Analysis error")


@app.get("/search/", response_model=List[Transaction])
async def search_transactions(
    query: str = Query(..., description="Строка для поиска"),
    search_type: str = Query("simple", enum=["simple", "phone", "person"]),
) -> JSONResponse:
    """
    Поиск транзакций по различным критериям

    Args:
        query: Строка поиска
        search_type: Тип поиска (simple, phone, person)

    Returns:
        Список найденных транзакций
    """
    try:
        transactions = load_transactions_from_excel(OPERATIONS_FILE)

        if search_type == "simple":
            result = simple_search(transactions, query)
        elif search_type == "phone":
            result = find_phone_transactions(transactions)
        else:
            result = find_person_transfers(transactions)

        return JSONResponse(result)
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(500, "Search error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
