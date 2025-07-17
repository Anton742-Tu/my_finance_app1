from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)


def test_generate_report() -> None:
    with patch("src.services.load_transactions_from_excel") as mock_load:
        mock_load.return_value = [
            {"operation_date": "2023-01-01", "amount": -100.0, "category": "Test", "description": "Test"}
        ]

        response = client.get("/report/")
        assert response.status_code == 200
