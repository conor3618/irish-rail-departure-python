"""
Irish Rail Station Directory Generator
----------------------------------------
Fetches the complete list of Irish Rail stations and their codes
from the Irish Rail Real-time API and saves them to stations.json.

Run this script to regenerate stations.json if the station list changes.

API source: http://api.irishrail.ie/realtime/realtime.asmx
No API key required.
"""

import requests
import json
import xml.etree.ElementTree as ET

# Base API endpoint and XML namespace
BASE_URL = "http://api.irishrail.ie/realtime/realtime.asmx"
NS       = "http://api.irishrail.ie/realtime/"


def get_all_stations() -> dict:
    """
    Fetch all stations from the Irish Rail API.

    Calls the getAllStationsXML endpoint and parses the XML response
    into a dictionary mapping station names to their station codes.

    Returns:
        dict: A dictionary in the format { "Station Name": "SCODE" }
    """
    url  = f"{BASE_URL}/getAllStationsXML"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    # Parse the XML response
    root     = ET.fromstring(resp.content)
    stations = root.findall(f"{{{NS}}}objStation")

    # Build a name → code lookup dictionary
    return {
        s.find(f"{{{NS}}}StationDesc").text.strip(): s.find(f"{{{NS}}}StationCode").text.strip()
        for s in stations
        if s.find(f"{{{NS}}}StationDesc") is not None
        and s.find(f"{{{NS}}}StationCode") is not None
    }


# --- Main Execution ---

station_directory = get_all_stations()
print(f"Loaded {len(station_directory)} stations.")

# Save to stations.json for use with irish_rail_departures.py
with open('stations.json', 'w', encoding='utf-8') as f:
    json.dump(station_directory, f, indent=2, ensure_ascii=False)
print("Station data saved to stations.json")
