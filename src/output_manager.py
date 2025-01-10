import os
import shutil
from datetime import datetime
from pathlib import Path

class OutputManager:
    def __init__(self, settings=None):
        self.base_dir = Path('output')
        self.settings = settings

    def save_kml(self, kml_object, subdir, filename):
        """
        Save KML file with versioning:
        1. If current file exists, rename it with timestamp
        2. Save new file without timestamp
        3. Add updated_at property to KML
        """
        # Create output directory if it doesn't exist
        output_dir = self.base_dir / subdir
        output_dir.mkdir(parents=True, exist_ok=True)

        # Current file path (without timestamp)
        current_path = output_dir / f'{filename}.kml'
        
        # If file exists, rename it with timestamp
        if current_path.exists():
            timestamp = datetime.fromtimestamp(current_path.stat().st_mtime).strftime('%Y%m%d_%H%M%S')
            archived_path = output_dir / f'{filename}_{timestamp}.kml'
            shutil.move(str(current_path), str(archived_path))
            print(f"Archived previous version to: {archived_path}")

        # Add updated_at to KML metadata
        if hasattr(kml_object, 'document'):
            timestamp = datetime.now().isoformat()
            extdata = kml_object.document.extendeddata
            extdata.newdata(name='updated_at', value=timestamp)

        # Save new file without timestamp
        kml_object.save(str(current_path))
        return current_path 