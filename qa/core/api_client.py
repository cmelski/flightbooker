
import requests


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def get(self, endpoint, params=None):
        url = self.base_url + endpoint
        return requests.get(url, params=params, timeout=10)