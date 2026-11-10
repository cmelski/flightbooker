import re
import pytest
from decimal import Decimal
import json
from qa.flows.flight_booking_flow import FlightBookingFlow
from playwright.sync_api import expect
from qa.core.utilities.common_utilities import format_date, format_flight_time_of_day, format_price, flight_date
from qa.core.utilities.logger import get_logger

logger = get_logger(__name__)


# @pytest.mark.smoke
# def test_search_flights_ui_alternative(reset_database, page_instance):
#     flight_search_page = FlightSearchPage(page_instance)
#     departure_date = date.today().strftime("%Y-%m-%d")
#     origin = 'YYZ'
#     destination = 'YVR'
#     num_of_passengers = 4
#
#     with page_instance.expect_response(
#         lambda response: (
#             '/api/v1/flights/search' in response.url
#             and response.status == 200
#         )
#     ) as response_info:
#         flight_search_page.search_flights(
#             origin, destination, departure_date, num_of_passengers
#         )
#
#     response = response_info.value
#     data = response.json()
#
#     number_of_flights = data['count']
#
#     expect(flight_search_page.search_message).to_be_visible()
#     search_message = flight_search_page.search_message.text_content()
#     assert search_message.split()[0] == str(number_of_flights)

@pytest.mark.smoke
@pytest.mark.ui1
def test_search_flights_ui(reset_database, flight_details_for_search, page_instance):
    origin = flight_details_for_search['origin']
    destination = flight_details_for_search['destination']
    departure_date = flight_details_for_search['departure_date']
    num_of_passengers = flight_details_for_search['num_of_passengers']
    logger.info(f'Starting flight search with search parameters: {origin}, {destination}, '
                f'{departure_date}, {num_of_passengers}')
    flight_booking_flow = FlightBookingFlow(page_instance)
    flight_booking_flow.search_flights(
        origin, destination, departure_date, num_of_passengers,
    )

    expect(flight_booking_flow.results_page.search_message).to_be_visible()
    # check that the search message element text contains a digit meaning the search has valid results
    expect(flight_booking_flow.results_page.search_message).to_have_text(
        re.compile(r"\d")
    )
    assert flight_booking_flow.results_page.compare_results_counts() is True
    search_results = flight_booking_flow.results_page.get_flight_search_results()
    dep_date_formatted = format_date(departure_date)
    for search_result in search_results:
        assert origin in search_result.values()
        assert destination in search_result.values()
        assert dep_date_formatted in search_result.values()
        assert search_result['total_price'] == search_result['price_per_passenger'] * num_of_passengers
        assert search_result['seats_available'] >= num_of_passengers


@pytest.mark.smoke
@pytest.mark.ui2
def test_search_and_select_flight_ui(reset_database, flight_details_for_search, page_instance):
    origin = flight_details_for_search['origin']
    destination = flight_details_for_search['destination']
    departure_date = flight_details_for_search['departure_date']
    num_of_passengers = flight_details_for_search['num_of_passengers']
    flight_number = flight_details_for_search['flight_number']
    departure_time = flight_details_for_search['departure_time']
    price = flight_details_for_search['price']
    total_price = format_price((Decimal(str(price)) * num_of_passengers))
    dep_date_formatted = format_date(departure_date)
    departure_time_formatted = format_flight_time_of_day(departure_time)

    flight_booking_flow = FlightBookingFlow(page_instance)
    booking_page = flight_booking_flow.search_and_select_flight(
        origin, destination, departure_date, num_of_passengers, flight_number,
    )

    expect(booking_page.selected_flight).to_contain_text(flight_number)
    expect(booking_page.selected_flight).to_contain_text(f'{origin} → {destination}')
    expect(booking_page.selected_flight).to_contain_text(dep_date_formatted)
    expect(booking_page.selected_flight).to_contain_text(departure_time_formatted)
    expect(booking_page.selected_flight).to_contain_text(total_price)
    expect(booking_page.selected_flight).to_contain_text(f'Passengers: {num_of_passengers}')


@pytest.mark.smoke
@pytest.mark.ui3
def test_book_flight_ui(reset_database, flight_details_for_search, page_instance):
    origin = flight_details_for_search['origin']
    destination = flight_details_for_search['destination']
    departure_date = flight_details_for_search['departure_date']
    num_of_passengers = flight_details_for_search['num_of_passengers']
    flight_number = flight_details_for_search['flight_number']
    price = flight_details_for_search['price']
    total_price = format_price((Decimal(str(price)) * num_of_passengers))
    first_name = 'Chris'
    last_name = 'Melski'
    email = 'cmelski@gmail.com'
    flight_booking_flow = FlightBookingFlow(page_instance)
    confirmation_page = flight_booking_flow.book_flight(origin, destination, departure_date, flight_number,
                                                        num_of_passengers, first_name, last_name, email)
    expect(confirmation_page.confirmation_panel).to_contain_text('trip is confirmed')
    expect(confirmation_page.confirmation_panel).to_contain_text(f'{origin} → {destination}')
    expect(confirmation_page.confirmation_panel).to_contain_text(flight_number)
    expect(confirmation_page.confirmation_panel).to_contain_text(total_price)
    expect(confirmation_page.confirmation_panel).to_contain_text(f'Passengers: {num_of_passengers}')

    booking_reference = confirmation_page.get_booking_reference()
    logger.info(f'Booking reference: {booking_reference}')
    historical_bookings = flight_booking_flow.view_booking_history()
    expect(historical_bookings.bookings_list).to_have_count(1)
    expect(historical_bookings.bookings_list).to_contain_text(f'Booking #{booking_reference}')
@pytest.mark.ui4
def test_flight_search_not_enough_seats(reset_database, page_instance):

    # Arrange: Mock flight search API response
    def mock_flight_search(route):

        mock_response = {
            "flights": [
                {
                    "flight_id": 101,
                    "flight_number": "TS101",
                    "origin": "YYZ",
                    "destination": "YVR",
                    "departure_date": flight_date(0),
                    "departure_time": "08:30:00",
                    "price": 289.99,
                    "total_seats": 2,
                    "status": "SCHEDULED"
                }
            ]
        }

        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_response)
        )

    page_instance.route(
        "**/api/v1/flights/search**",
        mock_flight_search
    )

    # Act: Search for 4 passengers
    flight_booking_flow = FlightBookingFlow(page_instance)

    flight_booking_flow.search_flights(
        "YYZ",
        "YVR",
        flight_date(0),
        4
    )

    # Assert
    expect(
        page_instance.locator("#search-message")
    ).to_contain_text("not enough seats")
    logger.info(f'Error message: {page_instance.locator("#search-message").text_content()}')

@pytest.mark.ui5
def test_flight_search_no_matching_flights(reset_database, page_instance):

    # Arrange: Mock flight search API response
    def mock_flight_search(route):

        mock_response = {
            "flights": []
        }

        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_response)
        )

    page_instance.route(
        "**/api/v1/flights/search**",
        mock_flight_search
    )

    # Act: Search for 4 passengers
    flight_booking_flow = FlightBookingFlow(page_instance)

    flight_booking_flow.search_flights(
        "YYZ",
        "YVR",
        flight_date(0),
        4
    )

    # Assert
    expect(
        page_instance.locator("#search-message")
    ).to_contain_text("No flights found for your search")
    logger.info(f'Error message: {page_instance.locator("#search-message").text_content()}')

