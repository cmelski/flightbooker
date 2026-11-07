
class ConfirmationPage:

    def __init__(self, page):
        self.page = page
        self.confirmation_panel = self.page.locator('#confirmation-panel')

    def get_booking_reference(self):
        booking_reference = self.confirmation_panel.locator('p').filter(
            has_text='Booking reference:').text_content().split(':')[1].strip()
        return booking_reference


