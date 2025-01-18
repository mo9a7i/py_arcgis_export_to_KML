# Export ArcGIS Online Webmap to GeoJSON

This script creates KML files from ArcGIS Online Webmap data, including Riyadh Metro lines and stations

## Features

- Metro lines with color coding
- Metro stations with names and coordinates
- POIs near metro stations
- Districts and streets data

## Data Sources

### Metro Data

The metro data is sourced from ArcGIS Online Webmap. To access the data:

1. Original viewer link:

   `https://www.arcgis.com/apps/Viewer/index.html?appid=f593b8c6f3404ccfb0c507256ae295a6`

2. API endpoint pattern:

   `https://www.arcgis.com/sharing/rest/content/items/{webmap_id}/data?f=json`

### Points of Interest (POIs)

POIs are fetched from Visit Saudi's API:

`https://map.visitsaudi.com/api/pointsOfInterest?cities=RUH&regions=RUH&locale={en|ar}&type=city,experiences&categories=`

### Districts Data

Districts information is sourced from a public GitHub repository:
`https://raw.githubusercontent.com/homaily/Saudi-Arabia-Regions-Cities-and-Districts/refs/heads/master/json/districts.json`

## Installation

```bash
pnpm install
```

## Configuration

Create a `.env` file with:

```bash
VISIT_SAUDI_API=https://map.visitsaudi.com/api/pointsOfInterest
ARCGIS_API_BASE=https://www.arcgis.com/sharing/rest/content/items
METRO_MAP_ID=6ee6a02b3cb3436982bd3b9a64dcc295
```

## Usage

```bash
# Convert all data
python -m src.main all

# Convert specific data
python -m src.main metro    # Only metro lines and stations
python -m src.main pois     # Only POIs
python -m src.main districts # Only districts
```

## Output Structure

```bash
output/
├── metro/
│   ├── lines.kml      # Metro lines with colors
│   └── stations.kml   # Metro stations with names
├── pois/
│   └── riyadh_city_pois_by_category.kml
└── districts/
    └── riyadh_city_districts.kml
```

## Metro Data Structure

The metro data contains:

- Lines (1-6) with unique colors
- Stations with codes (e.g. 1A1, 2B2, etc)
- Direction information for track segments

### Line Colors

- Line 1: Red
- Line 2: Blue
- Line 3: Orange
- Line 4: Yellow
- Line 5: Green
- Line 6: Purple

## API Notes

1. ArcGIS API:
   - Requires appid from viewer URL
   - Returns webmap configuration and layer data
   - Supports JSON format output

2. Visit Saudi API:
   - Supports multiple locales (en, ar)
   - Filters by city and region
   - Categories can be specified for POI filtering

3. Districts API:
   - Static JSON data
   - Includes boundaries, names in English and Arabic
   - Contains region and city identifiers

## Alternative Data Sources

### Alternative Metro Data Source

A static JSON file containing metro routes and stations data:

- Source: [Riyadh Metro JSON](https://raw.githubusercontent.com/aqar-app/Riyadh-Metro-Routes-and-Stations/refs/heads/main/riyadh_metro.json)
- Contains complete metro line routes and station locations
- No API key or authentication required
- Data includes:
  - Line geometries and colors
  - Station locations and codes
  - English and Arabic names
