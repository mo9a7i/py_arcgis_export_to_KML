import json
import simplekml

# Load GeoJSON file
with open("districts.json", "r") as file:
    geojson_data = json.load(file)

# Initialize KML
kml = simplekml.Kml()

# Filter features for city_id = 3
city_id_target = 3

for feature in geojson_data["features"]:
    # Check if the feature has the property city_id = 3
    if feature["properties"].get("city_id") == city_id_target:
        geometry = feature["geometry"]
        properties = feature["properties"]

        # Handle MultiPolygon and Polygon geometry
        if geometry["type"] == "Polygon":
            polygons = [geometry["coordinates"]]
        elif geometry["type"] == "MultiPolygon":
            polygons = geometry["coordinates"]
        else:
            continue  # Skip non-polygon features

        # Add to KML
        for polygon_coords in polygons:
            # Flatten the coordinates
            kml_coords = [(lon, lat) for ring in polygon_coords for lon, lat in ring]

            # Create KML Polygon
            pol = kml.newpolygon(
                name=properties.get("name_en", "Unknown District"),  # Default name
                outerboundaryis=kml_coords,
            )
            pol.description = f"City ID: {city_id_target}, District (EN): {properties.get('name_en', 'N/A')}, District (AR): {properties.get('name_ar', 'N/A')}"
            pol.style.polystyle.color = simplekml.Color.changealpha("80", simplekml.Color.green)

# Save KML
kml.save("city_3_districts.kml")
print("KML file 'city_3_districts.kml' created successfully! 🏙️")
