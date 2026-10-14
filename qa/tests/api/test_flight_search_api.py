
from qa.services.flight_service import FlightService


def test_search_flights_returns_matching_flights(flight_service):
    # Act
    response = flight_service.search_flights(
        origin="YYZ",
        destination="YVR",
        departure_date="2026-11-01"
    )

    # Assert
    assert response.status_code == 200

    data = response.json()
    print(data)

    assert "count" in data
    assert "flights" in data
    assert data["count"] == len(data["flights"])

    for flight in data["flights"]:
        assert flight["origin"] == "YYZ"
        assert flight["destination"] == "YVR"
        assert flight["departure_date"] == "2026-11-01"