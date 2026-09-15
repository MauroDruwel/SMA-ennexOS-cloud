from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import requests

from sma_ennexos_cloud.constants import ENNEXOS_GROUP_ID, ENNEXOS_LIVE_DATA_COMPONENT_ID
from sma_ennexos_cloud.status import get_live_data_status, get_portal_status

SAMPLE_STATUSPAGE_OPERATIONAL = {
    "components": [
        {
            "id": ENNEXOS_LIVE_DATA_COMPONENT_ID,
            "name": "Live Data",
            "status": "operational",
            "group_id": ENNEXOS_GROUP_ID,
        },
    ],
}

SAMPLE_STATUSPAGE_MAINTENANCE = {
    "components": [
        {
            "id": ENNEXOS_LIVE_DATA_COMPONENT_ID,
            "name": "Live Data",
            "status": "under_maintenance",
            "group_id": ENNEXOS_GROUP_ID,
        },
    ],
}


class TestStatus:
    def test_get_live_data_status_operational(self):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.json.return_value = SAMPLE_STATUSPAGE_OPERATIONAL
        mock_session.get.return_value = mock_resp

        assert get_live_data_status(session=mock_session) == "operational"

    def test_get_live_data_status_maintenance(self):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.json.return_value = SAMPLE_STATUSPAGE_MAINTENANCE
        mock_session.get.return_value = mock_resp

        assert get_live_data_status(session=mock_session) == "under_maintenance"

    def test_get_live_data_status_not_found(self):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"components": []}
        mock_session.get.return_value = mock_resp

        assert get_live_data_status(session=mock_session) == "unknown"

    def test_get_portal_status(self):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.json.return_value = SAMPLE_STATUSPAGE_MAINTENANCE
        mock_session.get.return_value = mock_resp

        portal_status = get_portal_status(session=mock_session)
        assert portal_status.live_data_status == "under_maintenance"

    def test_get_live_data_status_http_error(self):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
        mock_session.get.return_value = mock_resp

        with pytest.raises(requests.HTTPError):
            get_live_data_status(session=mock_session)
