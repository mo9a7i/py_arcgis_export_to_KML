# Export ArcGIS Online Webmap to GeoJSON

This script creates KML files from ArcGIS Online Webmap data, including Riyadh Metro lines and stations

## Features
- Metro lines with color coding
- Metro stations with names and coordinates
- POIs near metro stations
- Districts and streets data

if you have a viewer link that has id like this

https://www.arcgis.com/apps/Viewer/index.html?appid=f593b8c6f3404ccfb0c507256ae295a6

add it to this link
https://www.arcgis.com/sharing/rest/content/items/f593b8c6f3404ccfb0c507256ae295a6/data?f=json

you will get webmap id in the response, add it to this
`https://www.arcgis.com/sharing/rest/content/items/6ee6a02b3cb3436982bd3b9a64dcc295/data?f=json`


https://www.arcgis.com/apps/Viewer/index.html?appid=f593b8c6f3404ccfb0c507256ae295a6


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
python src/main.py all

# Convert specific data
python src/main.py metro    # Only metro lines and stations
python src/main.py pois     # Only POIs
python src/main.py districts # Only districts
```

## Output Structure
```
output/
├── metro/
│   ├── lines.kml      # Metro lines with colors
│   └── stations.kml   # Metro stations with names
├── pois/
│   └── riyadh_city_pois_by_category.kml
├── streets/
└── districts/
```

## Metro Data Structure
The metro data contains:
- Lines (1-6) with unique colors
- Stations with codes (e.g. 1A1, 2B2, etc)
- Direction information for track segments

### Line Colors:
- Line 1: Red
- Line 2: Blue
- Line 3: Orange
- Line 4: Yellow
- Line 5: Green
- Line 6: Purple