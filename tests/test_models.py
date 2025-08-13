import pytest
from src.models.operations import Operation
from decimal import Decimal


@pytest.mark.parametrize(
    "amount,expected",
    [
        (100.50, Decimal("100.50")),
        ("200.75", Decimal("200.75")),
    ],
)
def test_operation_amount(test_db, amount, expected):
    op = Operation(amount=amount)
    test_db.add(op)
    test_db.commit()

    assert op.amount == expected
