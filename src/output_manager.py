import os
from pathlib import Path
import simplekml
from datetime import datetime

class OutputManager:
    def __init__(self, settings):
        self.settings = settings
        self.output_dir = Path(settings.OUTPUT_DIR)
        self._ensure_output_dirs()
    
    def _ensure_output_dirs(self):
        for dir_name in ['pois', 'streets', 'districts']:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    def save_kml(self, kml_object, category: str, name: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.kml"
        output_path = self.output_dir / category / filename
        kml_object.save(str(output_path))
        return output_path 