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
                "type": "city,experiences"
            }
            async with session.get(self.settings.VISIT_SAUDI_API, params=params) as response:
                return await response.json()
                
    async def fetch_arcgis_data(self, item_id: str) -> Dict[str, Any]:
        url = f"{self.settings.ARCGIS_API_BASE}/{item_id}/data"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"f": "json"}) as response:
                return await response.json()

    async def fetch_url(self, url: str) -> Dict[str, Any]:
        """Fetch JSON data from any URL, handling both JSON and plain text responses"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                try:
                    return json.loads(text)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse JSON from {url}: {str(e)}") 