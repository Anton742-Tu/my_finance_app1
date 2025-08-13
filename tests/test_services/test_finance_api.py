from unittest.mock import patch
from src.services.finance_api import get_currency_rates


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_response = {"rates": {"USD": 1.0, "EUR": 0.85}}
    mock_get.return_value.json.return_value = mock_response

    result = get_currency_rates()
    assert result["USD"] == 1.0
    assert result["EUR"] == 0.85
