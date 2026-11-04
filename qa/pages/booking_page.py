
class BookingPage:

    def __init__(self, page):
        self.page = page
        self.selected_flight = self.page.locator('.selected-flight-summary')
