from unittest.mock import patch

from src.reports import generate_excel_report
import os

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