from qa.pages.booking_page import BookingPage
from qa.pages.flight_search_page import FlightSearchPage
from qa.pages.search_results_page import SearchResultsPage
from qa.pages.confirmation_page import ConfirmationPage
from qa.pages.historical_bookings_page import HistoricalBookingsPage


class FlightBookingFlow:

    def __init__(self, page):
        self.search_page = FlightSearchPage(page)
        self.results_page = SearchResultsPage(page)
        self.booking_page = BookingPage(page)
        self.confirmation_page = ConfirmationPage(page)
        self.historical_bookings_page = HistoricalBookingsPage(page)

    def search_flights(
            self, origin, destination, date, num_of_passengers
    ):
        self.search_page.search_flights(
            origin, destination, date, num_of_passengers
        )

    def search_and_select_flight(
            self, origin, destination, date, num_of_passengers, flight_number
    ):
        self.search_page.search_flights(
            origin, destination, date, num_of_passengers
        )

        self.results_page.select_flight(flight_number)
        return self.booking_page

    def complete_booking(
            self, firstname, lastname, email
    ):
        self.booking_page.submit_booking(firstname, lastname, email)

    def book_flight(
            self, origin, destination, date, flight_number, seats,
            firstname, lastname, email
    ):
        self.search_and_select_flight(
            origin, destination, date, seats, flight_number
        )

        self.complete_booking(
            firstname, lastname, email
        )
        return self.confirmation_page

    def view_booking_history(self):
        return self.historical_bookings_page
