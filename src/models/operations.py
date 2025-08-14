from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Numeric, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)  # Бывшее operation_date
    payment_date = Column(DateTime)
    card_number = Column(String(20))
    status = Column(String(10))
    amount = Column(Numeric(12, 2))
    currency = Column(String(3))
    cashback = Column(Numeric(5, 2))
    category = Column(String(50))
    mcc = Column(Integer)
    description = Column(String(100))
    bonuses = Column(Numeric(5, 2))
    rounding = Column(Numeric(5, 2))

    # Для аннотации типов
    if False:
        date: Optional[datetime]  # Соответствует Column(DateTime)
