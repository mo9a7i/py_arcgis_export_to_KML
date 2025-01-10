import json
from typing import Optional
import aiohttp
from urllib.parse import urlparse, parse_qs

class ArcGISResolver:
    def __init__(self):
        self.base_url = "https://www.arcgis.com/sharing/rest/content/items"
    
    async def get_webmap_data(self, viewer_url: str) -> Optional[dict]:
        """
        Resolve ArcGIS webmap data from a viewer URL through these steps:
        1. Extract appid from viewer URL
        2. Get webmap id from appid metadata
        3. Fetch actual webmap data
        """
        try:
            print(f"\nResolving webmap from viewer URL: {viewer_url}")
            
            app_id = self._extract_app_id(viewer_url)
            print(f"Extracted app_id: {app_id}")
            if not app_id:
                raise ValueError("No appid found in viewer URL")
            
            print(f"\nFetching metadata for app_id: {app_id}")
            webmap_id = await self._get_webmap_id(app_id)
            print(f"Retrieved webmap_id: {webmap_id}")
            if not webmap_id:
                raise ValueError(f"No webmap id found for app {app_id}")
            
            print(f"\nFetching webmap data for id: {webmap_id}")
            return await self._fetch_webmap_data(webmap_id)
            
        except Exception as e:
            print(f"Error resolving webmap data: {e}")
            return None

    def _extract_app_id(self, url: str) -> Optional[str]:
        """Extract appid from ArcGIS viewer URL"""
        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            return params.get('appid', [None])[0]
        except Exception as e:
            print(f"Error extracting appid: {e}")
            return None

    async def _get_webmap_id(self, app_id: str) -> Optional[str]:
        """Get webmap id from application metadata"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/{app_id}/data"
            params = {'f': 'json'}
            
            try:
                print(f"Requesting URL: {url}")
                async with session.get(url, params=params) as response:
                    print(f"Response status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        print(f"Response data: {json.dumps(data, indent=2)}")
                        # Look for webmap ID in values.webmap
                        webmap_id = data.get('values', {}).get('webmap')
                        if webmap_id:
                            print(f"Found webmap ID in values.webmap: {webmap_id}")
                        return webmap_id
                    else:
                        print(f"Error fetching app metadata: {response.status}")
                        return None
            except Exception as e:
                print(f"Error in webmap id request: {e}")
                return None

    async def _fetch_webmap_data(self, webmap_id: str) -> Optional[dict]:
        """Fetch the actual webmap data"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/{webmap_id}/data"
            params = {'f': 'json'}
            
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Error fetching webmap data: {response.status}")
                        return None
            except Exception as e:
                print(f"Error in webmap data request: {e}")
                return None 