from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    operation_date: datetime = Field(..., alias="Дата операции")
    payment_date: datetime = Field(..., alias="Дата платежа")
    card_number: Optional[str] = Field(None, alias="Номер карты")
    status: str = Field(..., alias="Статус")
    operation_amount: float = Field(..., alias="Сумма операции")
    operation_currency: str = Field(..., alias="Валюта операции")
    payment_amount: float = Field(..., alias="Сумма платежа")
    payment_currency: str = Field(..., alias="Валюта платежа")
    cashback: Optional[float] = Field(None, alias="Кэшбэк")
    category: str = Field(..., alias="Категория")
    mcc: Optional[str] = Field(None, alias="MCC")
    description: Optional[str] = Field(None, alias="Описание")
    bonuses: float = Field(..., alias="Бонусы (включая кэшбэк)")
    rounding: float = Field(..., alias="Округление на инвесткопилку")
    rounded_amount: float = Field(..., alias="Сумма операции с округлением")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid"
    )

    @field_validator('operation_date', 'payment_date', mode='before')
    def parse_dates(cls, value):
        if isinstance(value, str):
            try:
                # Для формата "31.12.2021 16:44:00"
                if ' ' in value:
                    return datetime.strptime(value, "%d.%m.%Y %H:%M:%S")
                # Для формата "31.12.2021"
                return datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid date format")
        return value

    @field_validator('mcc', mode='before')
    def convert_mcc_to_string(cls, value):
        if value is not None:
            return str(value)
        return None