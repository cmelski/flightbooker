
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
