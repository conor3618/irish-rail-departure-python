# Irish Rail Live Departures

A Python script that queries the [Irish Rail Real-time API](http://api.irishrail.ie/realtime/) to display live departure information for any Irish Rail station. Accepts either a station name or station code as input.

## Features
- Search by station name or station code
- Displays destination, direction, and minutes until departure for all upcoming trains
- Results sorted by soonest departure first
- Includes a script to generate a full station directory

## Usage
Run the main script and follow the prompts:
```bash
python irish_rail_departures.py
```

Example output:
```
Search by:
  1 — Station code
  2 — Station name

> 2
Enter station name: Dalkey

Live departures for: Dalkey

Destination                    Direction       Due (mins)
-------------------------------------------------------
Bray                           Southbound      11 mins
Malahide                       Northbound      17 mins
Howth                          Northbound      24 mins
Greystones                     Southbound      29 mins
Bray                           Southbound      37 mins
Malahide                       Northbound      39 mins
Howth                          Northbound      54 mins
Bray                           Southbound      58 mins
Malahide                       Northbound      69 mins
Greystones                     Southbound      71 mins
Howth                          Northbound      84 mins
Bray                           Southbound      86 mins
```



## stations.json
`stations.json` contains a full list of all Irish Rail stations and their corresponding station codes. Use this file to look up the correct code before running the script.

To regenerate `stations.json` with the latest station list, run:
```bash
python generate_stations.py
```

## How It Works
1. User selects whether to search by station name or station code
2. Script calls the appropriate Irish Rail API endpoint
3. XML response is parsed and filtered for destination, direction, and due time
4. Results are sorted by soonest departure and printed to the terminal

## Data Source
All live departure data is sourced from the [Irish Rail Real-time API](http://api.irishrail.ie/realtime/).
