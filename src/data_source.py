import aiohttp
import asyncio
import json
from typing import Dict, Any

class DataSourceManager:
    def __init__(self, settings):
        self.settings = settings
        
    async def fetch_pois(self, city: str = None) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            params = {
                "cities": city or self.settings.DEFAULT_CITY,
                "locale": "en",
                "type": "city,experiences",
                "regions": "RUH",
                "categories": ""
            }
            async with session.get(self.settings.VISIT_SAUDI_API, params=params) as response:
                return await response.json()
                
    async def fetch_arcgis_data(self, item_id: str) -> Dict[str, Any]:
        url = f"{self.settings.ARCGIS_API_BASE}/{item_id}/data"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"f": "json"}) as response:
                return await response.json()

    async def fetch_url(self, url: str) -> Dict[str, Any]:
        """Fetch JSON data from any URL"""
        async with aiohttp.ClientSession() as session:
            print("\nFetching URL:")
            print(f"URL: {url}")
            
            async with session.get(url) as response:
                print(f"Response status: {response.status}")
                text = await response.text()
                print(f"Response type: {type(text)}")
                print(f"First 200 chars: {text[:200]}")
                try:
                    data = json.loads(text)
                    print(f"Parsed data type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"Keys: {data.keys()}")
                    elif isinstance(data, list):
                        print(f"List length: {len(data)}")
                        if data:
                            print(f"First item type: {type(data[0])}")
                    return data
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    return [] 