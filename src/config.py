from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # API endpoints
    VISIT_SAUDI_API: str = Field(
        default="https://map.visitsaudi.com/api/pointsOfInterest",
        description="Visit Saudi API endpoint"
    )
    ARCGIS_API_BASE: str = Field(
        default="https://www.arcgis.com/sharing/rest/content/items",
        description="ArcGIS API base URL"
    )
    
    # Output configuration
    OUTPUT_DIR: str = Field(
        default="output",
        description="Directory for output files"
    )
    
    # Data source configurations
    DEFAULT_CITY: str = Field(
        default="RUH",
        description="Default city code"
    )
    COORDINATE_SYSTEM: dict = Field(
        default={
            "source": "EPSG:3857",
            "target": "EPSG:4326"
        },
        description="Coordinate system configuration"
    )
    
    class Config:
        env_file = ".env" 