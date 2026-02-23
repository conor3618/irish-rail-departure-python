"""
Irish Rail Live Departures
---------------------------
Queries the Irish Rail Real-time API to retrieve live departure information
for a specified station. Accepts either a station name or station code.
Displays destination, direction, and minutes until departure for all
upcoming trains.

API source: http://api.irishrail.ie/realtime/realtime.asmx
No API key required.
"""

import requests
import xml.etree.ElementTree as ET

# Base URL and XML namespace for the Irish Rail API
BASE_URL = "http://api.irishrail.ie/realtime/realtime.asmx"
NS       = "http://api.irishrail.ie/realtime/"


def _get(el, tag):
    """Extract and return text content from an XML element by tag name."""
    node = el.find(f"{{{NS}}}{tag}")
    return node.text.strip() if node is not None and node.text else "—"


def _parse_departures(xml_content: bytes) -> list[dict]:
    """
    Parse raw XML response from the Irish Rail API into a list of departures.

    Args:
        xml_content (bytes): Raw XML response content from the API.

    Returns:
        list[dict]: List of departures sorted by minutes until departure,
                    each containing Destination, Direction, and Due (mins).
    """
    root   = ET.fromstring(xml_content)
    trains = root.findall(f"{{{NS}}}objStationData")

    departures = []
    for t in trains:
        due_str   = _get(t, "Duein")
        direction = _get(t, "Direction")

        # Convert due time to integer, default to 0 if not numeric
        due = int(due_str) if due_str.lstrip("-").isdigit() else 0

        # Format direction as a readable label
        dir_label = "Northbound" if "North" in direction else "Southbound"

        departures.append({
            "Destination": _get(t, "Destination"),
            "Direction":   dir_label,
            "Due (mins)":  due,
        })

    # Sort by soonest departure first
    departures.sort(key=lambda x: x["Due (mins)"])
    return departures


def print_departures_list(station_input: str, departures: list[dict]):
    """
    Print a formatted departures table for a given station.

    Args:
        station_input (str): The station name or code entered by the user.
        departures (list[dict]): Parsed list of departure dictionaries.
    """
    print(f"\nLive departures for: {station_input}\n")
    print(f"{'Destination':<30} {'Direction':<15} {'Due (mins)'}")
    print("-" * 55)

    if not departures:
        print("No departures found.")
        return

    for dep in departures:
        print(f"{dep['Destination']:<30} {dep['Direction']:<15} {dep['Due (mins)']} mins")


# --- Main Entry Point ---

if __name__ == "__main__":
    print("Search by:")
    print("  1 — Station code")
    print("  2 — Station name")

    choice = input("\n> ").strip()

    if choice == "1":
        station = input("Enter station code: ").strip()
        url     = f"{BASE_URL}/getStationDataByCodeXML"
        params  = {"StationCode": station}
    elif choice == "2":
        station = input("Enter station name: ").strip()
        url     = f"{BASE_URL}/getStationDataByNameXML"
        params  = {"StationDesc": station}
    else:
        print("Invalid choice.")
        exit()

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        departures = _parse_departures(resp.content)
        print_departures_list(station, departures)
    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.ConnectionError:
        print("Connection error — check your internet connection.")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
