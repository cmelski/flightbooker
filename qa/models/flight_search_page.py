import re




class FlightSearchPage:

    def __init__(self, page):
        self.page = page
        self.origin_dropdown = self.page.get_by_label(re.compile("from", re.IGNORECASE))
        self.destination_dropdown = self.page.locator('#destination')
        self.departure_date_picker = self.page.get_by_label(re.compile("departure", re.IGNORECASE))
        self.num_of_passengers_dropdown = self.page.get_by_label(re.compile("passengers", re.IGNORECASE))
        self.search_flights_button = self.page.get_by_role("button",
                                                           name=re.compile("search flights", re.IGNORECASE))
        self.search_message = self.page.locator("#search-message")
        self.results_count = self.page.locator("#results-count")
        self.flight_cards = self.page.locator(".flight-card")


    def search_flights(self, origin, destination, departure_date, number_of_passengers):
        self.origin_dropdown.select_option(value=origin)
        self.destination_dropdown.select_option(value=destination)
        self.departure_date_picker.fill(departure_date)
        self.num_of_passengers_dropdown.select_option(value=str(number_of_passengers))
        self.search_flights_button.click()

    def compare_results_counts(self):
        search_message_count = int(self.search_message.text_content().split()[0])
        search_results_count = int(self.results_count.text_content().split()[0])
        flight_card_count = self.flight_cards.count()
        print(search_message_count, search_results_count, flight_card_count)
        return search_results_count == search_message_count == flight_card_count

    def validate_flight_details(self, origin, destination, num_of_passengers):

        # verify origin, destination, departure date
        flight_details = self.flight_cards.locator(".flight-details")
        flight_details_count = self.flight_cards.count()

        for i in range(flight_details_count):
            origin_destination = flight_details.nth(i).locator("h3").text_content()
            orig = origin_destination.split()[0]
            dest = origin_destination.split()[-1]
            print(orig, dest)
            if origin == orig and destination == dest:
                continue
            else:
                return False

        return True

