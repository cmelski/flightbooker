
from qa.core.api_client import APIClient


class FlightService:

    def __init__(self, base_url):
        self.api_client = APIClient(base_url)

    def search_flights(self, origin, destination, departure_date):
        params = {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date
        }

        return self.api_client.get(
            "/api/v1/flights/search",
            params=params
        )