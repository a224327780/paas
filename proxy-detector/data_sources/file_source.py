import json
import yaml
import aiofiles
from pathlib import Path
from typing import List
from loguru import logger

from .base import DataSource, ProxyInfo


class FileDataSource(DataSource):
    def __init__(self, config: dict):
        super().__init__(config)
        self.file_path = Path(config.get('path', './proxies.txt'))
        self.format = config.get('format', 'line')
    
    async def fetch_proxies(self) -> List[ProxyInfo]:
        if not self.enabled:
            logger.debug("File data source is disabled")
            return []
        
        if not self.file_path.exists():
            logger.warning(f"Proxy file not found: {self.file_path}")
            return []
        
        try:
            async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            if self.format == 'line':
                return await self._parse_line_format(content)
            elif self.format == 'json':
                return await self._parse_json_format(content)
            elif self.format == 'yaml':
                return await self._parse_yaml_format(content)
            else:
                logger.error(f"Unsupported format: {self.format}")
                return []
        
        except Exception as e:
            logger.error(f"Failed to read proxy file: {e}")
            return []
    
    async def _parse_line_format(self, content: str) -> List[ProxyInfo]:
        proxies = []
        for line in content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            try:
                proxy = self._parse_proxy_string(line)
                if proxy:
                    proxies.append(proxy)
            except Exception as e:
                logger.debug(f"Failed to parse proxy line: {line} - {e}")
        
        logger.info(f"Loaded {len(proxies)} proxies from file")
        return proxies
    
    async def _parse_json_format(self, content: str) -> List[ProxyInfo]:
        try:
            data = json.loads(content)
            proxies = []
            
            for item in data if isinstance(data, list) else [data]:
                try:
                    proxy = ProxyInfo(**item)
                    proxies.append(proxy)
                except Exception as e:
                    logger.debug(f"Failed to parse proxy from JSON: {e}")
            
            logger.info(f"Loaded {len(proxies)} proxies from JSON")
            return proxies
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            return []
    
    async def _parse_yaml_format(self, content: str) -> List[ProxyInfo]:
        try:
            data = yaml.safe_load(content)
            proxies = []
            
            proxy_list = data.get('proxies', []) if isinstance(data, dict) else data
            for item in proxy_list if isinstance(proxy_list, list) else [proxy_list]:
                try:
                    proxy = ProxyInfo(**item)
                    proxies.append(proxy)
                except Exception as e:
                    logger.debug(f"Failed to parse proxy from YAML: {e}")
            
            logger.info(f"Loaded {len(proxies)} proxies from YAML")
            return proxies
        except Exception as e:
            logger.error(f"Failed to parse YAML: {e}")
            return []
    
    def _parse_proxy_string(self, proxy_str: str) -> ProxyInfo:
        proxy_str = proxy_str.strip()
        
        if '://' in proxy_str:
            parts = proxy_str.split('://', 1)
            protocol = parts[0].lower()
            rest = parts[1]
            
            if '@' in rest:
                auth, host_port = rest.rsplit('@', 1)
                if ':' in auth:
                    username, password = auth.split(':', 1)
                else:
                    username, password = auth, None
            else:
                username, password = None, None
                host_port = rest
            
            if ':' in host_port:
                host, port_str = host_port.rsplit(':', 1)
                try:
                    port = int(port_str.rstrip('/'))
                except ValueError:
                    logger.debug(f"Invalid port in proxy string: {proxy_str}")
                    return None
            else:
                host = host_port.rstrip('/')
                port = 443 if protocol == 'https' else 80
            
            return ProxyInfo(
                protocol=protocol,
                host=host,
                port=port,
                username=username,
                password=password,
                raw_config=proxy_str
            )
        
        if proxy_str.startswith('ss://') or proxy_str.startswith('ssr://') or \
           proxy_str.startswith('vmess://') or proxy_str.startswith('vless://') or \
           proxy_str.startswith('trojan://') or proxy_str.startswith('hysteria://') or \
           proxy_str.startswith('hysteria2://') or proxy_str.startswith('hy2://'):
            protocol = proxy_str.split('://', 1)[0].lower()
            if protocol == 'hy2':
                protocol = 'hysteria2'
            
            return ProxyInfo(
                protocol=protocol,
                host='',
                port=0,
                raw_config=proxy_str
            )
        
        return None
    
    async def close(self):
        pass
