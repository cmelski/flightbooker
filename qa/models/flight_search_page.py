import re
from decimal import Decimal


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

    def get_flight_search_results(self, origin, destination, num_of_passengers):
        search_results = []
        # verify origin, destination, departure date
        flight_card_count = self.flight_cards.count()
        for i in range(flight_card_count):
            flight_details = self.flight_cards.nth(i).locator(".flight-details")
            origin_destination = flight_details.locator("h3").text_content()
            orig = origin_destination.split()[0]
            dest = origin_destination.split()[-1]
            dep_date = flight_details.locator("p").filter(
                has_text=re.compile(r"[A-Z][a-z]{2} \d{1,2}, \d{4}")
            ).text_content()
            seats_available = int(flight_details.locator('p').filter(
                has_text='seat').text_content().split()[0])
            flight_price = self.flight_cards.nth(i).locator(".flight-price")
            price_per_passenger = Decimal(flight_price.locator("h3").text_content().split('$')[1].
                                          replace(',', ''))
            total_price = Decimal(flight_price.locator('p').filter(has_text='Total').text_content().
                                  split('$')[1].replace(',', ''))
            print(orig, dest, price_per_passenger, total_price)
            search_results.append({
                'origin': orig,
                'destination': dest,
                'departure_date': dep_date,
                'price_per_passenger': price_per_passenger,
                'total_price': total_price,
                'seats_available': seats_available
            })

        print(search_results)
        return search_results
