# Changelog

## 0.2.5 (2026-11-12)

- Fix daily energy query day boundary for winter time (CET) and other timezones by computing local midnight dynamically using `zoneinfo` instead of a hardcoded `22:00:00Z` offset
- Support configurable plant timezone in `SmaClient` and `get_daily_energy(plant_timezone=...)`
- Auto-detect plant timezone from `/plants/{component_id}`
- Safely extract the latest non-null value (`values[-1]`) when multiple daily buckets are returned by SMA

## 0.2.4 (2026-10-18)

- Added weather forecast models, constants, and client endpoint (`get_weather`)

- Added Sunny Portal statuspage monitoring (`get_portal_status` and `PortalStatus` model)
- Added `check_portal_status` option to `SmaClient`
- Tracks ennexOS Live Data component status (`operational`, `under_maintenance`, etc.)

## 0.1.0 (2026-07-30)


- Initial release
- PKCE OAuth2 authentication
- Current power (gauge) and daily energy (measurements) endpoints
- Plant discovery and naming
