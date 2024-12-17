import json
import simplekml
import pyproj

# Load JSON file
with open("riyadh_streets.json", "r") as file:
    data = json.load(file)

# Initialize KML
kml = simplekml.Kml()

# Projection: Convert from EPSG:3857 (Web Mercator) to WGS84 (EPSG:4326)
transformer = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

# Function to generate dummy line coordinates for the layers
def create_dummy_lines(layer_extent):
    """
    Create dummy line geometry based on layer extent.
    :param layer_extent: Bounding box of the layer.
    :return: List of transformed line coordinates.
    """
    xmin, ymin, xmax, ymax = (
        layer_extent["xmin"],
        layer_extent["ymin"],
        layer_extent["xmax"],
        layer_extent["ymax"],
    )
    # Create a simple rectangular polyline using the extent
    coords = [
        (xmin, ymin),
        (xmax, ymin),
        (xmax, ymax),
        (xmin, ymax),
        (xmin, ymin),
    ]
    return [transformer.transform(x, y) for x, y in coords]


# Process Layers
for layer in data["layers"]:
    if layer["geometryType"] == "esriGeometryPolyline":
        name = layer["name"]
        visibility = "Visible" if layer["defaultVisibility"] else "Hidden"

        # Add folder for polyline layer
        folder = kml.newfolder(name=name)
        folder.description = f"Layer ID: {layer['id']}, Visibility: {visibility}"

        # Generate a dummy line for the extent
        line_coords = create_dummy_lines(data["fullExtent"])
        linestring = folder.newlinestring(name=name, coords=line_coords)
        linestring.style.linestyle.color = simplekml.Color.blue
        linestring.style.linestyle.width = 2
        linestring.description = f"Auto-generated polyline for layer '{name}'"

# Save KML
kml.save("converted_street_layers.kml")
print("KML file 'converted_street_layers.kml' created successfully! 🚀")
