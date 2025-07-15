from unittest.mock import patch

import pandas as pd
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_upload_file(tmp_path, valid_transaction_data):
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame([valid_transaction_data])
    df.to_excel(file_path, index=False)

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload/",
            files={"file": ("test.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1


def test_generate_report(sample_transaction):
    with patch("src.main.analyzer.load_transactions") as mock_load:
        mock_load.return_value = [sample_transaction]
        response = client.get("/report/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
