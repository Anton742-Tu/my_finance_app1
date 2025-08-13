import logging
from src.utils.parsers import parse_excel_to_db
from src.utils.database import init_db

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info("Инициализация базы данных...")
        init_db()  # Создаем таблицы

        logger.info("Начало загрузки данных...")
        parse_excel_to_db("data/operations.xlsx")
        logger.info("Данные успешно загружены!")
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        raise
