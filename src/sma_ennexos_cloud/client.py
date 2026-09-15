"""Main client for the SMA ennexOS / Sunny Portal API."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import requests

from .auth import login, refresh_access_token
from .constants import API_BASE, API_REQUEST_HEADERS, BROWSER_HEADERS
from .exceptions import AuthenticationError
from .models import EnergyData, PlantInfo, PortalStatus, PowerData, WeatherData
from .status import get_live_data_status

_LOGGER = logging.getLogger(__name__)


class SmaClient:
    """Client for the SMA ennexOS / Sunny Portal API."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        component_id: str | None = None,
        check_portal_status: bool = False,
    ) -> None:
        self.username = username
        self.password = password
        self._http = requests.Session()
        self._http.headers.update(BROWSER_HEADERS)
        self.access_token: str | None = None
        self.refresh_token: str | None = None
        self.component_id: str | None = str(component_id) if component_id is not None else None
        self._plant_name: str | None = None
        self.check_portal_status = check_portal_status
        self._live_data_status: str | None = None

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

    def get_plants(self) -> list[PlantInfo]:
        """Return a list of all plants available to this account."""
        nav = self._get("/navigation").json()
        if isinstance(nav, dict):
            nav = [nav]
        plants: list[PlantInfo] = []
        for item in nav:
            is_plant = item.get("componentType") == "Plant"
            has_id_only = "componentType" not in item and "componentId" in item
            if is_plant or has_id_only:
                plants.append(
                    PlantInfo(
                        component_id=str(item["componentId"]),
                        name=item.get("name") or str(item["componentId"]),
                    )
                )
        return plants

    def discover_plant(self) -> str:
        """Discover the default plant if component_id is not already set."""
        if self.component_id:
            return self.component_id
        plants = self.get_plants()
        if not plants:
            raise ValueError("No plants found for this account")
        self.component_id = plants[0].component_id
        self._plant_name = plants[0].name
        return self.component_id

    def set_plant(self, component_id: str, name: str | None = None) -> None:
        """Set the active plant component_id."""
        self.component_id = str(component_id)
        if name:
            self._plant_name = name

    def get_current_power(self) -> PowerData:
        if self.check_portal_status:
            try:
                status = self.get_live_data_status()
                if status != "operational":
                    _LOGGER.warning(
                        "Sunny Portal Live Data is currently '%s'",
                        status,
                    )
            except Exception as err:  # noqa: BLE001
                _LOGGER.debug("Could not verify live data status: %s", err)

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
        if self._plant_name:
            return self._plant_name
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

    def get_live_data_status(self, force_refresh: bool = False) -> str:
        """Fetch Live Data status ('operational', 'under_maintenance', etc.)."""
        if self._live_data_status is None or force_refresh:
            self._live_data_status = get_live_data_status(session=self._http)
        return self._live_data_status

    def get_portal_status(self, force_refresh: bool = False) -> PortalStatus:
        """Fetch PortalStatus with live_data_status."""
        return PortalStatus(live_data_status=self.get_live_data_status(force_refresh=force_refresh))

    @property
    def live_data_status(self) -> str | None:
        """Return the most recently fetched Live Data status."""
        return self._live_data_status

    @property
    def portal_status(self) -> PortalStatus | None:
        """Return the most recently fetched portal status."""
        if self._live_data_status is not None:
            return PortalStatus(live_data_status=self._live_data_status)
        return None

    def get_weather(
        self,
        component_id: str | None = None,
        start_today_utc: str | None = None,
    ) -> WeatherData:
        """Fetch current weather and tomorrow's forecast for the plant."""
        cid = component_id or self.component_id
        if not cid:
            cid = self.discover_plant()

        if start_today_utc is None:
            now_local = datetime.now().astimezone()
            start_today = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
            start_today_utc = (
                start_today.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            )

        r = self._get(
            f"/components/{cid}/forecast/weather",
            params={"startTodayUtc": start_today_utc},
        )
        return WeatherData.from_dict(r.json())

    def close(self) -> None:
        self._http.close()

