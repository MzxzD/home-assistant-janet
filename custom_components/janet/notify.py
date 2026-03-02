"""Notify platform for Janet integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.notify import BaseNotificationService
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, ATTR_VOICE

_LOGGER = logging.getLogger(__name__)


async def async_get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> JanetNotificationService | None:
    """Get the Janet notification service."""
    if discovery_info is None:
        return None
    
    entry_id = discovery_info["entry_id"]
    coordinator = hass.data[DOMAIN][entry_id]
    
    return JanetNotificationService(coordinator)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Any,
) -> None:
    """Set up Janet notify platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    await hass.helpers.discovery.async_load_platform(
        "notify",
        DOMAIN,
        {"entry_id": entry.entry_id},
        {},
    )


class JanetNotificationService(BaseNotificationService):
    """Implement the notification service for Janet."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize the service."""
        self._coordinator = coordinator

    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a message to Janet to speak."""
        voice = kwargs.get("data", {}).get(ATTR_VOICE)
        
        _LOGGER.debug("Sending message to Janet: %s (voice: %s)", message, voice)
        
        try:
            await self._coordinator.speak(message, voice)
        except Exception as err:
            _LOGGER.error("Failed to send message to Janet: %s", err)
