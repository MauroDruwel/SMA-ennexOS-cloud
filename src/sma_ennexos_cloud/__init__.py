"""
SMA ennexOS Cloud Python Library

A Python library for interacting with SMA ennexOS / Sunny Portal using
PKCE OAuth2 (no browser required).
"""

__version__ = "0.2.4"

from .client import SmaClient
from .constants import (
    WEATHER_CONDITION_MAP,
    WEATHER_DESCRIPTIONS,
    WEATHER_ICON_FILES,
    normalize_weather_icon_id,
)
from .exceptions import APIError, AuthenticationError, SmaError
from .models import (
    EnergyData,
    PlantInfo,
    PortalStatus,
    PowerData,
    WeatherCurrent,
    WeatherData,
    WeatherTomorrow,
)
from .status import get_live_data_status, get_portal_status

__all__ = [
    "APIError",
    "AuthenticationError",
    "EnergyData",
    "PlantInfo",
    "PortalStatus",
    "PowerData",
    "SmaClient",
    "SmaError",
    "WEATHER_CONDITION_MAP",
    "WEATHER_DESCRIPTIONS",
    "WEATHER_ICON_FILES",
    "WeatherCurrent",
    "WeatherData",
    "WeatherTomorrow",
    "get_live_data_status",
    "get_portal_status",
    "normalize_weather_icon_id",
]
