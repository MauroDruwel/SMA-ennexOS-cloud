from sma_ennexos.models import EnergyData, PlantInfo, PowerData


class TestPowerData:
    def test_defaults(self):
        p = PowerData()
        assert p.value is None
        assert p.timestamp == ""

    def test_to_dict(self):
        p = PowerData(value=123.4, timestamp="2026-07-30T12:00:00Z")
        d = p.to_dict()
        assert d["value"] == 123.4
        assert d["timestamp"] == "2026-07-30T12:00:00Z"


class TestEnergyData:
    def test_defaults(self):
        e = EnergyData()
        assert e.wh == 0
        assert e.timestamp == ""

    def test_to_dict(self):
        e = EnergyData(wh=5000, timestamp="2026-07-30T12:00:00Z")
        d = e.to_dict()
        assert d["wh"] == 5000


class TestPlantInfo:
    def test_to_dict(self):
        p = PlantInfo(component_id="123", name="My Plant")
        d = p.to_dict()
        assert d["component_id"] == "123"
        assert d["name"] == "My Plant"
