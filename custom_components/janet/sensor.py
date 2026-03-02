"""Sensor platform for Janet integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from datetime import timedelta

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Janet sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    update_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="janet_status",
        update_method=coordinator.get_status,
        update_interval=SCAN_INTERVAL,
    )
    
    await update_coordinator.async_config_entry_first_refresh()
    
    sensors = [
        JanetStatusSensor(coordinator, update_coordinator, entry),
        JanetConversationSensor(coordinator, update_coordinator, entry),
        JanetMemorySensor(coordinator, update_coordinator, entry),
    ]
    
    async_add_entities(sensors)


class JanetSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Janet sensors."""

    def __init__(
        self,
        coordinator: Any,
        update_coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(update_coordinator)
        self._coordinator = coordinator
        self._entry = entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Janet AI Companion",
            "manufacturer": "Janet Project",
            "model": "janet-seed",
            "sw_version": "1.0.0",
        }


class JanetStatusSensor(JanetSensorBase):
    """Sensor for Janet's overall status."""

    _attr_name = "Janet Status"
    _attr_icon = "mdi:robot"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_status"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if not self._coordinator.is_connected:
            return "disconnected"
        
        data = self.coordinator.data
        if not data:
            return "unknown"
        
        return data.get("state", "idle")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        data = self.coordinator.data
        if not data:
            return {}
        
        return {
            "connected": self._coordinator.is_connected,
            "host": self._entry.data[CONF_HOST],
            "uptime": data.get("uptime"),
            "model": data.get("model"),
            "voice_enabled": data.get("voice_enabled", False),
        }


class JanetConversationSensor(JanetSensorBase):
    """Sensor for Janet's conversation state."""

    _attr_name = "Janet Conversation"
    _attr_icon = "mdi:message-text"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_conversation"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        data = self.coordinator.data
        if not data:
            return "inactive"
        
        return "active" if data.get("in_conversation", False) else "inactive"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        data = self.coordinator.data
        if not data:
            return {}
        
        return {
            "last_input": data.get("last_input"),
            "last_response": data.get("last_response"),
            "turn_count": data.get("turn_count", 0),
        }


class JanetMemorySensor(JanetSensorBase):
    """Sensor for Janet's memory usage."""

    _attr_name = "Janet Memory"
    _attr_icon = "mdi:database"
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_native_unit_of_measurement = "MB"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_memory"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        data = self.coordinator.data
        if not data:
            return None
        
        memory_bytes = data.get("memory_usage", 0)
        return round(memory_bytes / (1024 * 1024), 2)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        data = self.coordinator.data
        if not data:
            return {}
        
        return {
            "green_vault_entries": data.get("green_vault_entries", 0),
            "blue_vault_active": data.get("blue_vault_active", False),
            "red_vault_entries": data.get("red_vault_entries", 0),
        }
