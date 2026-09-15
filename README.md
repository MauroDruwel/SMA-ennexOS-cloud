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

### Checking Live Data Status (Public Statuspage)

You can check whether SMA ennexOS Live Data is operational or under maintenance:

```python
from sma_ennexos_cloud import get_live_data_status

status = get_live_data_status()
print(status)  # "operational" or "under_maintenance"
```

Or via `SmaClient`:

```python
client = SmaClient(username="...", password="...", check_portal_status=True)
status = client.get_live_data_status()  # "operational" or "under_maintenance"
```

## API

| Method | Returns | Description |
|--------|---------|-------------|
| `login()` | — | PKCE OAuth2 login |
| `get_current_power()` | `PowerData` | Live PV power in watts |
| `get_daily_energy()` | `EnergyData` | Today's total energy in Wh |
| `get_plant_name()` | `str` | Name of your PV plant |
| `get_live_data_status(force_refresh=False)` | `str` | Live Data status (`operational`, `under_maintenance`, etc.) |
| `close()` | — | Close HTTP session |

## Standalone Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `get_live_data_status(session=None, timeout=10.0)` | `str` | Fetch ennexOS Live Data status without login |


## Development

```bash
pip install -e ".[dev]"
pytest
```

