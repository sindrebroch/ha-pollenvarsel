"""Diagnostics support for Pollenvarsel."""

from __future__ import annotations

import datetime
import math

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import BASE_URL, DOMAIN
from .coordinator import PollenvarselDataUpdateCoordinator
from .models import Area, AREA_PATH, PollenvarselResponse


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""

    coordinator: PollenvarselDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]
    data: PollenvarselResponse = coordinator.data

    area: Area = coordinator.area
    area_path: str = AREA_PATH[Area(area)]
    timestamp = datetime.datetime.now().timestamp() * 1000

    return {
        "data": str(data),
        "area": str(area),
        "url": f"{BASE_URL}/{area_path}?t={math.floor(timestamp)}",
    }
