import json
import simplekml
from typing import Dict, Any, List, Tuple

class DistrictConverter:
    def __init__(self, output_manager):
        self.output_manager = output_manager
        self.source_url = "https://raw.githubusercontent.com/homaily/Saudi-Arabia-Regions-Cities-and-Districts/refs/heads/master/json/districts.json"

    async def fetch_districts(self, data_manager):
        """Fetch districts data"""
        try:
            districts = await data_manager.fetch_districts()
            if not districts:
                print("No districts data received")
                return []
            return districts
        except Exception as e:
            print(f"Error fetching districts: {e}")
            return []

    def _format_coordinates(self, boundaries: List[List[List[float]]]) -> List[Tuple[float, float, float]]:
        """Convert boundary coordinates to KML format
        
        Args:
            boundaries: List of coordinate arrays
            
        Returns:
            Flattened list of (longitude, latitude, altitude) tuples
        """
        # Flatten the coordinates and convert to (lon, lat, alt) tuples
        return [(coord[1], coord[0], 0.0) for ring in boundaries for coord in ring]

    def convert(self, data):
        """Convert districts to KML without styling"""
        if not data:
            print("No district data to convert")
            return None
            
        kml = simplekml.Kml()
        riyadh_districts = [d for d in data if d["region_id"] == 1 and d["city_id"] == 3]
        folder = kml.newfolder(name="Riyadh City Districts")
        
        for district in riyadh_districts:
            boundaries = district["boundaries"]
            
            # Create polygon without styling
            pol = folder.newpolygon(name=district["name_en"])
            coordinates = self._format_coordinates(boundaries)
            pol.outerboundaryis = coordinates
            
            pol.description = f"Arabic Name: {district['name_ar']} | City ID: {district['city_id']} | Region ID: {district['region_id']}"

        return self.output_manager.save_kml(kml, 'districts', 'riyadh_city_districts') 