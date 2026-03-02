"""Config flow for Janet integration."""
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_WEBSOCKET_PORT, DEFAULT_WEBSOCKET_PORT

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST, default="localhost"): str,
    vol.Optional(CONF_PORT, default=8080): int,
    vol.Optional(CONF_WEBSOCKET_PORT, default=DEFAULT_WEBSOCKET_PORT): int,
})


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    host = data[CONF_HOST]
    port = data[CONF_PORT]
    
    url = f"http://{host}:{port}/health"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status != 200:
                    raise CannotConnect
                    
                data_response = await response.json()
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to Janet: %s", err)
            raise CannotConnect from err
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            raise CannotConnect from err

    return {"title": f"Janet ({host})"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Janet."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
