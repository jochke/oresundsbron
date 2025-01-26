# api.py
import random
import string
import requests
import logging

_LOGGER = logging.getLogger(__name__)

class OresundsbronAPI:
    """Handle communication with the Øresundsbron API."""

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

        try:
            response = requests.post(url, json=credentials, headers=headers)
            
            # Debug logs for request details
            _LOGGER.debug("Authentication request URL: %s", url)
            _LOGGER.debug("Authentication request headers: %s", headers)
            _LOGGER.debug("Authentication request body: %s", credentials)
            
            # Debug logs for response details
            _LOGGER.debug("Authentication response status: %s", response.status_code)
            _LOGGER.debug("Authentication response body: %s", response.text)

            if response.status_code == 200:
                data = response.json()
                self.token = data["token"]
                self.refresh_token = data["refreshToken"]
            else:
                raise Exception(f"Authentication failed with status {response.status_code}: {response.text}")

        except Exception as e:
            _LOGGER.error("Error during authentication: %s", e)
            raise

    def make_request(self, endpoint, method="GET", params=None):
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Azure-Api-Secret": self.secret_key
        }

        try:
            response = requests.request(method, url, headers=headers, params=params)
            
            # Debug logs for request details
            _LOGGER.debug("Request URL: %s", url)
            _LOGGER.debug("Request headers: %s", headers)
            _LOGGER.debug("Request method: %s", method)
            _LOGGER.debug("Request params: %s", params)
            
            # Debug logs for response details
            _LOGGER.debug("Response status: %s", response.status_code)
            _LOGGER.debug("Response body: %s", response.text)

            if response.status_code == 401:
                raise Exception("Unauthorized. Check your credentials or refresh token.")

            response.raise_for_status()
            return response.json()

        except Exception as e:
            _LOGGER.error("Error during API request: %s", e)
            raise
