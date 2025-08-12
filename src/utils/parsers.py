import pandas as pd
from datetime import datetime
from src.models.operations import Operation
from src.utils.database import SessionLocal


def parse_excel_to_db(file_path: str):
    df = pd.read_excel(file_path)
    db = SessionLocal()

    for _, row in df.iterrows():
        operation = Operation(
            operation_date=datetime.strptime(row["Дата операции"], "%d.%m.%Y %H:%M:%S"),
            payment_date=datetime.strptime(row["Дата платежа"], "%d.%m.%Y"),
            card_number=row["Номер карты"],
            status=row["Статус"],
            amount=abs(float(row["Сумма операции"].replace(",", "."))),
            currency=row["Валюта операции"],
            cashback=float(row["Кэшбэк"].replace(",", ".")) if row["Кэшбэк"] else 0,
            category=row["Категория"],
            mcc=int(row["MCC"]) if pd.notna(row["MCC"]) else None,
            description=row["Описание"],
            bonuses=(
                float(row["Бонусы (включая кэшбэк)"].replace(",", "."))
                if pd.notna(row["Бонусы (включая кэшбэк)"])
                else 0
            ),
            rounding=(
                float(row["Округление на инвесткопилку"].replace(",", "."))
                if pd.notna(row["Округление на инвесткопилку"])
                else 0
            ),
        )
        db.add(operation)

    db.commit()
    db.close()

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# В цикле обработки:
logger.info(f"Обработана операция: {row['Описание']}")