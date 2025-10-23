from abc import ABC, abstractmethod
from typing import Optional


class BaseNotifier(ABC):
    def __init__(self, config: dict, logger=None):
        self.config = config
        self.logger = logger
        self.enabled = config.get('enabled', False)
    
    @abstractmethod
    async def send(self, title: str, message: str) -> bool:
        pass
    
    async def send_if_enabled(self, title: str, message: str) -> bool:
        if not self.enabled:
            if self.logger:
                self.logger.debug(f"{self.__class__.__name__} 未启用，跳过发送")
            return False
        
        try:
            result = await self.send(title, message)
            if result and self.logger:
                self.logger.info(f"{self.__class__.__name__} 通知发送成功")
            return result
        except Exception as e:
            if self.logger:
                self.logger.error(f"{self.__class__.__name__} 通知发送失败: {e}")
            return False
