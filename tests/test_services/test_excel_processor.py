import pandas as pd
from src.services.excel_processor import load_operations_from_excel


def test_load_operations(tmp_path):
    """Тест загрузки операций из Excel"""
    test_file = tmp_path / "test.xlsx"

    data = {
        'Дата операции': ['01.01.2023 12:00:00'],
        'Дата платежа': ['02.01.2023'],
        'Сумма операции': ['-100,50'],
        'Валюта операции': ['RUB'],
        'Категория': ['Test']
    }

    df = pd.DataFrame(data)
    df.to_excel(test_file, index=False)

    operations = load_operations_from_excel(str(test_file))
    assert len(operations) == 1
    assert operations[0].amount == 100.50
    assert operations[0].category == "Test"
