import json
import simplekml
from collections import defaultdict, Counter
from typing import Dict, Any, List, Tuple

class POIConverter:
    def __init__(self, output_manager):
        self.output_manager = output_manager
        # Use the exact URL without any modifications
        self.source_url = "https://map.visitsaudi.com/api/pointsOfInterest?cities=RUH&regions=RUH&locale=en&type=city,experiences&categories="

    async def fetch_pois(self, data_manager) -> List[Dict[str, Any]]:
        """Fetch POI data from Visit Saudi API"""
        return await data_manager.fetch_url(self.source_url)

    def _analyze_pois(self, pois: List[Dict[str, Any]]) -> None:
        """Analyze POI data and print statistics"""
        print("\nAnalyzing POI data:")
        # print the first 1 poi
        print(f"First POI: {pois}")
        print(f"Data type: {type(pois)}")
        print("First item type:", type(pois[0]) if pois else None)
        print("First item:", pois[0] if pois else None)
        
        # Ensure we have a list of dictionaries
        if not all(isinstance(poi, dict) for poi in pois):
            print("Warning: Some POIs are not dictionaries")
            return
        
        # Count total POIs
        print(f"\nTotal POIs: {len(pois)}")
        
        # Count POIs by region
        regions = Counter(poi.get('slugRegion') for poi in pois if isinstance(poi, dict))
        print("\nPOIs by region:")
        for region, count in regions.items():
            print(f"  {region}: {count}")
        
        # Count POIs by category
        categories = Counter(poi.get('slugCategoryPOI', 'Uncategorized') for poi in pois if isinstance(poi, dict))
        print("\nPOIs by category:")
        for category, count in categories.items():
            print(f"  {category}: {count}")

    def _group_by_category(self, pois: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Group POIs by their category"""
        # First analyze the data
        self._analyze_pois(pois)
        
        grouped = defaultdict(list)
        
        # Filter for Riyadh POIs and group by category
        for poi in pois:
            if poi.get('slugRegion') == 'RUH':
                category = poi.get('slugCategoryPOI', 'Uncategorized')
                grouped[category].append(poi)
        
        print(f"\nGrouped {sum(len(pois) for pois in grouped.values())} Riyadh POIs into {len(grouped)} categories")
        return grouped

    def convert(self, pois: List[Dict[str, Any]]):
        kml = simplekml.Kml()
        
        # Group POIs by category
        grouped_pois = self._group_by_category(pois)
        
        if not grouped_pois:
            print("No POIs to convert")
            return self.output_manager.save_kml(kml, 'pois', 'riyadh_city_pois_by_category')
            
        # Create folders for each category
        for category, category_pois in grouped_pois.items():
            folder = kml.newfolder(name=category)
            print(f"\nProcessing {category}:")
            print(f"  POIs in category: {len(category_pois)}")
            
            poi_count = 0
            skipped_count = 0
            
            for poi in category_pois:
                # Skip POIs without coordinates
                if not poi.get('latitude') or not poi.get('longitude'):
                    skipped_count += 1
                    continue

                # Create placemark for each POI
                pnt = folder.newpoint(name=poi['name'])
                pnt.coords = [(float(poi['longitude']), float(poi['latitude']))]
                
                # Add description with available details
                description_parts = []
                if poi.get('description'):
                    description_parts.append(poi['description'])
                    
                pnt.description = "\n\n".join(description_parts)
                
                # Add extended data
                pnt.extendeddata.newdata(name="category", value=category)
                pnt.extendeddata.newdata(name="rating", value=str(poi.get('rating', 0)))
                pnt.extendeddata.newdata(name="id", value=poi.get('id', ''))
                pnt.extendeddata.newdata(name="slugPOI", value=poi.get('slugPOI', ''))
                pnt.extendeddata.newdata(name="businessHours", value=str(poi.get('businessHours', '')))
                pnt.extendeddata.newdata(name="poiType", value=str(poi.get('poiType', '')))
                pnt.extendeddata.newdata(name="website", value=str(poi.get('website', '')))
                
                poi_count += 1
            
            print(f"  Processed: {poi_count}")
            if skipped_count:
                print(f"  Skipped (no coordinates): {skipped_count}")

        return self.output_manager.save_kml(kml, 'pois', 'riyadh_city_pois_by_category') 