# Export ArcGIS Online Webmap to GeoJSON

this script will help create KML from ArcGIS Online Webmap data

## Preparation

if you have a viewer link that has id like this

https://www.arcgis.com/apps/Viewer/index.html?appid=f593b8c6f3404ccfb0c507256ae295a6

add it to this link
https://www.arcgis.com/sharing/rest/content/items/f593b8c6f3404ccfb0c507256ae295a6/data?f=json

you will get webmap id in the response, add it to this
`https://www.arcgis.com/sharing/rest/content/items/6ee6a02b3cb3436982bd3b9a64dcc295/data?f=json`


https://www.arcgis.com/apps/Viewer/index.html?appid=f593b8c6f3404ccfb0c507256ae295a6


https://map.visitsaudi.com/api/pointsOfInterest?cities=RUH&regions=RUH&locale=en&type=city,experiences&categories=

## Installation
```bash
pnpm install
```

## Configuration
Create a `.env` file with:
```bash
VISIT_SAUDI_API=https://map.visitsaudi.com/api/pointsOfInterest
ARCGIS_API_BASE=https://www.arcgis.com/sharing/rest/content/items
```

## Usage
```bash
python src/main.py
```

## Output Structure
```
output/
├── pois/
├── streets/
└── districts/
```