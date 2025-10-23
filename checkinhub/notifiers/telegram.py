import aiohttp
from typing import Optional
from .base import BaseNotifier


class TelegramNotifier(BaseNotifier):
    def __init__(self, config: dict, logger=None):
        super().__init__(config, logger)
        self.bot_token = config.get('bot_token', '')
        self.chat_id = config.get('chat_id', '')
    
    async def send(self, title: str, message: str) -> bool:
        if not self.bot_token or not self.chat_id:
            if self.logger:
                self.logger.error("Telegram 配置不完整")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        text = f"*{title}*\n\n{message}"
        
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('ok', False)
                    else:
                        if self.logger:
                            self.logger.error(f"Telegram API 返回错误: {resp.status}")
                        return False
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"Telegram 发送失败: {e}")
            return False
