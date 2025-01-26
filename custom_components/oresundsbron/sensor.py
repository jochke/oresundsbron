from homeassistant.helpers.entity import Entity
from homeassistant.components.camera import Camera
from homeassistant.helpers.entity import DeviceInfo
from .api import OresundsbronAPI
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors for Øresundsbron from a config entry."""
    api = OresundsbronAPI()

    # Authenticate using an executor to avoid blocking the event loop
    await hass.async_add_executor_job(api.authenticate, config_entry.data)

    entities = [
        BridgeStatusSensor(api, "bridge_status"),
        QueueTimeSensor(api, "towardsSweden", "queue_time_sweden"),
        QueueTimeSensor(api, "towardsDenmark", "queue_time_denmark"),
        WebcamCamera(api, "pyloneast", "webcam_pyloneast"),
        WebcamCamera(api, "pylonwest", "webcam_pylonwest"),
        AccountHiddenSensor(api, "customerNo", "account_customer_no"),
        AccountHiddenSensor(api, "contracts", "account_contracts"),
        LastTripSensor(api, "last_trip")
    ]
    async_add_entities(entities)

class BridgeStatusSensor(Entity):
    """Sensor for the bridge status."""

    def __init__(self, api, unique_id):
        self.api = api
        self._state = None
        self._unique_id = unique_id

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return "Bridge Status"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        data = await self.api.async_make_request("/api/content/v1/bridge-status/status")
        self._state = data.get("status")

class QueueTimeSensor(Entity):
    """Sensor for the queue times."""

    def __init__(self, api, direction, unique_id):
        self.api = api
        self.direction = direction
        self._state = None
        self._unique_id = unique_id

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return f"Queue Time {self.direction.title()}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {"unit_of_measurement": "minutes"}

    async def async_update(self):
        data = await self.api.async_make_request("/api/content/v1/bridge-status/queueTime")
        self._state = data.get(self.direction, {}).get("value")

class WebcamCamera(Camera):
    """Camera for the webcam images."""

    def __init__(self, api, cam_id, unique_id):
        super().__init__()
        self.api = api
        self.cam_id = cam_id
        self._unique_id = unique_id
        self._image_url = f"https://cams.oresundsbron.com/{self.cam_id}"

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return f"Webcam {self.cam_id.title()}"

    @property
    def is_streaming(self):
        return True

    async def async_camera_image(self):
        return await self.api.async_fetch_image(self._image_url)

    async def async_update(self):
        # Webcam updates every 30 seconds, no additional logic needed as HA will handle intervals
        pass

class AccountHiddenSensor(Entity):
    """Hidden sensors for account information."""

    def __init__(self, api, sensor_type, unique_id):
        self.api = api
        self.sensor_type = sensor_type
        self._state = None
        self._unique_id = unique_id

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return f"Account {self.sensor_type.title()}"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        data = await self.api.async_make_request("/api/customer/v1/account")
        if self.sensor_type == "customerNo":
            self._state = data.get("customerNo")
        elif self.sensor_type == "contracts":
            self._state = len(data.get("contracts", []))

class LastTripSensor(Entity):
    """Sensor for the last trip details."""

    def __init__(self, api, unique_id):
        self.api = api
        self._state = None
        self._attributes = {}
        self._unique_id = unique_id

    @property
    def unique_id(self):
        return self._unique_id

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
        data = await self.api.async_make_request("/api/customer/v1/trips", params={"page": 1, "pageSize": 1})
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
