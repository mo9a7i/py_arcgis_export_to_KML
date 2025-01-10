import asyncio
import argparse
from .config import Settings
from .data_source import DataSourceManager
from .output_manager import OutputManager
from .converters.district_converter import DistrictConverter
from .converters.poi_converter import POIConverter
from .data_source import ArcGISResolver
from .converters.metro_converter import MetroConverter
import json

async def convert_districts():
    settings = Settings()
    data_manager = DataSourceManager(settings)
    output_manager = OutputManager(settings)
    
    district_converter = DistrictConverter(output_manager)
    districts_data = await district_converter.fetch_districts(data_manager)
    
    if districts_data:
        district_output = district_converter.convert(districts_data)
        if district_output:
            print(f"Districts KML saved to: {district_output}")
    else:
        print("Failed to fetch district data")

async def convert_pois():
    """Convert POIs to KML"""
    data_manager = DataSourceManager(Settings())
    output_manager = OutputManager(Settings())
    poi_converter = POIConverter(output_manager)
    
    poi_data = await poi_converter.fetch_pois(data_manager)
    poi_output = poi_converter.convert(poi_data)
    
    print(f"\nPOI KML file saved: {poi_output}")

async def convert_metro():
    """Convert Metro data to KML"""
    resolver = ArcGISResolver()
    output_manager = OutputManager(Settings())
    metro_converter = MetroConverter(output_manager)
    
    # Get metro data
    data = await resolver.get_webmap_data("https://www.arcgis.com/apps/Viewer/index.html?appid=f593b8c6f3404ccfb0c507256ae295a6")
    
    if data:
        # Convert lines and stations separately
        lines_output = metro_converter.convert_lines(data)
        stations_output = metro_converter.convert_stations(data)
        
        print(f"\nMetro lines KML saved to: {lines_output}")
        print(f"Metro stations KML saved to: {stations_output}")
    else:
        print("Failed to fetch metro data")

async def main():
    parser = argparse.ArgumentParser(description='Convert various data sources to KML')
    parser.add_argument('source', choices=['districts', 'pois', 'metro', 'all'],
                      help='Specify which data source to convert (districts, pois, metro, or all)')
    
    args = parser.parse_args()
    
    if args.source == 'metro':
        await convert_metro()
    elif args.source == 'districts':
        await convert_districts()
    elif args.source == 'pois':
        await convert_pois()
    elif args.source == 'all':
        await convert_districts()
        await convert_pois()
        await convert_metro()

if __name__ == "__main__":
    asyncio.run(main()) 