import asyncio
import aiohttp
from typing import Optional
from python_socks.async_.asyncio.v2 import Proxy
from loguru import logger

from data_sources.base import ProxyInfo


class HttpProtocolHandler:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    async def test_proxy(self, proxy: ProxyInfo, test_url: str) -> tuple[bool, Optional[str], Optional[float]]:
        if proxy.protocol in ['http', 'https']:
            return await self._test_http_proxy(proxy, test_url)
        elif proxy.protocol == 'socks5':
            return await self._test_socks5_proxy(proxy, test_url)
        else:
            return False, f"Unsupported protocol: {proxy.protocol}", None
    
    async def _test_http_proxy(self, proxy: ProxyInfo, test_url: str) -> tuple[bool, Optional[str], Optional[float]]:
        proxy_url = proxy.to_url()
        
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(ssl=False)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                start_time = asyncio.get_event_loop().time()
                
                async with session.get(test_url, proxy=proxy_url) as response:
                    await response.read()
                    
                    end_time = asyncio.get_event_loop().time()
                    latency = (end_time - start_time) * 1000
                    
                    if response.status in [200, 201, 204, 301, 302, 307, 308]:
                        logger.debug(f"HTTP proxy {proxy} is working, latency: {latency:.2f}ms")
                        return True, None, latency
                    else:
                        return False, f"HTTP {response.status}", None
        
        except asyncio.TimeoutError:
            return False, "Timeout", None
        except Exception as e:
            logger.debug(f"HTTP proxy {proxy} failed: {e}")
            return False, str(e), None
    
    async def _test_socks5_proxy(self, proxy: ProxyInfo, test_url: str) -> tuple[bool, Optional[str], Optional[float]]:
        try:
            socks_proxy = Proxy.from_url(proxy.to_url())
            connector = aiohttp.TCPConnector(ssl=False)
            
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                start_time = asyncio.get_event_loop().time()
                
                async with session.get(test_url, proxy=socks_proxy.url) as response:
                    await response.read()
                    
                    end_time = asyncio.get_event_loop().time()
                    latency = (end_time - start_time) * 1000
                    
                    if response.status in [200, 201, 204, 301, 302, 307, 308]:
                        logger.debug(f"SOCKS5 proxy {proxy} is working, latency: {latency:.2f}ms")
                        return True, None, latency
                    else:
                        return False, f"HTTP {response.status}", None
        
        except asyncio.TimeoutError:
            return False, "Timeout", None
        except Exception as e:
            logger.debug(f"SOCKS5 proxy {proxy} failed: {e}")
            return False, str(e), None
