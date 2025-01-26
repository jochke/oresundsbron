from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, AUTH_URL
from .api import OresundsbronAPI
import voluptuous as vol

# Define the data schema for user input
data_schema = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str
})

class OresundsbronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Øresundsbron."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            api = OresundsbronAPI()
            try:
                # Attempt to authenticate with the API
                await self.hass.async_add_executor_job(api.authenticate, user_input)

                # If successful, create the entry
                return self.async_create_entry(title="Øresundsbron", data=user_input)

            except Exception:
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OresundsbronOptionsFlowHandler()

class OresundsbronOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for Øresundsbron."""

    def __init__(self):
        """Initialize options flow."""
        pass

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
