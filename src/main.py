import asyncio
import argparse
from .config import Settings
from .data_source import DataSourceManager
from .output_manager import OutputManager
from .converters.district_converter import DistrictConverter
from .converters.poi_converter import POIConverter

async def convert_districts():
    settings = Settings()
    data_manager = DataSourceManager(settings)
    output_manager = OutputManager(settings)
    
    district_converter = DistrictConverter(output_manager)
    districts_data = await district_converter.fetch_districts(data_manager)
    district_output = district_converter.convert(districts_data)
    
    print(f"Districts KML saved to: {district_output}")

async def convert_pois():
    settings = Settings()
    data_manager = DataSourceManager(settings)
    output_manager = OutputManager(settings)
    
    poi_data = await data_manager.fetch_pois()
    poi_converter = POIConverter(output_manager)
    poi_output = poi_converter.convert(poi_data)
    
    print(f"POIs KML saved to: {poi_output}")

async def main():
    parser = argparse.ArgumentParser(description='Convert various data sources to KML')
    parser.add_argument('source', choices=['districts', 'pois', 'all'],
                      help='Specify which data source to convert (districts, pois, or all)')
    
    args = parser.parse_args()
    
    if args.source == 'districts':
        await convert_districts()
    elif args.source == 'pois':
        await convert_pois()
    elif args.source == 'all':
        await convert_districts()
        await convert_pois()

if __name__ == "__main__":
    asyncio.run(main()) 