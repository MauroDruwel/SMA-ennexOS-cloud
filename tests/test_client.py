from unittest.mock import MagicMock

import pytest

from sma_ennexos_cloud import SmaClient
from sma_ennexos_cloud.exceptions import AuthenticationError


class TestSmaClient:
    def test_init(self):
        client = SmaClient(username="user", password="pass")
        assert client.username == "user"
        assert client.password == "pass"
        assert client.access_token is None
        assert client.refresh_token is None
        assert client.component_id is None

    def test_login_requires_credentials(self):
        client = SmaClient()
        with pytest.raises(ValueError, match="Username and password"):
            client.login()

    def test_api_headers_raises_if_not_logged_in(self):
        client = SmaClient(username="u", password="p")
        with pytest.raises(AuthenticationError, match="Not logged in"):
            client._api_headers()

    def test_init_with_component_id(self):
        client = SmaClient(username="user", password="pass", component_id="12345")
        assert client.component_id == "12345"

    def test_get_plants(self, monkeypatch):
        client = SmaClient(username="user", password="pass")
        mock_nav = [
            {"componentType": "Plant", "name": "Plant One", "componentId": "111"},
            {"componentType": "Plant", "name": "Plant Two", "componentId": "222"},
            {"componentType": "Device", "name": "Inverter", "componentId": "333"},
        ]

        class MockResponse:
            def json(self):
                return mock_nav

        monkeypatch.setattr(client, "_get", lambda path: MockResponse())

        plants = client.get_plants()
        assert len(plants) == 2
        assert plants[0].component_id == "111"
        assert plants[0].name == "Plant One"
        assert plants[1].component_id == "222"
        assert plants[1].name == "Plant Two"

    def test_discover_plant_uses_first(self, monkeypatch):
        client = SmaClient(username="user", password="pass")
        mock_nav = [
            {"componentType": "Plant", "name": "Plant One", "componentId": "111"},
            {"componentType": "Plant", "name": "Plant Two", "componentId": "222"},
        ]

        class MockResponse:
            def json(self):
                return mock_nav

        monkeypatch.setattr(client, "_get", lambda path: MockResponse())

        plant_id = client.discover_plant()
        assert plant_id == "111"
        assert client.component_id == "111"
        assert client.get_plant_name() == "Plant One"

    def test_discover_plant_empty_raises(self, monkeypatch):
        client = SmaClient(username="user", password="pass")

        class MockResponse:
            def json(self):
                return []

        monkeypatch.setattr(client, "_get", lambda path: MockResponse())
        with pytest.raises(ValueError, match="No plants found"):
            client.discover_plant()

    def test_discover_plant_already_set(self):
        client = SmaClient(username="user", password="pass", component_id="999")
        assert client.discover_plant() == "999"

    def test_set_plant(self):
        client = SmaClient(username="user", password="pass")
        client.set_plant("888", "Custom Plant")
        assert client.component_id == "888"
        assert client.get_plant_name() == "Custom Plant"

    def test_get_current_power(self, monkeypatch):
        client = SmaClient(username="user", password="pass", component_id="111")
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"value": 2500.5, "timestamp": "2026-09-12T12:00:00Z"}
        monkeypatch.setattr(client, "_get", lambda path, **kwargs: mock_resp)

        power = client.get_current_power()
        assert power.value == 2500.5
        assert power.timestamp == "2026-09-12T12:00:00Z"

    def test_get_daily_energy(self, monkeypatch):
        client = SmaClient(username="user", password="pass", component_id="111")
        mock_resp = MagicMock()
        mock_resp.json.return_value = [
            {
                "channelId": "Measurement.Metering.TotWhOut.Pv",
                "values": [{"value": 15400.0, "time": "2026-09-12T18:00:00Z"}],
            }
        ]
        monkeypatch.setattr(client, "_post", lambda path, json_body: mock_resp)

        energy = client.get_daily_energy()
        assert energy.wh == 15400.0
        assert energy.timestamp == "2026-09-12T18:00:00Z"

    def test_get_daily_energy_empty(self, monkeypatch):
        client = SmaClient(username="user", password="pass", component_id="111")
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        monkeypatch.setattr(client, "_post", lambda path, json_body: mock_resp)

        energy = client.get_daily_energy()
        assert energy.wh == 0

    def test_http_get_with_refresh(self, monkeypatch):
        client = SmaClient(username="user", password="pass")
        client.access_token = "valid_token"

        resp_401 = MagicMock()
        resp_401.status_code = 401
        resp_200 = MagicMock()
        resp_200.status_code = 200

        client._http.get = MagicMock(side_effect=[resp_401, resp_200])
        monkeypatch.setattr("sma_ennexos_cloud.client.refresh_access_token", lambda c: None)

        r = client._get("/test")
        assert r == resp_200

    def test_http_post_with_refresh(self, monkeypatch):
        client = SmaClient(username="user", password="pass")
        client.access_token = "valid_token"

        resp_401 = MagicMock()
        resp_401.status_code = 401
        resp_200 = MagicMock()
        resp_200.status_code = 200

        client._http.post = MagicMock(side_effect=[resp_401, resp_200])
        monkeypatch.setattr("sma_ennexos_cloud.client.refresh_access_token", lambda c: None)

        r = client._post("/test", {})
        assert r == resp_200

    def test_close_idempotent(self):
        client = SmaClient()
        client.close()
        client.close()
