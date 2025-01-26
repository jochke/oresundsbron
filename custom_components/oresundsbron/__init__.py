# __init__.py
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, PLATFORMS
from .api import OresundsbronAPI
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Øresundsbron integration from YAML configuration."""
    # We don't support YAML setup for this integration
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Øresundsbron integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Initialize the API object
    api = OresundsbronAPI()
    await api.authenticate(entry.data)

    # Store the API object and entry data in hass.data
    hass.data[DOMAIN]["api"] = api
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the setup to the sensor and camera platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("Øresundsbron integration is set up.")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        # Remove the API reference if this is the last entry
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    _LOGGER.info("Øresundsbron integration is unloaded.")
    return unload_ok