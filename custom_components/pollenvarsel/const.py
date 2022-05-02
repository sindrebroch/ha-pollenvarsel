"""Constants for the Pollenvarsel integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

PLATFORMS = ["sensor"]

DOMAIN = "pollenvarsel"
CONF_AREA = "area"

BASE_URL = "https://pollenkontroll.no/api/middleware/pollen"
