"""Config flow for Pollenvarsel integration."""
from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PollenvarselApiClient
from .const import CONF_AREA, DOMAIN as POLLENVARSEL_DOMAIN, LOGGER
from .models import Area, AREA_PATH

AREA_KEYS: list[str] = [area.name for area in AREA_PATH.keys()]
SCHEMA = vol.Schema({vol.Required(CONF_AREA): vol.In(sorted(AREA_KEYS))})


class PollenvarselFlowHandler(config_entries.ConfigFlow, domain=POLLENVARSEL_DOMAIN):
    """Config flow for Pollenvarsel."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:

            optional_area: str | None = user_input.get(CONF_AREA)

            if optional_area is not None:

                area: Area = Area.from_str(optional_area)

                await self.async_set_unique_id(area.name)
                self._abort_if_unique_id_configured()

                api = PollenvarselApiClient(
                    area=area, 
                    session=async_get_clientsession(self.hass),
                )

                errors: dict[str, Any] = {}

                try:
                    await api.fetch()
                except aiohttp.ClientError as error:
                    errors["base"] = "cannot_connect"
                    LOGGER.warning("error=%s. errors=%s", error, errors)

                if errors:
                    return self.async_show_form(
                        step_id="user", data_schema=SCHEMA, errors=errors
                    )

                return self.async_create_entry(
                    title=area.name.title(),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors={},
        )
