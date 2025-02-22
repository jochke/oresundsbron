# const.py
DOMAIN = "oresundsbron"

# Default Update Intervals (in minutes/seconds)
DEFAULT_UPDATE_INTERVAL_LATEST_TRIP = 5  # minutes
DEFAULT_UPDATE_INTERVAL_BRIDGE = 5  # minutes
DEFAULT_UPDATE_INTERVAL_WEBCAMS = 30  # seconds

# API Endpoints
AUTH_URL = "/api/auth/v1/login"
BRIDGE_STATUS_URL = "/api/content/v1/bridge-status/status"
QUEUE_TIME_URL = "/api/content/v1/bridge-status/queueTime"
WEATHER_URL = "/api/content/v1/bridge-status/weather"
LATEST_TRIP_URL = "/api/customer/v1/trips"
ACCOUNT_URL = "/api/customer/v1/account"

# Supported platforms
PLATFORMS = ["sensor", "camera"]
