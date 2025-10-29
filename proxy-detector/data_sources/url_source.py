import asyncio
from typing import List
import aiohttp
from loguru import logger

from .base import DataSource, ProxyInfo
from .file_source import FileDataSource


class UrlDataSource(DataSource):
    def __init__(self, config: dict):
        super().__init__(config)
        self.url = config.get('url')
        self.interval = config.get('interval', 3600)
        self.format = config.get('format', 'line')
        self.session = None
        self._cache = []
        self._last_fetch = 0
        self.file_parser = FileDataSource({
            'enabled': True,
            'format': self.format,
            'path': 'dummy'
        })
    
    async def _init_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    async def fetch_proxies(self) -> List[ProxyInfo]:
        if not self.enabled:
            logger.debug("URL data source is disabled")
            return []
        
        current_time = asyncio.get_event_loop().time()
        if self._cache and (current_time - self._last_fetch) < self.interval:
            logger.debug("Returning cached proxies from URL source")
            return self._cache
        
        try:
            await self._init_session()
            
            async with self.session.get(self.url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch proxies from URL: HTTP {response.status}")
                    return self._cache
                
                content = await response.text()
                
                if self.format == 'line':
                    proxies = await self.file_parser._parse_line_format(content)
                elif self.format == 'json':
                    proxies = await self.file_parser._parse_json_format(content)
                elif self.format == 'yaml':
                    proxies = await self.file_parser._parse_yaml_format(content)
                else:
                    logger.error(f"Unsupported format: {self.format}")
                    return self._cache
                
                self._cache = proxies
                self._last_fetch = current_time
                logger.info(f"Fetched {len(proxies)} proxies from URL")
                return proxies
        
        except Exception as e:
            logger.error(f"Failed to fetch proxies from URL: {e}")
            return self._cache
    
    async def close(self):
        if self.session:
            await self.session.close()
