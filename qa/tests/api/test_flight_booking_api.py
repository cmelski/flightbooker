from qa.core.schemas.flight_search_model import FlightSearchResponse
from qa.test_data.flight_data_generator import get_initial_flight_records_for_db
import pytest
from typing import Any


def get_booking_details() -> list[tuple[dict[str, Any], int]]:
    flight_details = get_initial_flight_records_for_db()[0]
    flight_id_to_book = flight_details[0]
    return [({"flight_id": flight_id_to_book,
              "firstname": "Karen",
              "lastname": "Melski",
              "email": "kmelski@gmail.com",
              "seats_booked": 4}, 201),
            ({"flight_id": 113,
              "firstname": "Karen",
              "lastname": "Melski",
              "email": "kmelski@gmail.com",
              "seats_booked": 4}, 404),
            ({"flight_id": flight_id_to_book,
              "firstname": "Karen",
              "lastname": "Melski",
              "email": "kmelski@gmail.com",
              "seats_booked": 181}, 409)
            ]


@pytest.mark.parametrize('bookings', get_booking_details(), ids=['valid booking', 'incorrect'
                                                                                  'flight_id',
                                                                 'not enough seats avail'])
@pytest.mark.flight_booking_api
def test_flight_booking_api(reset_database, flight_service, bookings):
    booking_payload, expected_status = bookings
    response = flight_service.book_flight(booking_payload)
    print(response.json())
    print(response.status_code)
    assert response.status_code == expected_status
