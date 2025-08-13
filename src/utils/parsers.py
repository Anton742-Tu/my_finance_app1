import logging
from datetime import datetime

import pandas as pd

from src.models.operations import Operation
from src.utils.database import SessionLocal

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def parse_excel_to_db(file_path: str) -> None:
    """Парсинг Excel-файла и загрузка данных в БД"""
    global e
    try:
        logger.info(f"Начало обработки файла: {file_path}")
        df = pd.read_excel(file_path)
        db = SessionLocal()

        for _, row_item in df.iterrows():
            try:
                # Преобразование данных
                operation_data = {
                    "date": datetime.strptime(str(row_item["Дата операции"]), "%d.%m.%Y %H:%M:%S"),
                    "payment_date": datetime.strptime(str(row_item["Дата платежа"]), "%d.%m.%Y"),
                    "card_number": str(row_item["Номер карты"]),
                    "status": str(row_item["Статус"]),
                    "amount": abs(float(str(row_item["Сумма операции"]).replace(",", "."))),
                    "currency": str(row_item["Валюта операции"]),
                    "cashback": (
                        float(str(row_item["Кэшбэк"]).replace(",", ".")) if pd.notna(row_item["Кэшбэк"]) else 0
                    ),
                    "category": str(row_item["Категория"]),
                    "mcc": int(row_item["MCC"]) if pd.notna(row_item["MCC"]) else None,
                    "description": str(row_item["Описание"]),
                    "bonuses": (
                        float(str(row_item["Бонусы (включая кэшбэк)"]).replace(",", "."))
                        if pd.notna(row_item["Бонусы (включая кэшбэк)"])
                        else 0
                    ),
                    "rounding": (
                        float(str(row_item["Округление на инвесткопилку"]).replace(",", "."))
                        if pd.notna(row_item["Округление на инвесткопилку"])
                        else 0
                    ),
                }

                operation = Operation(**operation_data)
                db.add(operation)
                logger.debug(f"Добавлена операция: {operation_data}")

            except Exception as e:
                logger.error(f"Ошибка при обработке строки: {row_item.to_dict()}. Ошибка: {str(e)}")
                continue

            db.commit()
            logger.info(f"Успешно обработано {len(df)} записей")

        logger.error(f"Критическая ошибка при обработке файла: {str(e)}")
        raise
    finally:
        db.close()
        logger.info("Соединение с БД закрыто")
