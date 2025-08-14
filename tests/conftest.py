import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.database import Base
from src.models.operations import Operation
from datetime import datetime


@pytest.fixture(scope="session")
def engine():
    """Движок SQLite в памяти для тестов"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(engine):
    """Сессия БД с автоматическим откатом"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_operations(db):
    """Тестовые данные операций"""
    operations = [
        Operation(
            date=datetime(2023, 1, 1),
            amount=100.0,
            category="Food",
            description="Lunch"
        ),
        Operation(
            date=datetime(2023, 1, 2),
            amount=200.0,
            category="Transport",
            description="Taxi"
        )
    ]
    db.add_all(operations)
    db.commit()
    return operations
