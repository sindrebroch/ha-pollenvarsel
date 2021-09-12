"""Sensor file for pollenvarsel."""

from typing import List, Optional, cast

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_AREA, DOMAIN as POLLENVARSEL_DOMAIN, LOGGER
from .coordinator import PollenvarselDataUpdateCoordinator
from .models import Allergen, Area, Day, Entities, PollenForecast, PollenvarselResponse


SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=Entities.Salix.value,
        name="Salix",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=Entities.BJORK.value,
        name="Bjørk",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=Entities.OR.value,
        name="Or",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=Entities.HASSEL.value,
        name="Hassel",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=Entities.GRESS.value,
        name="Gress",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=Entities.BUROT.value,
        name="Burot",
        icon="mdi:tree",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add Pollenvarsel entities from a config_entry."""

    coordinator: PollenvarselDataUpdateCoordinator = hass.data[POLLENVARSEL_DOMAIN][entry.entry_id]

    area: Optional[Area] = Area.from_str(entry.data[CONF_AREA])

    if area is not None:
        for sensor_description in SENSORS:
            async_add_entities(
                PollenvarselSensor(area, coordinator, sensor_description, Day.TODAY),
                PollenvarselSensor(area, coordinator, sensor_description, Day.TOMORROW),
            )


class PollenvarselSensor(CoordinatorEntity, SensorEntity):
    """Define a Pollenvarsel entity."""

    coordinator: PollenvarselDataUpdateCoordinator

    def __init__(
        self,
        area: Area,
        coordinator: PollenvarselDataUpdateCoordinator,
        description: SensorEntityDescription,
        day: Day,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)

        self.coordinator = coordinator
        self.entity_description = description

        self.day: Day = Day(day)
        self.area: Area = Area(area)
        self.sensor_data: str = _get_sensor_data(coordinator.data, day, description.key)

        self._attr_device_info = coordinator._attr_device_info

        if day == Day.TODAY:
            self._attr_name = f"{self.area.name.title()} {description.key}"
            self._attr_unique_id = f"{self.area.name}_{description.key}"
        else:
            day_string: str = "imorgen" if day == Day.TOMORROW else ""
            self._attr_name = f"{self.area.name.title()} {description.key} {day_string}"
            self._attr_unique_id = f"{self.area.name}_{description.key}_{day_string}"

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(
            self.coordinator.data, self.day, self.entity_description.key
        )
        self.async_write_ha_state()


def _get_sensor_data(sensors: PollenvarselResponse, day: Day, sensor_name: str) -> str:
    """Get sensor data."""

    forecasts: List[PollenForecast] = sensors.forecast
    current_day_forecast: PollenForecast = forecasts.__getitem__(day.value)
    allergens: List[Allergen] = current_day_forecast.allergens

    for allergen in allergens:
        if allergen.name.lower() == sensor_name.lower():
            return allergen.level_description

    LOGGER.debug("Could not find state for sensor.%s", sensor_name)

    return "Not found"
