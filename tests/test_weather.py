from __future__ import annotations

from unittest.mock import MagicMock

from sma_ennexos_cloud.client import SmaClient
from sma_ennexos_cloud.constants import (
    WEATHER_CONDITION_MAP,
    WEATHER_DESCRIPTIONS,
    WEATHER_ICON_FILES,
    normalize_weather_icon_id,
)
from sma_ennexos_cloud.models import WeatherCurrent, WeatherData, WeatherTomorrow


class TestWeatherConstants:
    def test_normalize_weather_icon_id(self):
        assert normalize_weather_icon_id(0) == 0
        assert normalize_weather_icon_id(2) == 2
        assert normalize_weather_icon_id(99) == 99
        assert normalize_weather_icon_id(100) == 0
        assert normalize_weather_icon_id(102) == 2
        assert normalize_weather_icon_id(180) == 80

    def test_mappings_exist(self):
        # Verify typical weather icon ids are mapped
        for icon_id in (0, 1, 2, 3, 10, 20, 30, 31, 32, 50, 60, 80, 90):
            assert icon_id in WEATHER_DESCRIPTIONS
            assert icon_id in WEATHER_CONDITION_MAP
            assert icon_id in WEATHER_ICON_FILES

        assert WEATHER_CONDITION_MAP[0] == "sunny"
        assert WEATHER_CONDITION_MAP[1] == "partlycloudy"
        assert WEATHER_CONDITION_MAP[2] == "cloudy"
        assert WEATHER_CONDITION_MAP[32] == "pouring"
        assert WEATHER_CONDITION_MAP[80] == "lightning"


class TestWeatherModels:
    def test_defaults(self):
        now = WeatherCurrent()
        assert now.time == ""
        assert now.icon_id is None
        assert now.temperature is None
        assert now.condition is None

        tomorrow = WeatherTomorrow()
        assert tomorrow.date == ""
        assert tomorrow.icon_id is None
        assert tomorrow.min_temperature is None
        assert tomorrow.max_temperature is None

        data = WeatherData()
        assert data.city is None
        assert data.now is None
        assert data.tomorrow is None

    def test_from_dict_full(self):
        raw = {
            "now": {
                "time": "2026-09-15T12:00:00Z",
                "iconId": 2,
                "temperature": 24,
            },
            "tomorrow": {
                "date": "2026-09-15T22:00:00Z",
                "iconId": 100,  # test normalization: 100 -> 0 (sunny / cloudless)
                "minTemperature": 13,
                "maxTemperature": 18,
            },
            "city": "Tielt",
        }
        weather = WeatherData.from_dict(raw)
        assert weather.city == "Tielt"
        assert weather.now is not None
        assert weather.now.time == "2026-09-15T12:00:00Z"
        assert weather.now.icon_id == 2
        assert weather.now.temperature == 24
        assert weather.now.condition == "cloudy"
        assert weather.now.description == "Cloudy"
        assert weather.now.icon_file == "803D.png"

        assert weather.tomorrow is not None
        assert weather.tomorrow.date == "2026-09-15T22:00:00Z"
        assert weather.tomorrow.icon_id == 100
        assert weather.tomorrow.min_temperature == 13
        assert weather.tomorrow.max_temperature == 18
        assert weather.tomorrow.condition == "sunny"
        assert weather.tomorrow.description == "Cloudless"
        assert weather.tomorrow.icon_file == "800D.png"

        d = weather.to_dict()
        assert d["city"] == "Tielt"
        assert d["now"]["temperature"] == 24
        assert d["tomorrow"]["min_temperature"] == 13

    def test_from_dict_partial_and_empty(self):
        weather = WeatherData.from_dict({})
        assert weather.city is None
        assert weather.now is None
        assert weather.tomorrow is None

        raw_partial = {
            "now": {"iconId": "invalid", "temperature": 19.5},
            "tomorrow": None,
        }
        weather2 = WeatherData.from_dict(raw_partial)
        assert weather2.now is not None
        assert weather2.now.temperature == 19.5
        assert weather2.now.condition is None
        assert weather2.tomorrow is None


class TestClientWeather:
    def test_get_weather(self, monkeypatch):
        client = SmaClient(username="user", password="pass", component_id="17478443")
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "now": {
                "time": "2026-09-15T12:00:00Z",
                "iconId": 2,
                "temperature": 24,
            },
            "tomorrow": {
                "date": "2026-09-15T22:00:00Z",
                "iconId": 0,
                "minTemperature": 13,
                "maxTemperature": 18,
            },
            "city": "Tielt",
        }

        called_args = []

        def fake_get(path, **kwargs):
            called_args.append((path, kwargs))
            return mock_resp

        monkeypatch.setattr(client, "_get", fake_get)

        weather = client.get_weather()
        assert weather.city == "Tielt"
        assert weather.now.temperature == 24
        assert weather.tomorrow.max_temperature == 18

        assert len(called_args) == 1
        path, kwargs = called_args[0]
        assert path == "/components/17478443/forecast/weather"
        assert "startTodayUtc" in kwargs.get("params", {})

    def test_get_weather_explicit_params(self, monkeypatch):
        client = SmaClient(username="user", password="pass", component_id="default_id")
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"city": "Berlin"}

        called_args = []

        def fake_get(path, **kwargs):
            called_args.append((path, kwargs))
            return mock_resp

        monkeypatch.setattr(client, "_get", fake_get)

        weather = client.get_weather(
            component_id="custom_id",
            start_today_utc="2026-09-14T22:00:00.000Z",
        )
        assert weather.city == "Berlin"
        path, kwargs = called_args[0]
        assert path == "/components/custom_id/forecast/weather"
        assert kwargs["params"]["startTodayUtc"] == "2026-09-14T22:00:00.000Z"

    def test_get_weather_discovers_plant_if_needed(self, monkeypatch):
        client = SmaClient(username="user", password="pass")

        def fake_discover():
            client.component_id = "discovered_123"
            return "discovered_123"

        monkeypatch.setattr(client, "discover_plant", fake_discover)

        mock_resp = MagicMock()
        mock_resp.json.return_value = {"city": "Ghent"}
        called = []

        def fake_get(path, **kwargs):
            called.append(path)
            return mock_resp

        monkeypatch.setattr(client, "_get", fake_get)


        weather = client.get_weather()
        assert weather.city == "Ghent"
        assert client.component_id == "discovered_123"
        assert called[0] == "/components/discovered_123/forecast/weather"

