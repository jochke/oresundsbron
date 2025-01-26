from homeassistant.components.camera import Camera
from .const import DOMAIN
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up webcams for Øresundsbron."""
    api = hass.data.get(DOMAIN, {}).get("api")
    if not api:
        _LOGGER.error("API instance not found in hass.data for Øresundsbron")
        return

    async_add_entities([
        WebcamCamera(api, "pyloneast", "webcam_pyloneast"),
        WebcamCamera(api, "pylonwest", "webcam_pylonwest"),
    ])


class WebcamCamera(Camera):
    """Camera entity for Öresundsbron webcams."""

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
        if self.cam_id == "pyloneast":
            return "Pylon Cam East View"
        elif self.cam_id == "pylonwest":
            return "Pylon Cam West View"

    @property
    def icon(self):
        return "mdi:camera"

    @property
    def is_streaming(self):
        return True

    async def async_camera_image(self):
        """Fetch the latest image from the webcam."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._image_url) as response:
                    if response.status == 200:
                        return await response.read()
                    _LOGGER.error(
                        "Failed to fetch image for %s: %s", self.name, response.status
                    )
                    return None
        except Exception as e:
            _LOGGER.error("Error fetching image for %s: %s", self.name, e)
            return None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bridge_device")},
            "name": "The Bridge",
            "manufacturer": "Øresundsbron",
            "model": "Bridge API",
            "entry_type": None,
            "configuration_url": "https://www.oresundsbron.com/en/traffic-information",
        }

    async def async_update(self):
        """Periodic update (no additional state to fetch)."""
        pass
