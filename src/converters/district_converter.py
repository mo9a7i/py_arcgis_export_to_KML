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

    def _format_coordinates(self, boundaries: List[List[float]]) -> List[Tuple[float, float]]:
        """Convert boundary coordinates to KML format
        
        Args:
            boundaries: List of coordinate pairs [latitude, longitude]
            
        Returns:
            List of (longitude, latitude) tuples as required by KML
        """
        return [(coord[0], coord[1]) for coord in boundaries]

    def convert(self, data):
        """Convert districts to KML"""
        if not data:
            print("No district data to convert")
            return None
            
        kml = simplekml.Kml()
        riyadh_districts = [d for d in data if d["region_id"] == 1 and d["city_id"] == 3]
        folder = kml.newfolder(name="Riyadh City Districts")
        
        for district in riyadh_districts:
            boundaries = district["boundaries"]
            
            # Create polygon
            pol = folder.newpolygon(name=district["name_en"])
            coordinates = self._format_coordinates(boundaries)
            pol.outerboundaryis = coordinates
            
            pol.description = f"Arabic Name: {district['name_ar']} | City ID: {district['city_id']} | Region ID: {district['region_id']}"
            
            # Style the polygon
            pol.style.polystyle.color = 'CC0000FF'
            pol.style.polystyle.outline = 1
            pol.style.linestyle.color = 'FF0000FF'
            pol.style.linestyle.width = 2

        return self.output_manager.save_kml(kml, 'districts', 'riyadh_city_districts') 