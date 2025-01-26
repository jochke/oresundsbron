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
    await api.authenticate(config_entry.data)

    # Fetch account details to retrieve contracts
    account_data = await api.async_make_request("/api/customer/v1/account")
    contracts = account_data.get("contracts", [])

    entities = []

    # Create entities for each contract (Agreement Devices)
    for contract in contracts:
        contract_no = contract.get("contractNo")
        entities.append(
            AgreementStatusSensor(api, contract, f"agreement_status_{contract_no}")
        )
        entities.append(
            AgreementDeviceLatestTripSensor(api, contract, f"last_trip_{contract_no}")
        )

    # Add the single Bridge Device entities
    entities.extend([
        BridgeStatusSensor(api, "bridge_status"),
        QueueTimeSensor(api, "towardsSweden", "queue_time_sweden"),
        QueueTimeSensor(api, "towardsDenmark", "queue_time_denmark"),
        WebcamCamera(api, "pyloneast", "webcam_pyloneast"),
        WebcamCamera(api, "pylonwest", "webcam_pylonwest"),
        BridgeWeatherSensor(api, "bridge_weather_temperature", "temperature"),
        BridgeWeatherSensor(api, "bridge_weather_windspeed", "windspeed"),
        BridgeWeatherSensor(api, "bridge_weather_direction", "direction"),
    ])

    async_add_entities(entities)

class AgreementStatusSensor(Entity):
    """Sensor for agreement status."""

    def __init__(self, api, contract, unique_id):
        self.api = api
        self.contract = contract
        self.contract_no = contract.get("contractNo")
        self._unique_id = unique_id
        self._state = None

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return "Status"

    @property
    def state(self):
        return self.contract.get("status")

    @property
    def icon(self):
        return "mdi:card-account-details"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"agreement_{self.contract_no}")},
            "name": f"Agreement {self.contract_no}",
            "manufacturer": "Øresundsbron",
            "model": self.contract.get("contractType"),
            "entry_type": None,
            "configuration_url": "https://www.oresundsbron.com/account/login",
        }

    async def async_update(self):
        self._state = self.contract.get("status")

class AgreementDeviceLatestTripSensor(Entity):
    """Sensor for the latest trip details under an agreement."""

    def __init__(self, api, contract, unique_id):
        self.api = api
        self.contract = contract
        self.contract_no = contract.get("contractNo")
        self._unique_id = unique_id
        self._state = None
        self._attributes = {}

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return "Latest Trip"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        return "mdi:car"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"agreement_{self.contract_no}")},
            "name": f"Agreement {self.contract_no}",
            "manufacturer": "Øresundsbron",
            "model": self.contract.get("contractType"),
            "entry_type": None,
            "configuration_url": "https://www.oresundsbron.com/account/login",
        }

    async def async_update(self):
        """Fetch latest trip details for the agreement."""
        data = await self.api.async_make_request(
            "/api/customer/v1/trips", params={"contractNo": self.contract_no, "page": 1, "tripsType": "Trip", "pageSize": 3}
        )
        trips = data.get("trips", [])
        if trips:
            last_trip = trips[0]
            direction = last_trip.get("direction")
            self._state = last_trip.get("dateTime")
            self._attributes = {
                "trip_id": last_trip.get("id"),
                "Price incl. VAT": last_trip.get("price", {}).get("amountInclVAT"),
                "License Plate": last_trip.get("alpr"),
                "Contract No": self.contract_no,
                "Bizz No": last_trip.get("bizzNr"),
                "Currency": last_trip.get("price", {}).get("currencyCode"),
                "Price ex. VAT": last_trip.get("price", {}).get("amount"),
                "direction": "SE" if direction == "countries.sweden" else "DK",
                "actor": last_trip.get("actor"),
            }

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

    @property
    def icon(self):
        return "mdi:bridge"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bridge_device")},
            "name": "The Bridge",
            "manufacturer": "Øresundsbron",
            "model": "Bridge API",
            "entry_type": None,
            "configuration_url": "https://www.oresundsbron.com/account/login",
        }

    async def async_update(self):
        """Fetch bridge status."""
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
        return f"Toll Waiting Time Towards {self.direction.title()}"

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:clock-outline"

    @property
    def extra_state_attributes(self):
        return {"unit_of_measurement": "Minutes"}

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bridge_device")},
            "name": "The Bridge",
            "manufacturer": "Øresundsbron",
            "model": "Bridge API",
            "entry_type": None,
            "configuration_url": "https://www.oresundsbron.com/account/login",
        }

    async def async_update(self):
        """Fetch queue times."""
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
    def icon(self):
        return "mdi:video"

    @property
    def is_streaming(self):
        return True

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bridge_device")},
            "name": "The Bridge",
            "manufacturer": "Øresundsbron",
            "model": "Bridge API",
            "entry_type": None,
            "configuration_url": "https://www.oresundsbron.com/account/login",
        }

    async def async_camera_image(self):
        return await self.api.async_fetch_image(self._image_url)

    async def async_update(self):
        pass

class BridgeWeatherSensor(Entity):
    """Sensor for bridge weather conditions."""

    def __init__(self, api, unique_id, sensor_type):
        self.api = api
        self._state = None
        self._attributes = {}
        self._unique_id = unique_id
        self.sensor_type = sensor_type

    @property
    def unit_of_measurement(self):
        if self.sensor_type == "temperature":
            return "°C"
        elif self.sensor_type == "windspeed":
            return "m/s"
        elif self.sensor_type == "direction":
            return None