"""The Pollenvarsel coordinator."""
from __future__ import annotations

from datetime import timedelta

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from voluptuous.error import Error

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PollenvarselApiClient
from .const import DOMAIN as POLLENVARSEL_DOMAIN, LOGGER
from .models import Area, PollenvarselResponse

class PollenvarselDataUpdateCoordinator(DataUpdateCoordinator[PollenvarselResponse]):
    """Class to manage fetching Pollenvarsel data API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        area: Area,
    ) -> None:
        """Initialize."""

        update_interval = timedelta(minutes=60)

        self.area: Area = area
        self.api = PollenvarselApiClient(area=area, session=session)

        self._attr_device_info: DeviceInfo = {
            "identifiers": {(POLLENVARSEL_DOMAIN, self.area.name)},
            "name": f"Pollenvarsel {self.area.name.title()}",
            "model": "Pollenvarsel",
            "manufacturer": f"{self.area.name.title()}",
        }

        super().__init__(
            hass,
            LOGGER,
            name=POLLENVARSEL_DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> PollenvarselResponse:
        """Update data via library."""

        try:
            return await self.api.fetch()
        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error
