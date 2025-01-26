from homeassistant.components.camera import Camera
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up webcams for Øresundsbron."""
    api = hass.data[DOMAIN]["api"]
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
        return f"Webcam {self.cam_id.title()}"

    @property
    def is_streaming(self):
        return True

    async def async_camera_image(self):
        """Fetch the latest image from the webcam."""
        try:
            return await self.api.async_fetch_image(self._image_url)
        except Exception as e:
            _LOGGER.error("Failed to fetch image for %s: %s", self.name, e)
            return None

    async def async_update(self):
        """Update the camera entity (handled automatically)."""
        pass
