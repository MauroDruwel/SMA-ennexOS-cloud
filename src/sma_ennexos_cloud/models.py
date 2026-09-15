from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .utils import _asdict


class _ToDictMixin:
    def to_dict(self) -> dict[str, Any]:
        return _asdict(self)


@dataclass
class PowerData(_ToDictMixin):
    value: float | None = None
    timestamp: str = ""


@dataclass
class EnergyData(_ToDictMixin):
    wh: float = 0
    timestamp: str = ""


@dataclass
class PlantInfo(_ToDictMixin):
    component_id: str
    name: str = ""


@dataclass
class PortalStatus(_ToDictMixin):
    live_data_status: str = "unknown"


@dataclass
class WeatherCurrent(_ToDictMixin):
    time: str = ""
    icon_id: int | None = None
    temperature: float | None = None
    condition: str | None = None
    description: str | None = None
    icon_file: str | None = None


@dataclass
class WeatherTomorrow(_ToDictMixin):
    date: str = ""
    icon_id: int | None = None
    min_temperature: float | None = None
    max_temperature: float | None = None
    condition: str | None = None
    description: str | None = None
    icon_file: str | None = None


@dataclass
class WeatherData(_ToDictMixin):
    city: str | None = None
    now: WeatherCurrent | None = None
    tomorrow: WeatherTomorrow | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WeatherData:
        return parse_weather_data(data)


def parse_weather_data(data: dict[str, Any]) -> WeatherData:
    """Parse raw Sunny Portal weather API JSON dictionary into WeatherData."""
    from .constants import (
        WEATHER_CONDITION_MAP,
        WEATHER_DESCRIPTIONS,
        WEATHER_ICON_FILES,
        normalize_weather_icon_id,
    )

    city = data.get("city")
    now_raw = data.get("now")
    now_model: WeatherCurrent | None = None
    if isinstance(now_raw, dict):
        raw_icon = now_raw.get("iconId")
        norm_icon = normalize_weather_icon_id(raw_icon) if isinstance(raw_icon, int) else None
        now_model = WeatherCurrent(
            time=str(now_raw.get("time", "")),
            icon_id=raw_icon,
            temperature=now_raw.get("temperature"),
            condition=WEATHER_CONDITION_MAP.get(norm_icon) if norm_icon is not None else None,
            description=WEATHER_DESCRIPTIONS.get(norm_icon) if norm_icon is not None else None,
            icon_file=WEATHER_ICON_FILES.get(norm_icon) if norm_icon is not None else None,
        )

    tomorrow_raw = data.get("tomorrow")
    tomorrow_model: WeatherTomorrow | None = None
    if isinstance(tomorrow_raw, dict):
        raw_icon = tomorrow_raw.get("iconId")
        norm_icon = normalize_weather_icon_id(raw_icon) if isinstance(raw_icon, int) else None
        tomorrow_model = WeatherTomorrow(
            date=str(tomorrow_raw.get("date", "")),
            icon_id=raw_icon,
            min_temperature=tomorrow_raw.get("minTemperature"),
            max_temperature=tomorrow_raw.get("maxTemperature"),
            condition=WEATHER_CONDITION_MAP.get(norm_icon) if norm_icon is not None else None,
            description=WEATHER_DESCRIPTIONS.get(norm_icon) if norm_icon is not None else None,
            icon_file=WEATHER_ICON_FILES.get(norm_icon) if norm_icon is not None else None,
        )

    return WeatherData(city=city, now=now_model, tomorrow=tomorrow_model)
