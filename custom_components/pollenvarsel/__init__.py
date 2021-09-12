"""The Pollenvarsel integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_AREA, DOMAIN as POLLENVARSEL_DOMAIN, PLATFORMS
from .coordinator import PollenvarselDataUpdateCoordinator
from .models import Area


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pollenvarsel from a config entry."""

    hass.data.setdefault(POLLENVARSEL_DOMAIN, {})

    coordinator = PollenvarselDataUpdateCoordinator(
        hass, 
        async_get_clientsession(hass), 
        Area.from_str(entry.data[CONF_AREA]),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[POLLENVARSEL_DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[POLLENVARSEL_DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
