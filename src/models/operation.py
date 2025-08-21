from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional


@dataclass
class Operation:
    """Модель финансовой операции"""

    date: datetime
    payment_date: datetime
    card_number: str
    status: str
    amount: Decimal
    currency: str
    cashback: Decimal
    category: str
    mcc: Optional[int]
    description: str
    bonuses: Decimal
    rounding: Decimal

    @classmethod
    def from_dict(cls, data: dict) -> "Operation":
        """Создает операцию из словаря данных (из Excel строки)"""
        try:
            return cls(
                date=datetime.strptime(str(data["Дата операции"]).strip(), "%d.%m.%Y %H:%M:%S"),
                payment_date=datetime.strptime(str(data["Дата платежа"]).strip(), "%d.%m.%Y"),
                card_number=str(data.get("Номер карты", "")),
                status=str(data.get("Статус", "OK")),
                amount=abs(Decimal(str(data["Сумма операции"]).replace(",", "."))),
                currency=str(data.get("Валюта операции", "RUB")),
                cashback=Decimal(str(data.get("Кэшбэк", "0")).replace(",", ".")),
                category=str(data.get("Категория", "")),
                mcc=int(data["MCC"]) if data.get("MCC") not in [None, ""] and str(data["MCC"]).isdigit() else None,
                description=str(data.get("Описание", "")),
                bonuses=Decimal(str(data.get("Бонусы (включая кэшбэк)", "0")).replace(",", ".")),
                rounding=Decimal(str(data.get("Округление на инвесткопилку", "0")).replace(",", ".")),
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Ошибка создания операции из данных: {data}. Ошибка: {e}")

    def to_dict(self) -> dict[str, Any]:
        """Преобразует операцию в словарь (для JSON ответа)"""
        return {
            "date": self.date.isoformat(),
            "payment_date": self.payment_date.isoformat(),
            "card_number": self.card_number,
            "status": self.status,
            "amount": float(self.amount),
            "currency": self.currency,
            "cashback": float(self.cashback),
            "category": self.category,
            "mcc": self.mcc,
            "description": self.description,
            "bonuses": float(self.bonuses),
            "rounding": float(self.rounding),
        }
