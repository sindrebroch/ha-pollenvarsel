"""Diagnostics support for Pollenvarsel."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.pollenvarsel.coordinator import PollenvarselDataUpdateCoordinator
from custom_components.pollenvarsel.models import PollenvarselResponse

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""

    coordinator: PollenvarselDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    data: PollenvarselResponse = coordinator.data

    return {
        "data": str(data),
    }
