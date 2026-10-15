
from qa.core.schemas.flight_search_model import FlightSearchResponse


def test_search_flights_returns_matching_flights(reset_database, flight_service):
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





def test_search_flights_returns_valid_response(reset_database, flight_service):
    response = flight_service.search_flights(
        origin="YYZ",
        destination="YVR",
        departure_date="2026-11-01"
    )

    assert response.status_code == 200

    # Validate the complete JSON response
    data = FlightSearchResponse.model_validate(response.json())

    # Check the business requirements
    assert data.count > 0

    for flight in data.flights:
        assert flight.origin == "YYZ"
        assert flight.destination == "YVR"
        assert flight.departure_date.isoformat() == "2026-11-01"