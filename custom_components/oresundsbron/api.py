import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class OresundsbronAPI:
    """Handle communication with the Øresundsbron API."""

    def __init__(self):
        self.base_url = "https://www.oresund.io"
        self.token = None
        self.refresh_token = None
        self.secret_key = "fqF*MVT6VUX03#wCUkbV"  # Constant value for X-Azure-Api-Secret

    async def authenticate(self, credentials):
        """Authenticate with the API and retrieve tokens."""
        url = f"{self.base_url}/api/auth/v1/login"
        headers = {"X-Azure-Api-Secret": self.secret_key}
        body = {**credentials, "rcToken": "app"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.token = data["token"]
                    self.refresh_token = data["refreshToken"]
                    _LOGGER.info("Authentication successful!")
                else:
                    error_text = await response.text()
                    _LOGGER.error(f"Authentication failed: {response.status} - {error_text}")
                    raise Exception(f"Authentication failed: {response.status}")

    async def async_make_request(self, endpoint, method="GET", params=None):
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Azure-Api-Secret": self.secret_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    _LOGGER.error(f"Request failed: {response.status} - {error_text}")
                    raise Exception(f"Request failed: {response.status}")
