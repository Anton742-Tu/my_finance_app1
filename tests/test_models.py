import pytest
from decimal import Decimal
from src.models.operation import Operation


def test_operation_amount(db, test_data):
    op = db.query(Operation).first()
    assert op is not None
    assert float(op.amount) == 100.50