import json
import simplekml
from typing import Dict, Any, List, Tuple

class DistrictConverter:
    def __init__(self, output_manager):
        self.output_manager = output_manager
        self.source_url = "https://raw.githubusercontent.com/homaily/Saudi-Arabia-Regions-Cities-and-Districts/refs/heads/master/json/districts.json"

    async def fetch_districts(self, data_manager) -> Dict[str, Any]:
        """Fetch districts data from GitHub"""
        return await data_manager.fetch_url(self.source_url)

    def _format_coordinates(self, boundaries: List[List[float]]) -> List[Tuple[float, float]]:
        """Convert boundary coordinates to KML format"""
        # Convert [[lon1, lat1], [lon2, lat2], ...] to [(lon1, lat1), (lon2, lat2), ...]
        return [(coord[0], coord[1]) for coord in boundaries]

    def convert(self, data):
        kml = simplekml.Kml()
        # Filter for both Riyadh region (region_id=1) AND Riyadh city (city_id=3)
        riyadh_districts = [d for d in data if d["region_id"] == 1 and d["city_id"] == 3]
        
        folder = kml.newfolder(name="Riyadh City Districts")
        
        for district in riyadh_districts:
            pol = folder.newpolygon(name=district["name_en"])
            
            # Format coordinates properly for KML
            coordinates = self._format_coordinates(district["boundaries"][0])
            pol.outerboundaryis = coordinates
            
            # Enhanced description in a single line
            pol.description = f"Arabic Name: {district['name_ar']} | City ID: {district['city_id']} | Region ID: {district['region_id']}"
            
            # Style the polygon
            pol.style.polystyle.color = 'CC0000FF'  # Red with some transparency
            pol.style.polystyle.outline = 1
            pol.style.linestyle.color = 'FF0000FF'  # Solid red outline
            pol.style.linestyle.width = 2

        return self.output_manager.save_kml(kml, 'districts', 'riyadh_city_districts') 