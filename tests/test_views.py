import pytest
from fastapi.testclient import TestClient

from src.views import app

client = TestClient(app)


@pytest.fixture
def test_transactions():
    return [...]


def test_dashboard_view():
    test_date = "2023-05-20 15:30:00"
    response = client.get(f"/dashboard?date_time={test_date}")
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert "cards" in data
    assert len(data["top_transactions"]) == 5


def test_events_view():
    test_date = "2023-05-20 15:30:00"
    for period in ["W", "M", "Y", "ALL"]:
        response = client.get(f"/events?date_time={test_date}&period={period}")
        assert response.status_code == 200
        data = response.json()
        assert "spending" in data
        assert "income" in data
