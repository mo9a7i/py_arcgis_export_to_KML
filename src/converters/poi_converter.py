from collections import defaultdict
import simplekml

class POIConverter:
    def __init__(self, output_manager):
        self.output_manager = output_manager
    
    def convert(self, data):
        kml = simplekml.Kml()
        grouped_data = self._group_data(data)
        
        for category, pois in grouped_data.items():
            folder = kml.newfolder(name=category)
            self._add_pois_to_folder(folder, pois)
            
        return self.output_manager.save_kml(kml, 'pois', 'filtered_pois')
    
    def _group_data(self, data):
        grouped = defaultdict(list)
        for obj in data:
            category = obj.get("slugCategoryPOI", "Uncategorized")
            grouped[category].append(obj)
        return grouped 