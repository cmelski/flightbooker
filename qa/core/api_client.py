import requests

class APIClient:

    def __init__(self, base_url, headers=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(headers or {"Content-Type": "application/json"})

    def get(self, endpoint, **kwargs):
        return self.session.get(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            timeout=10,
            **kwargs
        )


