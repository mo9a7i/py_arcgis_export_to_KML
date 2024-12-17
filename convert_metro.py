import json
import simplekml
import pyproj

# Load the JSON file
with open("data.json", "r") as file:
    data = json.load(file)

# Initialize KML
kml = simplekml.Kml()

# Projection: Convert from EPSG:3857 (Web Mercator) to WGS84 (EPSG:4326)
transformer = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

# Process layers
for layer in data["operationalLayers"]:
    title = layer["title"]

    if "featureCollection" in layer and "layers" in layer["featureCollection"]:
        for feature_layer in layer["featureCollection"]["layers"]:
            features = feature_layer["featureSet"]["features"]
            geometry_type = feature_layer["featureSet"]["geometryType"]

            if geometry_type == "esriGeometryPoint":  # Handle Stations (Points)
                folder = kml.newfolder(name=f"{title} - Points")
                for feature in features:
                    x = feature["geometry"]["x"]
                    y = feature["geometry"]["y"]
                    lon, lat = transformer.transform(x, y)  # Convert coordinates
                    name = feature["attributes"].get("Name", "Unknown Station")

                    # Add to KML
                    pnt = folder.newpoint(name=name, coords=[(lon, lat)])
                    pnt.description = f"Station Name: {name}"

            elif geometry_type == "esriGeometryPolyline":  # Handle Metro Lines
                folder = kml.newfolder(name=f"{title} - Lines")
                for feature in features:
                    paths = feature["geometry"]["paths"]
                    name = feature["attributes"].get("Name", "Unknown Line")
                    description = f"Metro Line: {name}"

                    # Consolidate all paths into one LineString with multiple segments
                    multigeometry = folder.newmultigeometry(name=name)
                    multigeometry.description = description

                    for path in paths:
                        coords = [transformer.transform(x, y) for x, y in path]
                        line = multigeometry.newlinestring(coords=coords)
                        line.style.linestyle.width = 2.5  # Set line style
                        line.style.linestyle.color = simplekml.Color.red

# Save the KML file
kml.save("metro_lines_and_stations_2.kml")
print("KML file 'metro_lines_and_stations_2.kml' created successfully! 🚀")
