
class HistoricalBookingsPage:

    def __init__(self, page):
        self.page = page
        self.bookings_list = self.page.locator('.bookings-list')