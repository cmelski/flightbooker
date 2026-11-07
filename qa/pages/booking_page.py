import re


class BookingPage:

    def __init__(self, page):
        self.page = page
        self.selected_flight = self.page.locator('.selected-flight-summary')
        self.first_name = self.page.get_by_label(re.compile("first name", re.IGNORECASE))
        self.last_name = self.page.get_by_label(re.compile("last name", re.IGNORECASE))
        self.email = self.page.get_by_label(re.compile("email address", re.IGNORECASE))
        self.submit_booking_button = self.page.get_by_role('button', name='Confirm booking')

    def submit_booking(self, firstname, lastname, email):
        self.first_name.fill(firstname)
        self.last_name.fill(lastname)
        self.email.fill(email)
        self.submit_booking_button.click()





