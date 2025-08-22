from datetime import datetime
from typing import Any, Dict, List, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.services.excel_processor import load_operations_from_excel
from src.services.services import (
    Transaction,
    analyze_cashback_categories,
    convert_operations_to_transactions,
    find_person_transfers,
    find_phone_transactions,
    investment_bank,
    simple_search,
)
from src.views.events import events_page
from src.views.home import get_home_data

app = FastAPI(title="My Finance App API", version="1.0.0")

# Глобальные переменные для хранения данных
operations: List[Any] = []
transactions: List[Transaction] = []


# Загружаем операции при старте приложения
@app.on_event("startup")
async def startup_event() -> None:
    """Загрузка операций при запуске приложения"""
    global operations, transactions
    try:
        operations = load_operations_from_excel("data/operations.xlsx")
        transactions = convert_operations_to_transactions(operations)
        print(f"Загружено {len(operations)} операций")
    except FileNotFoundError as e:
        print(f"Ошибка загрузки файла: {e}")
        operations = []
        transactions = []
    except Exception as e:
        print(f"Ошибка загрузки операций: {e}")
        operations = []
        transactions = []


@app.get("/")
async def home(date: str = "2024-01-15 12:00:00") -> Dict[str, Any]:
    """Главная страница с финансовой аналитикой"""
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        data = get_home_data("data/operations.xlsx", target_date)
        return data
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD HH:MM:SS")


@app.get("/events/{date_str}")
async def events(date_str: str, period: Literal["W", "M", "Y", "ALL"] = "M") -> Dict[str, Any]:
    """Страница событий с фильтрацией по дате"""
    try:
        return await events_page(date_str, period)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты")


# Новые эндпоинты для сервисов


@app.get("/api/cashback-analysis/{year}/{month}")
async def cashback_analysis(year: int, month: int) -> Dict[str, float]:
    """
    Анализ выгодных категорий для повышенного кешбэка
    """
    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Месяц должен быть от 1 до 12")

    try:
        result = analyze_cashback_categories(transactions, year, month)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")


@app.get("/api/investment-savings/{month}")
async def investment_savings(month: str, limit: int = 100) -> Dict[str, float]:
    """
    Расчет суммы для инвесткопилки через округление трат
    """
    if limit not in [10, 50, 100]:
        raise HTTPException(status_code=400, detail="Лимит должен быть 10, 50 или 100")

    try:
        # Конвертируем операции в формат для сервиса
        transactions_for_investment = [
            {
                "date": op.date.isoformat(),
                "amount": float(op.amount),
                "category": op.category,
                "description": op.description,
            }
            for op in operations
        ]

        savings = investment_bank(month, transactions_for_investment, limit)
        return {"savings": savings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка расчета: {str(e)}")


@app.get("/api/search")
async def search_transactions(query: str) -> List[Dict[str, Any]]:
    """
    Поиск транзакций по описанию или категории
    """
    try:
        result = simple_search(transactions, query)
        return result  # Теперь возвращает уже готовые dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")


@app.get("/api/phone-transactions")
async def phone_transactions() -> List[Dict[str, Any]]:
    """
    Поиск транзакций с телефонными номерами в описании
    """
    try:
        result = find_phone_transactions(transactions)
        return [dict(transaction) for transaction in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")


@app.get("/api/person-transfers")
async def person_transfers() -> List[Dict[str, Any]]:
    """
    Поиск переводов физическим лицам
    """
    try:
        result = find_person_transfers(transactions)
        return [dict(transaction) for transaction in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Проверка здоровья приложения"""
    return {"status": "healthy", "operations_loaded": str(len(operations))}


# Обработчики ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Any, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request: Any, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
