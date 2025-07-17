from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_generate_excel_report(tmp_path):
    from src.services import generate_excel_report

    test_data = [{"operation_date": "2023-01-01", "amount": -100.0, "category": "Test", "description": "Test"}]

    output_path = tmp_path / "report.xlsx"
    generate_excel_report(test_data, str(output_path))
    assert output_path.exists()


def test_generate_report() -> None:
    with patch("src.main.load_transactions_from_excel") as mock_load:
        mock_load.return_value = [
            {"operation_date": "2023-01-01", "amount": -100.0, "category": "Test", "description": "Test"}
        ]

        response = client.get("/report/")
        assert response.status_code == 200
        assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers["content-type"]
