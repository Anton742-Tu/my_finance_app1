from decimal import Decimal
from src.models.operations import Operation


def test_operation_amount(db):
    # Тестируем разные форматы сумм
    op1 = Operation(amount=100.50)
    op2 = Operation(amount=Decimal('200.75'))

    db.add_all([op1, op2])
    db.commit()

    assert float(op1.amount) == 100.50
    assert float(op2.amount) == 200.75
