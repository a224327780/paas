import asyncio
from typing import List
import aiohttp
from loguru import logger

from .base import DataSource, ProxyInfo


class ApiDataSource(DataSource):
    def __init__(self, config: dict):
        super().__init__(config)
        self.url = config.get('url')
        self.method = config.get('method', 'GET').upper()
        self.headers = config.get('headers', {})
        self.interval = config.get('interval', 3600)
        self.session = None
        self._cache = []
        self._last_fetch = 0
    
    async def _init_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    async def fetch_proxies(self) -> List[ProxyInfo]:
        if not self.enabled:
            logger.debug("API data source is disabled")
            return []
        
        current_time = asyncio.get_event_loop().time()
        if self._cache and (current_time - self._last_fetch) < self.interval:
            logger.debug("Returning cached proxies from API source")
            return self._cache
        
        try:
            await self._init_session()
            
            async with self.session.request(
                self.method,
                self.url,
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch proxies from API: HTTP {response.status}")
                    return self._cache
                
                data = await response.json()
                proxies = []
                
                proxy_list = data if isinstance(data, list) else data.get('proxies', [])
                for item in proxy_list:
                    try:
                        proxy = ProxyInfo(**item)
                        proxies.append(proxy)
                    except Exception as e:
                        logger.debug(f"Failed to parse proxy from API response: {e}")
                
                self._cache = proxies
                self._last_fetch = current_time
                logger.info(f"Fetched {len(proxies)} proxies from API")
                return proxies
        
        except Exception as e:
            logger.error(f"Failed to fetch proxies from API: {e}")
            return self._cache
    
    async def close(self):
        if self.session:
            await self.session.close()
