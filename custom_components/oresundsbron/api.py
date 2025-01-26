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
        self.base_secret = "kfqF*MVT6VUX03#wCUkbVgh"  # Base value for X-Azure-Api-Secret

    def generate_secret(self):
        """Modify the base X-Azure-Api-Secret key dynamically."""
        characters = string.ascii_letters + string.digits
        secret_list = list(self.base_secret)

        # Decide whether to modify the first or last 4 characters
        if random.choice([True, False]):
            # Modify the first 4 characters
            for i in range(4):
                secret_list[i] = random.choice(characters)
        else:
            # Modify the last 4 characters
            for i in range(4):
                secret_list[-(i + 1)] = random.choice(characters)

        # Return the modified secret
        generated_secret = ''.join(secret_list)
        _LOGGER.debug("Generated X-Azure-Api-Secret: %s", generated_secret)
        return generated_secret

    def authenticate(self, credentials):
        """Authenticate with the API and retrieve tokens."""
        url = f"{self.base_url}/api/auth/v1/login"
        self.secret_key = self.generate_secret()  # Generate a new secret for each call
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
                _LOGGER.info("Authentication successful!")
            else:
                # Log the response when authentication fails
                _LOGGER.error(
                    "Authentication failed with status %s: %s",
                    response.status_code,
                    response.text,
                )
                raise Exception(f"Authentication failed: {response.text}")

        except Exception as e:
            # Log the exact error
            _LOGGER.error("Error during authentication: %s", str(e))
            raise

    def make_request(self, endpoint, method="GET", params=None):
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        self.secret_key = self.generate_secret()  # Generate a new secret for each call
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
                _LOGGER.error("Unauthorized request: %s", response.text)
                raise Exception("Unauthorized. Check your credentials or refresh token.")

            response.raise_for_status()
            return response.json()

        except Exception as e:
            # Log the exact error
            _LOGGER.error("Error during API request: %s", str(e))
            raise
