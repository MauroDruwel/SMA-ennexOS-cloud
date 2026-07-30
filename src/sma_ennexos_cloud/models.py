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
