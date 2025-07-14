from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_generate_report(sample_transaction):
    with patch("src.main.analyzer.load_transactions") as mock_load:
        mock_load.return_value = [sample_transaction]
        response = client.get("/report/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
