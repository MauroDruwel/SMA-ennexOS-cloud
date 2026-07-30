"""Example usage of the SMA ennexOS library."""
import json
import sys
import time

from sma_ennexos_cloud import SmaClient


def main():
    username = input("SMA ID / Sunny Portal email: ").strip()
    password = input("SMA ID password: ").strip()

    client = SmaClient(username=username, password=password)
    print("Logging in ...", file=sys.stderr)
    client.login()

    plant_name = client.get_plant_name()
    print(f"Plant: {plant_name}", file=sys.stderr)

    try:
        while True:
            power = client.get_current_power()
            energy = client.get_daily_energy()

            output = {
                "watts": power.value,
                "daily_wh": energy.wh,
                "plant": plant_name,
                "ts": power.timestamp,
            }
            print(json.dumps(output))
            sys.stdout.flush()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()


if __name__ == "__main__":
    main()
