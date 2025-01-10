import simplekml
import pyproj
from typing import Dict, Any, Optional

class MetroConverter:
    def __init__(self, output_manager):
        self.output_manager = output_manager
        self.transformer = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
        # Define the specific layer IDs we want
        self.METRO_LINES_ID = "metrolines_110"
        self.STATIONS_ID = "stations_4748"

    def convert_lines(self, data: Dict[str, Any]) -> Optional[str]:
        """Convert metro lines to KML - grouped by line number"""
        kml = simplekml.Kml()
        line_groups = {}
        
        # Find the metro lines layer
        for layer in data.get("operationalLayers", []):
            if layer.get("id") != self.METRO_LINES_ID:
                continue
                
            for feature_layer in layer["featureCollection"].get("layers", []):
                if feature_layer["featureSet"]["geometryType"] != "esriGeometryPolyline":
                    continue
                
                for feature in feature_layer["featureSet"]["features"]:
                    name = feature["attributes"].get("Name", "Unknown Line")
                    if name not in line_groups:
                        line_groups[name] = []
                    line_groups[name].extend(feature["geometry"]["paths"])
        
        folder = kml.newfolder(name="Metro Lines")
        
        for line_name, paths in line_groups.items():
            multigeometry = folder.newmultigeometry(name=line_name)
            multigeometry.description = f"Metro Line: {line_name}"
            
            for path in paths:
                coords = [self.transformer.transform(x, y) for x, y in path]
                multigeometry.newlinestring(coords=coords)
        
        return self.output_manager.save_kml(kml, 'metro', 'riyadh_metro_lines')

    def convert_stations(self, data: Dict[str, Any]) -> Optional[str]:
        """Convert metro stations to KML"""
        kml = simplekml.Kml()
        folder = kml.newfolder(name="Metro Stations")
        
        # Find the stations layer
        for layer in data.get("operationalLayers", []):
            if layer.get("id") != self.STATIONS_ID:
                continue
                
            for feature_layer in layer["featureCollection"].get("layers", []):
                if feature_layer["featureSet"]["geometryType"] != "esriGeometryPoint":
                    continue
                
                for feature in feature_layer["featureSet"]["features"]:
                    x = feature["geometry"]["x"]
                    y = feature["geometry"]["y"]
                    lon, lat = self.transformer.transform(x, y)
                    name = feature["attributes"].get("Name", "Unknown Station")
                    
                    pnt = folder.newpoint()
                    pnt.name = name
                    pnt.coords = [(lon, lat)]
                    if feature["attributes"].get("Description"):
                        pnt.description = feature["attributes"]["Description"]
        
        return self.output_manager.save_kml(kml, 'metro', 'riyadh_metro_stations') 