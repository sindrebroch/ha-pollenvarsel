"""Sensor file for pollenvarsel."""

from datetime import date, datetime
from typing import Optional, cast

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_AREA, DOMAIN as POLLENVARSEL_DOMAIN
from .coordinator import PollenvarselDataUpdateCoordinator
from .models import Allergen, Area, Day


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add Pollenvarsel entities from a config_entry."""

    coordinator: PollenvarselDataUpdateCoordinator = hass.data[POLLENVARSEL_DOMAIN][
        entry.entry_id
    ]

    area: Optional[Area] = Area.from_str(entry.data[CONF_AREA])

    if area is not None:
        for forecast in coordinator.data.forecasts:
            day = datetime.strptime(forecast.date, "%Y-%m-%d").date()
            day_type = Day.TODAY if day == date.today() else Day.TOMORROW

            for allergen in forecast.allergens:
                async_add_entities(
                    [PollenvarselSensor(area, coordinator, day_type, allergen)]
                )


class PollenvarselSensor(CoordinatorEntity, SensorEntity):
    """Define a Pollenvarsel entity."""

    coordinator: PollenvarselDataUpdateCoordinator

    def __init__(
        self,
        area: Area,
        coordinator: PollenvarselDataUpdateCoordinator,
        day: Day,
        allergen: Allergen,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)

        self.coordinator = coordinator
        self.allergen = allergen
        self._attr_icon = "mdi:tree"
        self._attr_name = allergen.name

        self.day: Day = Day(day)
        self.area: Area = Area(area)
        self.sensor_data: str = _get_sensor_data(allergen)

        self._attr_device_info = coordinator._attr_device_info

        if day == Day.TODAY:
            self._attr_name = f"{self.area.name.title()} {allergen.name}"
            self._attr_unique_id = f"{self.area.name}_{allergen.name}"
        else:
            day_string: str = "imorgen" if day == Day.TOMORROW else ""
            self._attr_name = f"{self.area.name.title()} {allergen.name} {day_string}"
            self._attr_unique_id = f"{self.area.name}_{allergen.name}_{day_string}"

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(self.allergen)
        super()._handle_coordinator_update()


def _get_sensor_data(allergen: Allergen) -> str:
    """Get sensor data."""

    if allergen.out_of_season:
        return "Out of season"
    elif allergen.no_data:
        return "No data"
    return allergen.level
