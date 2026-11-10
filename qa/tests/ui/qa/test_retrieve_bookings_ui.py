import pytest
from playwright.sync_api import expect
from qa.core.utilities.common_utilities import format_date, format_flight_time_of_day, format_price, flight_date
from qa.core.utilities.logger import get_logger
from qa.flows.flight_booking_flow import FlightBookingFlow

logger = get_logger(__name__)


@pytest.mark.ui6
def test_retrieve_bookings_ui_no_bookings(reset_database, page_instance):
    flight_booking_flow = FlightBookingFlow(page_instance)

    flight_booking_flow.historical_bookings_page.retrieve_bookings()

    # Assert
    expect(
        flight_booking_flow.historical_bookings_page.bookings_list
    ).to_contain_text("No bookings found")
    logger.info(f'Message: {flight_booking_flow.historical_bookings_page.
                bookings_list.locator("p").text_content()}')


@pytest.mark.smoke
@pytest.mark.ui7
def test_view_past_reservations(reset_database, create_booking_api, page_instance):
    booking_response = create_booking_api.json()['booking']
    print(booking_response)

    with page_instance.expect_response(
            lambda response: (
                    '/api/v1/bookings' in response.url
                    and response.status == 200
            )
    ) as response_info:
        flight_booking_flow = FlightBookingFlow(page_instance)
        flight_booking_flow.historical_bookings_page.retrieve_my_bookings()

    response = response_info.value
    data = response.json()
    print(data)
    expect(flight_booking_flow.historical_bookings_page.bookings_list).to_have_count(data['count'])

    for booking in data['bookings']:
        expect(flight_booking_flow.historical_bookings_page.bookings_list).to_contain_text(booking['firstname'])
        expect(flight_booking_flow.historical_bookings_page.bookings_list).to_contain_text(booking['lastname'])
        expect(flight_booking_flow.historical_bookings_page.bookings_list).to_contain_text(str(booking['flight_id']))
        expect(flight_booking_flow.historical_bookings_page.bookings_list).to_contain_text(str(booking['seats_booked']))
