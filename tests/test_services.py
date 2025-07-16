import pytest
from src.services import FinanceAnalyzer
from src.models import Transaction
from datetime import datetime
import pandas as pd


@pytest.fixture
def sample_transactions():
    return [
        Transaction(
            operation_date=datetime(2023, 1, 1, 16, 44),
            payment_date=datetime(2023, 1, 1),
            card_number="*7197",
            status="OK",
            operation_amount=-160.89,
            operation_currency="RUB",
            payment_amount=-160.89,
            payment_currency="RUB",
            category="Супермаркеты",
            mcc="5411",
            description="Колхоз",
            bonuses=3.00,
            rounding=0.00,
            rounded_amount=160.89
        )
    ]


def test_load_transactions(tmp_path, valid_transaction_data):
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame([valid_transaction_data])
    df.to_excel(file_path, index=False)

    analyzer = FinanceAnalyzer()
    transactions = analyzer.load_transactions(str(file_path))
    assert len(transactions) == 1
    assert transactions[0].category == valid_transaction_data["Категория"]