import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.database import Base


@pytest.fixture(scope="session")
def engine():
    """Движок тестовой БД"""
    engine = create_engine("sqlite:///:memory:")

    # Создаем таблицы напрямую
    Base.metadata.create_all(engine)

    yield engine

    # Очистка
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(engine):
    """Сессия БД с автоматическим откатом"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    # Откат и закрытие
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_data(db):
    """Создает тестовые данные"""
    from src.models.operation import Operation
    from datetime import datetime

    operations = [
        Operation(
            date=datetime(2023, 1, 1, 12, 0),
            payment_date=datetime(2023, 1, 2),
            card_number="*1234",
            status="OK",
            amount=100.50,
            currency="RUB",
            category="Food",
            description="Lunch"
        )
    ]

    db.add_all(operations)
    db.commit()
    return operations
