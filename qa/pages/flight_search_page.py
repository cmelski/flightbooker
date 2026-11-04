import re

class FlightSearchPage:

    def __init__(self, page):
        self.page = page
        self.origin_dropdown = self.page.get_by_label(re.compile("from", re.IGNORECASE))
        self.destination_dropdown = self.page.locator('#destination')
        self.departure_date_picker = (self.page.get_by_label
                                      (re.compile("departure", re.IGNORECASE)))
        self.num_of_passengers_dropdown = (self.page.get_by_label
                                           (re.compile("passengers", re.IGNORECASE)))
        self.search_flights_button = self.page.get_by_role("button",
                                                           name=re.compile("search flights", re.IGNORECASE))

    def search_flights(self, origin, destination, departure_date, number_of_passengers):
        self.origin_dropdown.select_option(value=origin)
        self.destination_dropdown.select_option(value=destination)
        self.departure_date_picker.fill(departure_date)
        self.num_of_passengers_dropdown.select_option(value=str(number_of_passengers))
        self.search_flights_button.click()
