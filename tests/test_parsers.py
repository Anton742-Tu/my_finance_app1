import pytest
from src.utils.parsers import parse_excel_to_db
from src.models.operations import Operation


def test_parse_excel_to_db(test_db, sample_excel):
    parse_excel_to_db(sample_excel, db=test_db)

    operation = test_db.query(Operation).first()
    assert operation is not None
    assert operation.amount == 160.89
    assert operation.category == "Супермаркеты"
    assert operation.description == "Колхоз"
