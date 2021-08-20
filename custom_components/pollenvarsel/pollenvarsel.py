"""Pollenvarsel library."""

import json
from typing import Optional

import aiohttp
from voluptuous.error import Error

from homeassistant.const import HTTP_OK, HTTP_UNAUTHORIZED

from .const import AREA_PATH, LOGGER
from .models import Area, PollenvarselResponse

BASE_URL = "https://pollenkontroll.no/api/middleware/pollen"

class Pollenvarsel:
    """Main class for handling connection with."""

    def __init__(
        self,
        area: Area,
        session: Optional[aiohttp.client.ClientSession] = None,
    ) -> None:
        """Initialize connection with Pollenvarsel."""

        self._session = session
        self.area: Area = area

    async def fetch(self) -> PollenvarselResponse:
        """Fetch data from Pollenvarsel."""

        if self._session is None:
            raise RuntimeError("Session required")

        area_path: str = AREA_PATH[Area(self.area)]
        URL = f"{BASE_URL}/{area_path}"
        LOGGER.debug("Fetching pollenvarsel for area=%s. URL=%s", self.area, URL)

        async with self._session.get(url=URL) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise Error(f"Unauthorized. {resp.status}")
            if resp.status != HTTP_OK:
                error_text = json.loads(await resp.text())
                raise Error(f"Not OK {resp.status} {error_text}")

            data = await resp.json()

        formatted_response = PollenvarselResponse.from_dict(data)
        LOGGER.debug("formatted_response %s", formatted_response)
        return formatted_response
