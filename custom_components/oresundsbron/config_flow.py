from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN
from .api import OresundsbronAPI  # Ensure API is imported for validation

class OresundsbronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Öresundsbron."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            api = OresundsbronAPI()
            try:
                # Validate credentials
                await api.authenticate(user_input)
                return self.async_create_entry(title="Öresundsbron", data=user_input)
            except Exception:
                errors["base"] = "auth_failed"

        data_schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OresundsbronOptionsFlowHandler(config_entry)


class OresundsbronOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for Öresundsbron."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="Update Intervals", data=user_input)

        # Default values for update intervals
        current_options = self.config_entry.options
        update_interval_latest_trip = current_options.get("update_interval_latest_trip", 5)
        update_interval_bridge = current_options.get("update_interval_bridge", 5)
        update_interval_webcams = current_options.get("update_interval_webcams", 30)

        options_schema = vol.Schema({
            vol.Required(
                "update_interval_latest_trip",
                default=update_interval_latest_trip
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
            vol.Required(
                "update_interval_bridge",
                default=update_interval_bridge
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
            vol.Required(
                "update_interval_webcams",
                default=update_interval_webcams
            ): vol.All(vol.Coerce(int), vol.Range(min=10, max=60)),
        })

        return self.async_show_form(
            step_id="init", data_schema=options_schema
        )
