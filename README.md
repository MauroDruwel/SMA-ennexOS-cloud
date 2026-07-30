# SMA ennexOS

Python library for interacting with the SMA ennexOS / Sunny Portal API.

Uses PKCE OAuth2 to authenticate and provides typed access to PV plant data
(current power, daily energy, plant info).

## Installation

```bash
pip install sma_ennexos
```

## Usage

```python
from sma_ennexos import SmaClient

client = SmaClient(username="your@email.com", password="your-password")
client.login()

plant_name = client.get_plant_name()
power = client.get_current_power()
energy = client.get_daily_energy()

print(f"Plant: {plant_name}")
print(f"Power: {power.value} W")
print(f"Daily energy: {energy.wh} Wh")
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
