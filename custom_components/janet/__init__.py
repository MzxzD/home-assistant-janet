"""
Janet AI Companion Integration for Home Assistant.

This integration allows Home Assistant to communicate with Janet,
enabling voice control, notifications, and bidirectional automation.
"""
import asyncio
import logging
from typing import Any

import aiohttp
import websockets
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = "janet"
PLATFORMS = [Platform.SENSOR, Platform.NOTIFY]

CONF_WEBSOCKET_PORT = "websocket_port"
DEFAULT_WEBSOCKET_PORT = 8765

SERVICE_SPEAK = "speak"
SERVICE_COMMAND = "command"

SPEAK_SCHEMA = vol.Schema({
    vol.Required("message"): cv.string,
    vol.Optional("voice"): cv.string,
})

COMMAND_SCHEMA = vol.Schema({
    vol.Required("command"): cv.string,
})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Janet component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Janet from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, 8080)
    ws_port = entry.data.get(CONF_WEBSOCKET_PORT, DEFAULT_WEBSOCKET_PORT)

    coordinator = JanetCoordinator(hass, host, port, ws_port)
    
    try:
        await coordinator.async_connect()
    except Exception as err:
        _LOGGER.error("Failed to connect to Janet: %s", err)
        raise ConfigEntryNotReady from err

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_speak(call: ServiceCall) -> None:
        """Handle the speak service call."""
        message = call.data["message"]
        voice = call.data.get("voice")
        await coordinator.speak(message, voice)

    async def handle_command(call: ServiceCall) -> None:
        """Handle the command service call."""
        command = call.data["command"]
        await coordinator.send_command(command)

    hass.services.async_register(DOMAIN, SERVICE_SPEAK, handle_speak, schema=SPEAK_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_COMMAND, handle_command, schema=COMMAND_SCHEMA)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_disconnect()

    return unload_ok


class JanetCoordinator:
    """Coordinator for Janet communication."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, ws_port: int):
        """Initialize the coordinator."""
        self.hass = hass
        self.host = host
        self.port = port
        self.ws_port = ws_port
        self.base_url = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{ws_port}"
        self.websocket = None
        self.is_connected = False
        self._listen_task = None
        self._session = None

    async def async_connect(self) -> None:
        """Connect to Janet."""
        self._session = aiohttp.ClientSession()
        
        try:
            async with self._session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status != 200:
                    raise ConfigEntryNotReady("Janet API not responding")
        except Exception as err:
            await self._session.close()
            raise ConfigEntryNotReady(f"Cannot connect to Janet: {err}") from err

        self._listen_task = asyncio.create_task(self._listen_websocket())
        self.is_connected = True
        _LOGGER.info("Connected to Janet at %s", self.base_url)

    async def async_disconnect(self) -> None:
        """Disconnect from Janet."""
        self.is_connected = False
        
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass

        if self.websocket:
            await self.websocket.close()

        if self._session:
            await self._session.close()

    async def _listen_websocket(self) -> None:
        """Listen for WebSocket messages from Janet."""
        while self.is_connected:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    self.websocket = websocket
                    _LOGGER.info("WebSocket connected to Janet")
                    
                    async for message in websocket:
                        await self._handle_message(message)
                        
            except Exception as err:
                _LOGGER.error("WebSocket error: %s", err)
                await asyncio.sleep(5)

    async def _handle_message(self, message: str) -> None:
        """Handle incoming WebSocket message."""
        try:
            import json
            data = json.loads(message)
            
            event_type = data.get("type")
            if event_type == "speech":
                self.hass.bus.async_fire(f"{DOMAIN}_speech", {"text": data.get("text")})
            elif event_type == "status":
                self.hass.bus.async_fire(f"{DOMAIN}_status", data)
            elif event_type == "command_result":
                self.hass.bus.async_fire(f"{DOMAIN}_command_result", data)
                
        except Exception as err:
            _LOGGER.error("Error handling message: %s", err)

    async def speak(self, message: str, voice: str | None = None) -> None:
        """Send a speak command to Janet."""
        payload = {"text": message}
        if voice:
            payload["voice"] = voice

        try:
            async with self._session.post(
                f"{self.base_url}/api/speak",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to send speak command: %s", await response.text())
        except Exception as err:
            _LOGGER.error("Error sending speak command: %s", err)

    async def send_command(self, command: str) -> None:
        """Send a voice command to Janet."""
        payload = {"command": command}

        try:
            async with self._session.post(
                f"{self.base_url}/api/command",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to send command: %s", await response.text())
        except Exception as err:
            _LOGGER.error("Error sending command: %s", err)

    async def get_status(self) -> dict[str, Any]:
        """Get Janet's current status."""
        try:
            async with self._session.get(
                f"{self.base_url}/api/status",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        except Exception as err:
            _LOGGER.error("Error getting status: %s", err)
            return {}
