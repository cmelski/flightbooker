from decimal import Decimal
import re


class SearchResultsPage:

    def __init__(self, page):
        self.page = page
        self.search_message = self.page.locator("#search-message")
        self.results_count = self.page.locator("#results-count")
        self.flight_cards = self.page.locator(".flight-card")

    def select_flight(self, flight_number):
        flight_card = self.flight_cards.filter(
            has=self.page.locator(".flight-details p").filter(
                has_text=flight_number
            )
        )

        flight_card.get_by_role('Button', name='Select flight').click()

    def compare_results_counts(self):
        search_message_count = int(self.search_message.text_content().split()[0])
        search_results_count = int(self.results_count.text_content().split()[0])
        flight_card_count = self.flight_cards.count()
        print(search_message_count, search_results_count, flight_card_count)
        return search_results_count == search_message_count == flight_card_count

    def get_flight_search_results(self):
        search_results = []
        # verify origin, destination, departure date
        flight_card_count = self.flight_cards.count()
        for i in range(flight_card_count):
            flight_details = self.flight_cards.nth(i).locator(".flight-details")
            origin_destination = flight_details.locator("h3").text_content()
            origin = origin_destination.split()[0]
            destination = origin_destination.split()[-1]
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
            print(origin, destination, price_per_passenger, total_price)
            search_results.append({
                'origin': origin,
                'destination': destination,
                'departure_date': dep_date,
                'price_per_passenger': price_per_passenger,
                'total_price': total_price,
                'seats_available': seats_available
            })

        print(search_results)
        return search_results
