# api.py
import requests
import logging

_LOGGER = logging.getLogger(__name__)

class OresundsbronAPI:
    """Handle communication with the Øresundsbron API."""

    def __init__(self):
        self.base_url = "https://www.oresund.io"
        self.token = None
        self.refresh_token = None
        self.secret_key = "fqF*MVT6VUX03#wCUkbV"

    def log_request_response(self, url, method, headers, body, response):
        """Log request and response details for debugging."""
        _LOGGER.error("REQUEST URL: %s", url)
        _LOGGER.error("REQUEST METHOD: %s", method)
        _LOGGER.error("REQUEST HEADERS: %s", headers)
        _LOGGER.error("REQUEST BODY: %s", body)
        _LOGGER.error("RESPONSE STATUS CODE: %s", response.status_code)
        _LOGGER.error("RESPONSE BODY: %s", response.text)

    def authenticate(self, credentials):
        """Authenticate with the API and retrieve tokens."""
        url = f"{self.base_url}/api/auth/v1/login"
        headers = {"X-Azure-Api-Secret": self.secret_key}

        # Add the rcToken to the request body
        body = {
            **credentials,
            "rcToken": "app"
        }

        try:
            response = requests.post(url, json=body, headers=headers)

            # Log both request and response
            self.log_request_response(url, "POST", headers, body, response)

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
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Azure-Api-Secret": self.secret_key
        }

        try:
            response = requests.request(method, url, headers=headers, params=params)

            # Log both request and response
            self.log_request_response(url, method, headers, params, response)

            if response.status_code == 401:
                _LOGGER.error("Unauthorized request: %s", response.text)
                raise Exception("Unauthorized. Check your credentials or refresh token.")

            response.raise_for_status()
            return response.json()

        except Exception as e:
            # Log the exact error
            _LOGGER.error("Error during API request: %s", str(e))
            raise
