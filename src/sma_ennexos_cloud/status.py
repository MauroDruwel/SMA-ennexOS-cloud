"""Status fetching for SMA ennexOS Live Data via statuspage.io."""

from __future__ import annotations

import requests

from .constants import ENNEXOS_GROUP_ID, ENNEXOS_LIVE_DATA_COMPONENT_ID, STATUS_PAGE_SUMMARY_URL
from .models import PortalStatus


def get_live_data_status(
    session: requests.Session | None = None,
    timeout: float = 10.0,
) -> str:
    """Fetch ennexOS Live Data status ('operational', 'under_maintenance', etc.)."""
    http = session or requests
    response = http.get(
        STATUS_PAGE_SUMMARY_URL,
        headers={"Accept": "application/json"},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()

    for c in data.get("components", []):
        c_id = str(c.get("id", ""))
        c_name = c.get("name", "")
        c_group_id = c.get("group_id")

        if c_id == ENNEXOS_LIVE_DATA_COMPONENT_ID or (
            c_name == "Live Data" and c_group_id == ENNEXOS_GROUP_ID
        ):
            return c.get("status", "unknown")

    return "unknown"


def get_portal_status(
    session: requests.Session | None = None,
    timeout: float = 10.0,
) -> PortalStatus:
    """Return PortalStatus containing live_data_status."""
    return PortalStatus(live_data_status=get_live_data_status(session=session, timeout=timeout))
