from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel


class ProxyInfo(BaseModel):
    protocol: str
    host: str
    port: int
    username: str = None
    password: str = None
    raw_config: str = None
    extra_params: dict = None
    
    def to_url(self) -> str:
        if self.protocol in ['http', 'https', 'socks5']:
            auth = f"{self.username}:{self.password}@" if self.username else ""
            return f"{self.protocol}://{auth}{self.host}:{self.port}"
        return self.raw_config or ""
    
    def __str__(self):
        return f"{self.protocol}://{self.host}:{self.port}"


class DataSource(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get('enabled', True)
    
    @abstractmethod
    async def fetch_proxies(self) -> List[ProxyInfo]:
        pass
    
    @abstractmethod
    async def close(self):
        pass
