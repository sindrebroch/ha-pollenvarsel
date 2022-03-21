"""Models for Pollenvarsel."""

from enum import Enum, IntEnum
from typing import Any, Dict, List

import attr

from .const import LOGGER


class Day(IntEnum):
    """Enum representing type of Day."""

    TODAY = 0
    TOMORROW = 1

class Entities(Enum):
    SALIX = "salix"
    BJORK = "bjørk"
    OR = "or"
    HASSEL = "hassel"
    GRESS = "gress"
    BUROT = "burot"

class Area(Enum):
    """Enum representing area."""

    TROMS = "troms"
    FINNMARK = "finnmark"
    NORDLAND = "nordland"
    ROGALAND = "rogaland"
    SØRLANDET = "sørlandet"
    TRØNDELAG = "trøndelag"
    HORDALAND = "hordaland"
    INDRE_ØSTLAND = "indre_østland"
    MØRE_OG_ROMSDAL = "møre_og_romsdal"
    SOGN_OG_FJORDANE = "sogn_og_fjordane"
    ØSTLANDET_MED_OSLO = "østlandet_med_oslo"
    SENTRALE_FJELLSTRØK_I_SØR_NORGE = "sentrale_fjellstrøk_i_sør_norge"

    @staticmethod
    def from_str(label: str) -> "Area":
        """Find enum from string."""

        for area in Area:
            if label.lower() == area.name.lower():
                return area

        raise NotImplementedError


AREA_PATH: Dict[Area, str] = {
    Area.TROMS: "50a10889-9132-402a-a14e-c98cd872bff3",
    Area.NORDLAND: "2680e4ac-1317-4423-baeb-b804e57c8285",
    Area.ROGALAND: "901f3d22-b95f-4b64-a181-0b847b76b1a3",
    Area.FINNMARK: "9a18de3a-06a3-4cb8-8eb0-9e42ed804ea4",
    Area.SØRLANDET: "fc1c3ec7-a311-4ce0-a5a7-b0e79813ecf7",
    Area.HORDALAND: "ed8a16e7-75aa-4994-b3b8-0a5b88c8f81e",
    Area.TRØNDELAG: "f2911165-bc25-494d-a331-42c05e14cfe2",
    Area.INDRE_ØSTLAND: "7c2de2d4-2ad0-45cb-bf25-10eeaf88c202",
    Area.MØRE_OG_ROMSDAL: "6ea90b97-547e-40ee-8eca-a2eb788ad567",
    Area.SOGN_OG_FJORDANE: "5d6f74b5-5e23-4271-ad85-b18452a7f849",
    Area.ØSTLANDET_MED_OSLO: "b5bb4856-2117-433d-bf18-53504ef2f101",
    Area.SENTRALE_FJELLSTRØK_I_SØR_NORGE: "a3d194c3-7788-45ae-82e7-e8be1d75a713",
}

@attr.s(auto_attribs=True)
class PollenStation:
    """Class representing PollenStation."""

    name: str
    country_code: str
    distance_in_km: float

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PollenStation":
        """Transform data to dict."""

        LOGGER.debug("PollenStation=%s", data)

        return PollenStation(
            name=data["name"],
            country_code=data["country_code"],
            distance_in_km=float(data["distance_in_km"]),
        )


@attr.s(auto_attribs=True)
class Allergen:
    """Class representing Allergen."""

    name: str
    latin_name: str
    level: float
    no_data: bool
    out_of_season: bool

    @staticmethod
    def from_dict(data: List[Dict[str, Any]]) -> List["Allergen"]:
        """Transform data to dict."""

        LOGGER.debug("Allergen=%s", data)

        allergens = []
        for allergen in data:
            allergens.append(
                Allergen(
                    name=allergen["name"],
                    latin_name=allergen["latin_name"],
                    level=float(allergen["level"]),
                    no_data=bool(allergen["no_data"]),
                    out_of_season=bool(allergen["out_of_season"]),
                )
            )
        return allergens


@attr.s(auto_attribs=True)
class PollenForecast:
    """Class representing PollenForecast."""

    date: str
    allergens: List["Allergen"]

    @staticmethod
    def from_dict(data: List[Dict[str, Any]]) -> List["PollenForecast"]:
        """Transform data to dict."""

        LOGGER.debug("PollenForecast from_dict %s", data)

        forecasts = []
        for forecast in data:
            forecast_allergens: List[Dict[str, Any]] = forecast["allergens"]
            forecasts.append(
                PollenForecast(
                    date=forecast["date"],
                    allergens=Allergen.from_dict(forecast_allergens),
                )
            )
        return forecasts


@attr.s(auto_attribs=True)
class PollenvarselResponse:
    """Class representing Pollenvarsel."""

    status: int
    pollen_station: "PollenStation"
    forecast: List["PollenForecast"]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PollenvarselResponse":
        """Transform data to dict."""

        LOGGER.debug("PollenvarselResponse=%s", data)

        forecast: List[Dict[str, Any]] = data["forecast"]
        pollen_station: Dict[str, Any] = data["pollen_station"]

        return PollenvarselResponse(
            status=data["status"],
            forecast=PollenForecast.from_dict(forecast),
            pollen_station=PollenStation.from_dict(pollen_station),
        )
