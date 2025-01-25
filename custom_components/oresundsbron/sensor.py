# sensor.py
from homeassistant.helpers.entity import Entity
from .api import OresundsbronAPI
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors for Öresundsbron from a config entry."""
    api = OresundsbronAPI()
    api.authenticate(config_entry.data)

    sensors = [
        BridgeStatusSensor(api),
        QueueTimeSensor(api, direction="towardsSweden"),
        QueueTimeSensor(api, direction="towardsDenmark"),
        WebcamSensor(api, "pyloneast"),
        WebcamSensor(api, "pylonwest"),
        AccountHiddenSensor(api, "customerNo"),
        AccountHiddenSensor(api, "contracts"),
        LastTripSensor(api)
    ]
    async_add_entities(sensors)

class BridgeStatusSensor(Entity):
    """Sensor for the bridge status."""

    def __init__(self, api):
        self.api = api
        self._state = None

    @property
    def name(self):
        return "Bridge Status"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        data = self.api.make_request("/api/content/v1/bridge-status/status")
        self._state = data.get("status")

class QueueTimeSensor(Entity):
    """Sensor for the queue times."""

    def __init__(self, api, direction):
        self.api = api
        self.direction = direction
        self._state = None

    @property
    def name(self):
        return f"Queue Time {self.direction.title()}"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        data = self.api.make_request("/api/content/v1/bridge-status/queueTime")
        self._state = data.get(self.direction, {}).get("value")

class WebcamSensor(Entity):
    """Sensor for the webcam images."""

    def __init__(self, api, cam_id):
        self.api = api
        self.cam_id = cam_id
        self._image = None

    @property
    def name(self):
        return f"Webcam {self.cam_id.title()}"

    @property
    def state(self):
        return "Image Available"

    @property
    def extra_state_attributes(self):
        return {"image_url": f"https://cams.oresundsbron.com/{self.cam_id}"}

    async def async_update(self):
        self._image = f"https://cams.oresundsbron.com/{self.cam_id}"

class AccountHiddenSensor(Entity):
    """Hidden sensors for account information."""

    def __init__(self, api, sensor_type):
        self.api = api
        self.sensor_type = sensor_type
        self._state = None

    @property
    def name(self):
        return f"Account {self.sensor_type.title()}"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        data = self.api.make_request("/api/customer/v1/account")
        if self.sensor_type == "customerNo":
            self._state = data.get("customerNo")
        elif self.sensor_type == "contracts":
            self._state = len(data.get("contracts", []))

class LastTripSensor(Entity):
    """Sensor for the last trip details."""

    def __init__(self, api):
        self.api = api
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Last Trip"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        data = self.api.make_request("/api/customer/v1/trips", params={"page": 1, "pageSize": 1})
        trips = data.get("trips", [])
        if trips:
            last_trip = trips[0]
            self._state = last_trip.get("id")
            self._attributes = {
                "dateTime": last_trip.get("dateTime"),
                "station": last_trip.get("station"),
                "type": last_trip.get("type"),
                "price_currencyCode": last_trip.get("price", {}).get("currencyCode"),
                "price_amountInclVAT": last_trip.get("price", {}).get("amountInclVAT"),
                "price_amount": last_trip.get("price", {}).get("amount"),
                "alpr": last_trip.get("alpr"),
                "bizzNr": last_trip.get("bizzNr"),
                "direction": last_trip.get("direction"),
                "actor": last_trip.get("actor")
            }