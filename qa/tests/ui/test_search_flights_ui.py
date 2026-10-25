import re

from qa.models.flight_search_page import FlightSearchPage
from playwright.sync_api import expect


def test_search_flights_ui(page_instance):
    flight_search_page = FlightSearchPage(page_instance)
    departure_date = '2026-11-01'

    with page_instance.expect_response(
        lambda response: (
            '/api/v1/flights/search' in response.url
            and response.status == 200
        )
    ) as response_info:
        flight_search_page.search_flights(
            'YYZ', 'YVR', departure_date, 4
        )

    response = response_info.value
    data = response.json()

    number_of_flights = data['count']

    expect(flight_search_page.search_message).to_be_visible()
    search_message = flight_search_page.search_message.text_content()
    assert search_message.split()[0] == str(number_of_flights)

def test_search_flights_ui_alternative(page_instance):
    flight_search_page = FlightSearchPage(page_instance)
    departure_date = '2026-11-01'

    flight_search_page.search_flights(
            'YYZ', 'YVR', departure_date, 4
        )

    expect(flight_search_page.search_message).to_be_visible()
    # check that the search message element text contains a digit meaning the search has valid results
    expect(flight_search_page.search_message).to_have_text(
        re.compile(r"\d")
    )
    print(flight_search_page.search_message.text_content())
