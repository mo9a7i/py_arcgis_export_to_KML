import json
import simplekml
from collections import defaultdict

# Load the JSON file
with open("data/RUH_POIs.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Filter and group by slugCategoryPOI
slugCity_target = "RUH"
grouped_data = defaultdict(list)

for obj in data:
    if obj.get("slugCity") == slugCity_target:
        category = obj.get("slugCategoryPOI", "Uncategorized")
        grouped_data[category].append(obj)

# Create the KML
kml = simplekml.Kml()

# Add folders for each category
for category, pois in grouped_data.items():
    folder = kml.newfolder(name=category)
    for poi in pois:
        name = poi.get("name", "Unnamed POI")
        latitude = poi.get("latitude")
        longitude = poi.get("longitude")
        description = f"ID: {poi.get('id')}, Type: {poi.get('poiType', 'N/A')}"
        
        # Add placemark
        placemark = folder.newpoint(name=name, coords=[(longitude, latitude)])
        placemark.description = description

# Save the KML
kml.save("output/filtered_pois_grouped_by_category.kml")
print("KML file created successfully!")
