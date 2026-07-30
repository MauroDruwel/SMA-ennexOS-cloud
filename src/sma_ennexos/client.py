"""Main client for the SMA ennexOS / Sunny Portal API."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

from .auth import login, refresh_access_token
from .constants import API_BASE, API_REQUEST_HEADERS, BROWSER_HEADERS, CLIENT_ID, TOKEN_URL
from .exceptions import APIError, AuthenticationError
from .models import EnergyData, PlantInfo, PowerData


class SmaClient:
    """Client for the SMA ennexOS / Sunny Portal API."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        self.username = username
        self.password = password
        self._http = requests.Session()
        self._http.headers.update(BROWSER_HEADERS)
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.component_id: Optional[str] = None
        self._plant_name: Optional[str] = None

    def login(self) -> None:
        if not self.username or not self.password:
            raise ValueError("Username and password are required")
        login(self)

    def _api_headers(self) -> dict[str, str]:
        if not self.access_token:
            raise AuthenticationError("Not logged in. Call login() first.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            **API_REQUEST_HEADERS,
        }

    def _get(self, path: str, **kwargs) -> requests.Response:
        r = self._http.get(
            f"{API_BASE}{path}",
            headers=self._api_headers(),
            **kwargs,
        )
        if r.status_code == 401:
            refresh_access_token(self)
            r = self._http.get(
                f"{API_BASE}{path}",
                headers=self._api_headers(),
                **kwargs,
            )
        if r.status_code == 401:
            raise AuthenticationError("Access denied after token refresh")
        r.raise_for_status()
        return r

    def _post(self, path: str, json_body: dict) -> requests.Response:
        r = self._http.post(
            f"{API_BASE}{path}",
            json=json_body,
            headers={**self._api_headers(), "Content-Type": "application/json"},
        )
        if r.status_code == 401:
            refresh_access_token(self)
            r = self._http.post(
                f"{API_BASE}{path}",
                json=json_body,
                headers={**self._api_headers(), "Content-Type": "application/json"},
            )
        if r.status_code == 401:
            raise AuthenticationError("Access denied after token refresh")
        r.raise_for_status()
        return r

    def discover_plant(self) -> str:
        nav = self._get("/navigation").json()
        plant_id = nav[0]["componentId"] if isinstance(nav, list) else nav["componentId"]
        self.component_id = str(plant_id)
        return self.component_id

    def get_current_power(self) -> PowerData:
        if not self.component_id:
            self.discover_plant()
        r = self._get(
            "/widgets/gauge/power",
            params={
                "componentId": self.component_id,
                "type": "PvProduction",
            },
        )
        data = r.json()
        return PowerData(
            value=data.get("value"),
            timestamp=data.get("timestamp", ""),
        )

    def get_plant_name(self) -> str:
        if not self.component_id:
            self.discover_plant()
        r = self._get(f"/plants/{self.component_id}")
        name = r.json().get("name", str(self.component_id))
        self._plant_name = name
        return name

    def get_daily_energy(self) -> EnergyData:
        if not self.component_id:
            self.discover_plant()
        now = datetime.now(timezone.utc)
        prev = now - timedelta(days=1)
        r = self._post(
            "/measurements/search",
            {
                "queryItems": [
                    {
                        "componentId": self.component_id,
                        "channelId": "Measurement.Metering.TotWhOut.Pv",
                        "resolution": "OneDay",
                        "timezone": "Europe/Brussels",
                        "aggregate": "Dif",
                        "multiAggregate": "Sum",
                    }
                ],
                "dateTimeBegin": prev.strftime("%Y-%m-%dT22:00:00.000Z"),
                "dateTimeEnd": now.strftime("%Y-%m-%dT22:00:00.000Z"),
            },
        )
        data = r.json()
        for channel in data:
            if channel["channelId"] == "Measurement.Metering.TotWhOut.Pv":
                for v in channel.get("values", []):
                    if v.get("value") is not None:
                        return EnergyData(
                            wh=v["value"],
                            timestamp=v.get("time", ""),
                        )
        return EnergyData(wh=0)

    def close(self) -> None:
        self._http.close()
