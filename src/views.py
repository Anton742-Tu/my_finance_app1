import os

from fastapi import APIRouter, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from src.services import FinanceAnalyzer
from typing import Optional, List, Dict, Union
from datetime import datetime
import pandas as pd
import logging
from io import BytesIO

router = APIRouter(prefix="/api/v1", tags=["transactions"], responses={404: {"description": "Not found"}})

logger = logging.getLogger(__name__)
analyzer = FinanceAnalyzer()


@router.post("/transactions/upload", response_model=Dict[str, Union[int, List[str], Dict[str, float]]])
async def upload_transactions(file: UploadFile) -> JSONResponse:
    """
    Загружает и обрабатывает файл с транзакциями

    Args:
        file: Excel файл с транзакциями (формат .xlsx или .xls)

    Returns:
        JSON с количеством транзакций, списком колонок и базовой статистикой

    Raises:
        HTTPException: 400 - если файл невалидный
        HTTPException: 500 - при внутренних ошибках обработки
    """
    try:
        # Валидация типа файла
        if not file.filename.lower().endswith((".xlsx", ".xls")):
            raise HTTPException(status_code=400, detail="Поддерживаются только Excel файлы (.xlsx, .xls)")

        # Чтение и валидация содержимого
        content = await file.read()
        if not content.startswith(b"PK"):
            raise HTTPException(status_code=400, detail="Неверный формат Excel файла")

        # Обработка транзакций
        with BytesIO(content) as bio:
            bio.seek(0)
            transactions = analyzer.load_transactions(bio)
            df = analyzer.to_dataframe(transactions)

        return JSONResponse(
            {
                "status": "success",
                "transactions_count": len(transactions),
                "columns": list(df.columns),
                "statistics": analyzer.get_stats(transactions),
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transaction upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/transactions/report", response_class=FileResponse)
async def generate_transactions_report(
    start_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
) -> FileResponse:
    """
    Генерирует Excel отчет по транзакциям за указанный период

    Args:
        start_date: Начальная дата в формате YYYY-MM-DD (опционально)
        end_date: Конечная дата в формате YYYY-MM-DD (опционально)

    Returns:
        Excel файл с отчетом

    Raises:
        HTTPException: 400 - при неверном формате дат
        HTTPException: 404 - если нет данных за период
    """
    try:
        # Загрузка и фильтрация транзакций
        transactions = analyzer.load_transactions("data/operations.xlsx")
        df = analyzer.to_dataframe(transactions)

        # Применение фильтров по дате
        if start_date or end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

            if start and end and start > end:
                raise HTTPException(status_code=400, detail="Start date cannot be after end date")

            date_mask = True
            if start:
                date_mask &= df["Дата операции"] >= start
            if end:
                date_mask &= df["Дата операции"] <= end

            df = df[date_mask]

            if df.empty:
                raise HTTPException(status_code=404, detail="No transactions found for the specified period")

        # Генерация отчета
        report_path = "data/output/transactions_report.xlsx"
        generate_excel_report(df, report_path)

        return FileResponse(
            report_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"transactions_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}") from e


@router.get("/transactions/categories/{category}", response_model=Dict[str, Union[str, Dict[str, float], float]])
async def get_category_spending(
    category: str,
    months: int = Query(3, ge=1, le=12, description="Количество месяцев для анализа"),
    end_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
) -> JSONResponse:
    """
    Анализ трат по конкретной категории

    Args:
        category: Название категории
        months: Количество месяцев для анализа (1-12)
        end_date: Конечная дата периода (по умолчанию текущая дата)

    Returns:
        JSON с данными по тратам в категории
    """
    try:
        transactions = analyzer.load_transactions("data/operations.xlsx")
        df = analyzer.to_dataframe(transactions)

        target_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.now()
        result = get_category_spending(df, category, target_date, months)

        return JSONResponse(result)

    except Exception as e:
        logger.error(f"Category analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Category analysis error: {str(e)}") from e


def generate_excel_report(df: pd.DataFrame, output_path: str) -> None:
    """Вспомогательная функция для генерации Excel отчетов"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            # Основной лист с транзакциями
            df.to_excel(writer, sheet_name="Transactions", index=False)

            workbook = writer.book
            worksheet = writer.sheets["Transactions"]

            # Форматирование
            header_format = workbook.add_format({"bold": True, "border": 1, "bg_color": "#D7E4BC", "align": "center"})

            for col_num, value in enumerate(df.columns):
                worksheet.write(0, col_num, value, header_format)

            # Автонастройка ширины колонок
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max(), len(str(col)))
                worksheet.set_column(i, i, min(max_len + 2, 50))

    except Exception as e:
        logger.error(f"Excel report generation error: {str(e)}")
        raise
