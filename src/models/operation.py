from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


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
            # Обрабатываем отсутствующие даты платежа
            payment_date_str = data.get("Дата платежа")
            if payment_date_str in [None, "nan", ""]:
                # Если дата платежа отсутствует, используем дату операции
                payment_date = datetime.strptime(str(data["Дата операции"]).strip(), "%d.%m.%Y %H:%M:%S")
            else:
                payment_date = datetime.strptime(str(payment_date_str).strip(), "%d.%m.%Y")

            # Обрабатываем MCC
            mcc_value = data.get("MCC")
            if mcc_value in [None, "nan", ""]:
                mcc = None
            else:
                try:
                    mcc = int(float(mcc_value)) if mcc_value else None
                except (ValueError, TypeError):
                    mcc = None

            return cls(
                date=datetime.strptime(str(data["Дата операции"]).strip(), "%d.%m.%Y %H:%M:%S"),
                payment_date=payment_date,
                card_number=str(data.get("Номер карты", "") or ""),
                status=str(data.get("Статус", "OK") or "OK"),
                amount=abs(Decimal(str(data["Сумма операции"]).replace(",", "."))),
                currency=str(data.get("Валюта операции", "RUB") or "RUB"),
                cashback=Decimal(str(data.get("Кэшбэк", "0") or "0").replace(",", ".")),
                category=str(data.get("Категория", "") or ""),
                mcc=mcc,
                description=str(data.get("Описание", "") or ""),
                bonuses=Decimal(str(data.get("Бонусы (включая кэшбэк)", "0") or "0").replace(",", ".")),
                rounding=Decimal(str(data.get("Округление на инвесткопилку", "0") or "0").replace(",", ".")),
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Ошибка создания операции из данных: {data}. Ошибка: {e}")

    def to_dict(self) -> dict:
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
