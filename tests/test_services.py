from typing import Any, Dict

import pandas as pd

from src.services import FinanceAnalyzer


def test_load_transactions(tmp_path: Any, valid_transaction_data: Dict[str, Any]) -> None:
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame([valid_transaction_data])
    df.to_excel(file_path, index=False)

    analyzer = FinanceAnalyzer()
    transactions = analyzer.load_transactions(str(file_path))
    assert len(transactions) == 1
    assert transactions[0].category == valid_transaction_data["Категория"]
