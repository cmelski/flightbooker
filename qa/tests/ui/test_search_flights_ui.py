import re
import pytest
from qa.models.flight_search_page import FlightSearchPage
from playwright.sync_api import expect
from qa.core.utilities.common_utilities import format_date
from datetime import date

@pytest.mark.smoke
def test_search_flights_ui(reset_database, page_instance):
    flight_search_page = FlightSearchPage(page_instance)
    departure_date = date.today().strftime("%Y-%m-%d")
    origin = 'YYZ'
    destination = 'YVR'
    num_of_passengers = 4

    with page_instance.expect_response(
        lambda response: (
            '/api/v1/flights/search' in response.url
            and response.status == 200
        )
    ) as response_info:
        flight_search_page.search_flights(
            origin, destination, departure_date, num_of_passengers
        )

    response = response_info.value
    data = response.json()

    number_of_flights = data['count']

    expect(flight_search_page.search_message).to_be_visible()
    search_message = flight_search_page.search_message.text_content()
    assert search_message.split()[0] == str(number_of_flights)
@pytest.mark.smoke
@pytest.mark.ui1
def test_search_flights_ui_alternative(reset_database, page_instance):
    flight_search_page = FlightSearchPage(page_instance)
    origin = 'YYZ'
    destination = 'YVR'
    departure_date = date.today().strftime("%Y-%m-%d")
    num_of_passengers = 4

    flight_search_page.search_flights(
            origin, destination, departure_date, num_of_passengers
        )

    expect(flight_search_page.search_message).to_be_visible()
    # check that the search message element text contains a digit meaning the search has valid results
    expect(flight_search_page.search_message).to_have_text(
        re.compile(r"\d")
    )

    assert flight_search_page.compare_results_counts() is True

    search_results = flight_search_page.get_flight_search_results(origin, destination, num_of_passengers)
    dep_date_formatted = format_date(departure_date)
    for search_result in search_results:
        assert origin in search_result.values()
        assert destination in search_result.values()
        assert dep_date_formatted in search_result.values()
        assert search_result['total_price'] == search_result['price_per_passenger'] * num_of_passengers
        assert search_result['seats_available'] >= num_of_passengers
