"""
SMA ennexOS Python Library

A Python library for interacting with SMA ennexOS / Sunny Portal using
PKCE OAuth2 (no browser required).
"""

__version__ = "0.1.0"

from .client import SmaClient
from .exceptions import APIError, AuthenticationError, SmaError
from .models import EnergyData, PlantInfo, PowerData

__all__ = [
    "APIError",
    "AuthenticationError",
    "EnergyData",
    "PlantInfo",
    "PowerData",
    "SmaClient",
    "SmaError",
]
