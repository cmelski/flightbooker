
from qa.test_data.flight_data_generator import get_initial_flight_records_for_db, get_flight_parameters
import pytest
from typing import Any
from qa.core.utilities.logger import get_logger
logger = get_logger(__name__)


def get_booking_details() -> list[tuple[dict[str, Any], int]]:
    flight_details = get_initial_flight_records_for_db()[0]
    flight_id_to_book = flight_details[0]
    seats = 4
    ticket_price = flight_details[6]
    return [({"flight_id": flight_id_to_book,
              "firstname": "Karen",
              "lastname": "Melski",
              "email": "kmelski@gmail.com",
              "seats_booked": seats,
              "total_price": seats * ticket_price}, 201),
            ({"flight_id": 113,
              "firstname": "Karen",
              "lastname": "Melski",
              "email": "kmelski@gmail.com",
              "seats_booked": 4,
              "total_price": seats * ticket_price}, 404),
            ({"flight_id": flight_id_to_book,
              "firstname": "Karen",
              "lastname": "Melski",
              "email": "kmelski@gmail.com",
              "seats_booked": 181,
              "total_price": seats * ticket_price}, 409)
            ]


@pytest.mark.parametrize('bookings', get_booking_details(), ids=['valid booking', 'incorrect'
                                                                                  'flight_id',
                                                                 'not enough seats avail'])
@pytest.mark.flight_booking_api
def test_flight_booking_status_codes_api(reset_database, flight_service, bookings):
    booking_payload, expected_status = bookings
    response = flight_service.book_flight(booking_payload)
    print(response.json())
    print(response.status_code)
    assert response.status_code == expected_status


@pytest.mark.api_business_rules
def test_flight_booking_api_business_rules(reset_database, flight_service):
    flight_to_book = get_initial_flight_records_for_db()[0]
    # get available seats for flight before booking
    avail_seats = flight_to_book[7]
    # get ticket price
    ticket_price = flight_to_book[6]
    # get booking details from function
    booking_details = get_booking_details()[0][0]
    flight_id = booking_details['flight_id']
    seats_booked = booking_details['seats_booked']
    # book flight
    response_flight_booking = flight_service.book_flight(booking_details)
    #search for flights
    origin = get_flight_parameters()[0]['origin']
    destination = get_flight_parameters()[0]['destination']
    departure_date = get_flight_parameters()[0]['departure_date']

    response_flight_search = flight_service.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date
    )

    print(response_flight_search.json()['flights'])

    # assert seats reduced in flights table
    for flight in response_flight_search.json()['flights']:
        if flight['flight_id'] == flight_id:
            assert flight['seats_available'] == avail_seats - seats_booked
            logger.info(f'Seats before booking: {avail_seats}\n'
                        f'Seats booked: {seats_booked}\n'
                        f'Seats after booking: {flight["seats_available"]}')
    # assert total price in bookings table
    total_price = response_flight_booking.json()['booking']['total_price']
    assert total_price == ticket_price * seats_booked
    logger.info(f'Ticket price: {ticket_price}\n'
                f'Seats booked: {seats_booked}\n'
                f'Total price in bookings table: {total_price}')


