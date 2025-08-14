import pandas as pd
from datetime import datetime
from src.models.operations import Operation
from src.utils.database import SessionLocal


def parse_excel_to_db(file_path: str) -> None:
    """Парсинг Excel с проверкой обязательных колонок"""
    REQUIRED_COLUMNS = {
        'Дата операции', 'Дата платежа', 'Номер карты',
        'Статус', 'Сумма операции', 'Валюта операции'
    }

    db = SessionLocal()
    try:
        df = pd.read_excel(file_path)

        # Проверка обязательных колонок
        missing_cols = REQUIRED_COLUMNS - set(df.columns)
        if missing_cols:
            raise KeyError(f"Отсутствуют обязательные колонки: {missing_cols}")

        db.begin()

        for idx, row in df.iterrows():
            try:
                operation = _create_operation_from_row(row)
                db.add(operation)
            except Exception as e:
                logger.error(f"Ошибка в строке {idx}: {str(e)}")
                continue

        db.commit()
        logger.info(f"Успешно обработано {len(df)} записей")

    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка обработки файла: {str(e)}")
        raise
    finally:
        db.close()
        logger.info("Соединение с БД закрыто")


def _create_operation_from_row(row) -> Operation:
    """Создает операцию из строки с проверкой данных"""
    try:
        return Operation(
            date=datetime.strptime(str(row['Дата операции']), "%d.%m.%Y %H:%M:%S"),
            payment_date=datetime.strptime(str(row['Дата платежа']), "%d.%m.%Y"),
            card_number=str(row['Номер карты']),
            status=str(row['Статус']),
            amount=abs(float(str(row['Сумма операции']).replace(',', '.'))),
            currency=str(row['Валюта операции']),
            cashback=float(str(row.get('Кэшбэк', '0')).replace(',', '.')),
            category=str(row.get('Категория', '')),
            mcc=int(row['MCC']) if 'MCC' in row and pd.notna(row['MCC']) else None,
            description=str(row.get('Описание', '')),
            bonuses=float(str(row.get('Бонусы (включая кэшбэк)', '0')).replace(',', '.')),
            rounding=float(str(row.get('Округление на инвесткопилку', '0')).replace(',', '.'))
        )
    except ValueError as e:
        raise ValueError(f"Ошибка преобразования данных: {str(e)}")
