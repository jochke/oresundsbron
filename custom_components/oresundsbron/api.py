# api.py
import random
import string
import requests

class OresundsbronAPI:
    """Handle communication with the Öresundsbron API."""

    def __init__(self):
        self.base_url = "https://www.oresund.io"
        self.token = None
        self.refresh_token = None
        self.secret_key = self.generate_secret()

    def generate_secret(self):
        """Generate a dynamic X-Azure-Api-Secret key."""
        characters = string.ascii_letters + string.digits + "!@#$%&*"
        return ''.join(random.choice(characters) for _ in range(20))

    def authenticate(self, credentials):
        """Authenticate with the API and retrieve tokens."""
        url = f"{self.base_url}/api/auth/v1/login"
        headers = {"X-Azure-Api-Secret": self.secret_key}

        response = requests.post(url, json=credentials, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.token = data["token"]
            self.refresh_token = data["refreshToken"]
        else:
            raise Exception("Authentication failed")

    def make_request(self, endpoint, method="GET", params=None):
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Azure-Api-Secret": self.secret_key
        }

        response = requests.request(method, url, headers=headers, params=params)
        if response.status_code == 401:
            raise Exception("Unauthorized. Check your credentials or refresh token.")

        response.raise_for_status()
        return response.json()
