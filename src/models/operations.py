from sqlalchemy import Column, String, DateTime, Numeric, Integer
from src.utils.database import Base


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operation_date = Column(DateTime)  # Дата операции
    payment_date = Column(DateTime)  # Дата платежа
    card_number = Column(String(20))  # Номер карты
    status = Column(String(10))  # Статус
    amount = Column(Numeric(12, 2))  # Сумма операции
    currency = Column(String(3))  # Валюта операции
    cashback = Column(Numeric(5, 2))  # Кэшбэк
    category = Column(String(50))  # Категория
    mcc = Column(Integer)  # MCC код
    description = Column(String(100))  # Описание
    bonuses = Column(Numeric(5, 2))  # Бонусы
    rounding = Column(Numeric(5, 2))  # Округление на инвесткопилку
