from unittest.mock import patch

import pytest
from src.reports import generate_excel_report
from src.services import Transaction
import pandas as pd
import os

from tests.test_views import client


@pytest.fixture
def sample_transactions():
    return [
        Transaction(id=1, date="2023-01-01", amount=100.0, category="Food"),
        Transaction(id=2, date="2023-01-02", amount=200.0, category="Transport"),
    ]


def test_generate_excel_report(tmp_path, sample_transaction):
    output_path = tmp_path / "report.xlsx"
    generate_excel_report([sample_transaction], str(output_path))
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

def test_generate_report(tmp_path, sample_transaction):
    output_path = tmp_path / "report.xlsx"
    with patch("src.main.analyzer.load_transactions") as mock_load:
        mock_load.return_value = [sample_transaction]
        generate_excel_report([sample_transaction], str(output_path))
    assert os.path.exists(output_path)