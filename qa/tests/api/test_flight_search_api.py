from qa.core.schemas.flight_search_model import FlightSearchResponse
from qa.test_data.flight_data_generator import get_flight_parameters
import pytest
from datetime import date



@pytest.mark.api1
def test_search_flights_returns_matching_flights(reset_database, flight_service):
    # Act
    origin = get_flight_parameters()[0]['origin']
    destination = get_flight_parameters()[0]['destination']
    departure_date = get_flight_parameters()[0]['departure_date']

    response = flight_service.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date
    )

    # Assert
    assert response.status_code == 200

    data = response.json()
    print(data)

    assert "count" in data
    assert "flights" in data
    assert data["count"] == len(data["flights"])

    for flight in data["flights"]:
        assert flight["origin"] == origin
        assert flight["destination"] == destination
        assert flight["departure_date"] == departure_date


@pytest.mark.api_status_codes
@pytest.mark.parametrize('flights', get_flight_parameters())
def test_search_flights_returns_expected_response_code(reset_database, flight_service, flights):
    response = flight_service.search_flights(
        origin=flights['origin'],
        destination=flights['destination'],
        departure_date=flights['departure_date']
    )

    print(f'Expected: {flights["expected_status_code"]} / Actual: {response.status_code}')

    assert response.status_code == flights['expected_status_code']


def test_search_flights_returns_valid_response(reset_database, flight_service):
    response = flight_service.search_flights(
        origin="YYZ",
        destination="YVR",
        departure_date=date.today().strftime("%Y-%m-%d")
    )

    assert response.status_code == 200

    # Validate the complete JSON response
    data = FlightSearchResponse.model_validate(response.json())

    # Check the business requirements
    assert data.count > 0

    for flight in data.flights:
        assert flight.origin == "YYZ"
        assert flight.destination == "YVR"
        assert flight.departure_date.isoformat() == date.today().strftime("%Y-%m-%d")

