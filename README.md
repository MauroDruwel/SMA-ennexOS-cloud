# SMA ennexOS Cloud

Python library for interacting with the SMA ennexOS / Sunny Portal API.

Uses PKCE OAuth2 to authenticate and provides typed access to PV plant data
(current power, daily energy, plant info). No browser required.

## Installation

```bash
pip install sma_ennexos_cloud
```

## Usage

```python
from sma_ennexos_cloud import SmaClient

client = SmaClient(username="your@email.com", password="your-password")
client.login()

plant_name = client.get_plant_name()
power = client.get_current_power()
energy = client.get_daily_energy()

print(f"Plant: {plant_name}")
print(f"Power: {power.value} W")
print(f"Daily energy: {energy.wh} Wh")
client.close()
```

## API

| Method | Returns | Description |
|--------|---------|-------------|
| `login()` | — | PKCE OAuth2 login |
| `get_current_power()` | `PowerData` | Live PV power in watts |
| `get_daily_energy()` | `EnergyData` | Today's total energy in Wh |
| `get_plant_name()` | `str` | Name of your PV plant |
| `close()` | — | Close HTTP session |

## Development

```bash
pip install -e ".[dev]"
pytest
```
