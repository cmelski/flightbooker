from unittest.mock import patch
from qa.services.flight_service import FlightService
import pytest

@pytest.mark.api_mock
@patch("qa.services.flight_service.APIClient")
def test_search_flights(mock_api_client):

    # Arrange
    mock_get = mock_api_client.return_value.get

    mock_get.return_value = {
        "count": 1,
        "flights": [
            {
                "flight_number": "TS101",
                "origin": "YYZ",
                "destination": "YVR",
                "price": 289.99
            }
        ]
    }

    service = FlightService("http://127.0.0.1:5002")

    # Act
    result = service.search_flights(
        "YYZ", "YVR", "2026-11-01"
    )
    print(result)
    # Assert
    assert result["count"] == 1
    assert result["flights"][0]["flight_number"] == "TS101"

    mock_get.assert_called_once_with(
        "/api/v1/flights/search",
        params={
            "origin": "YYZ",
            "destination": "YVR",
            "departure_date": "2026-11-01"
        }
    )