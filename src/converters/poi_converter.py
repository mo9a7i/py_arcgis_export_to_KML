import json
import simplekml
from collections import defaultdict, Counter
from typing import Dict, Any, List, Tuple

class POIConverter:
    def __init__(self, output_manager):
        self.output_manager = output_manager
        self.en_source_url = "https://map.visitsaudi.com/api/pointsOfInterest?cities=RUH&regions=RUH&locale=en&type=city,experiences&categories="
        self.ar_source_url = "https://map.visitsaudi.com/api/pointsOfInterest?cities=RUH&regions=RUH&locale=ar&type=city,experiences&categories="

    async def fetch_pois(self, data_manager) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Fetch POI data from Visit Saudi API in both English and Arabic"""
        en_data = await data_manager.fetch_url(self.en_source_url)
        ar_data = await data_manager.fetch_url(self.ar_source_url)
        return en_data, ar_data

    def _merge_pois(self, en_pois: List[Dict[str, Any]], ar_pois: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge English and Arabic POI data"""
        merged_pois = []
        
        # Create map of Arabic POIs using slugPOI
        ar_poi_map = {}
        for poi in ar_pois:
            if 'slugPOI' not in poi:
                print(f"Warning: Arabic POI missing slugPOI: {poi.get('name', 'NO_NAME')}")
            else:
                ar_poi_map[poi['slugPOI']] = poi
        
        if len(ar_poi_map) != len(ar_pois):
            print(f"\nTotal Arabic POIs skipped due to missing slugPOI: {len(ar_pois) - len(ar_poi_map)}")
        
        differences_count = 0
        different_ids = []

        for en_poi in en_pois:
            if 'slugPOI' not in en_poi:
                print(f"Warning: English POI missing slugPOI: {en_poi.get('name', 'NO_NAME')}")
                continue
                
            slug_poi = en_poi['slugPOI']
            ar_poi = ar_poi_map.get(slug_poi)
            
            if not ar_poi:
                print(f"Warning: No Arabic data found for POI {slug_poi}")
                merged_pois.append(en_poi)
                continue

            # Create merged POI starting with English data
            merged_poi = en_poi.copy()
            
            # Add Arabic name, description and address
            merged_poi['name_ar'] = ar_poi['name']
            merged_poi['description_ar'] = ar_poi['description']
            if ar_poi.get('address'):
                merged_poi['address_ar'] = ar_poi['address']

            # Handle IDs
            if 'id' in ar_poi:
                merged_poi['id_ar'] = ar_poi['id']

            # Handle coordinates if they differ
            if ar_poi.get('latitude') != en_poi.get('latitude'):
                merged_poi['latitude_ar'] = ar_poi.get('latitude')
            if ar_poi.get('longitude') != en_poi.get('longitude'):
                merged_poi['longitude_ar'] = ar_poi.get('longitude')

            # Handle website if it differs
            if ar_poi.get('website') != en_poi.get('website') and ar_poi.get('website'):
                merged_poi['website_ar'] = ar_poi['website']

            # Combine images if they differ
            if ar_poi.get('bannerImage') != en_poi.get('bannerImage'):
                merged_poi['bannerImage'] = list(set(en_poi.get('bannerImage', []) + ar_poi.get('bannerImage', [])))
            if ar_poi.get('e60Image') != en_poi.get('e60Image'):
                merged_poi['e60Image'] = list(set(en_poi.get('e60Image', []) + ar_poi.get('e60Image', [])))

            # Handle createdAt dates
            if 'createdAt' in ar_poi and 'createdAt' in en_poi:
                ar_date = ar_poi.get('createdAt')
                en_date = en_poi.get('createdAt')
                if ar_date and en_date:
                    merged_poi['createdAt'] = min(ar_date, en_date)
                else:
                    merged_poi['createdAt'] = ar_date or en_date

            # Check for differences in other fields (excluding handled fields)
            for key, en_value in en_poi.items():
                if key not in ['name', 'description', 'address', 'businessHours', 'id', 'createdAt',
                             'latitude', 'longitude', 'website', 'bannerImage', 'e60Image']:
                    ar_value = ar_poi.get(key)
                    if en_value != ar_value:
                        if differences_count == 0:
                            print("\nDifferences found between English and Arabic data:")
                        differences_count += 1
                        if slug_poi not in different_ids:
                            different_ids.append(slug_poi)
                        print(f"POI {slug_poi}: Field '{key}' differs:")
                        print(f"  EN: {en_value}")
                        print(f"  AR: {ar_value}")

            merged_pois.append(merged_poi)

        print(f"\nTotal POIs with differences (excluding name/description/address/businessHours): {differences_count}")
        if different_ids:
            print(f"IDs with differences: {', '.join(different_ids)}")

        return merged_pois

    def _sanitize_text(self, text: str) -> str:
        """Sanitize text for XML/KML output"""
        if not text:
            return ""
        # Replace problematic characters
        return (str(text)
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;')
                .strip())

    def convert(self, pois_tuple: Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]):
        en_pois, ar_pois = pois_tuple
        merged_pois = self._merge_pois(en_pois, ar_pois)
        
        kml = simplekml.Kml()
        
        # Group POIs by category
        grouped_pois = defaultdict(list)
        for poi in merged_pois:
            category = poi.get('slugCategoryPOI', 'Uncategorized')
            grouped_pois[category].append(poi)
        
        if not grouped_pois:
            print("No POIs to convert")
            return self.output_manager.save_kml(kml, 'pois', 'riyadh_city_pois_by_category')
            
        # Create folders for each category
        for category, category_pois in grouped_pois.items():
            folder = kml.newfolder(name=category)
            poi_count = 0
            skipped_count = 0
            
            for poi in category_pois:
                # Skip POIs without coordinates
                if not poi.get('latitude') or not poi.get('longitude'):
                    skipped_count += 1
                    continue
                
                # Create placemark
                pnt = folder.newpoint(name=poi['name'])
                pnt.coords = [(poi['longitude'], poi['latitude'])]
                
                # Build description
                description_parts = []
                if poi.get('description'):
                    description_parts.append(poi['description'])
                if poi.get('businessHours'):
                    description_parts.append(f"Hours: {poi['businessHours']}")
                if poi.get('website'):
                    description_parts.append(f"Website: {poi['website']}")
                    
                pnt.description = "\n\n".join(description_parts)
                
                # Create ExtendedData element
                extdata = pnt.extendeddata
                
                # Add regular fields
                fields = [
                    "slugGovernorate", "website", "website_ar",
                    "slugPOI", "slugCity", "poiType", "slugCategoryPOI",
                    "active", "external", "featured", "slugRegion", "businessHours",
                    "rating", "publishedAt", "createdAt", "lastUpdatedAt", "videos",
                    "name_ar", "description_ar", "address", "address_ar",
                    "latitude_ar", "longitude_ar"  # Add Arabic coordinates
                ]
                
                # Add IDs if they exist
                if 'id' in poi:
                    extdata.newdata(
                        name='id',
                        value=self._sanitize_text(str(poi['id']))
                    )
                if 'id_ar' in poi:
                    extdata.newdata(
                        name='id_ar',
                        value=self._sanitize_text(str(poi['id_ar']))
                    )
                
                for field in fields:
                    value = poi.get(field)
                    if value is not None:  # Include empty strings but exclude None
                        extdata.newdata(
                            name=field,
                            value=self._sanitize_text(str(value))
                        )
                
                # Add image arrays as JSON strings
                if poi.get('bannerImage'):
                    extdata.newdata(
                        name='bannerImages',
                        value=json.dumps(poi['bannerImage'])
                    )
                
                if poi.get('e60Image'):
                    extdata.newdata(
                        name='e60Images',
                        value=json.dumps(poi['e60Image'])
                    )
                
                poi_count += 1
            
            print(f"  Processed: {poi_count}")
            if skipped_count:
                print(f"  Skipped (no coordinates): {skipped_count}")

        return self.output_manager.save_kml(kml, 'pois', 'riyadh_city_pois_by_category') 