from pydantic import BaseModel

class Transaction(BaseModel):
    id: int
    amount: float
    category: str
    date: str  # или datetime