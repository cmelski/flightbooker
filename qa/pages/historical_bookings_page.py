
class HistoricalBookingsPage:

    def __init__(self, page):
        self.page = page
        self.bookings_list = self.page.locator('.bookings-list')
        self.refresh_button = self.page.get_by_role('button', name='Refresh')

    def retrieve_bookings(self):
        self.refresh_button.click()