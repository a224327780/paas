import aiohttp
import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import Optional
from .base import BaseNotifier


class DingtalkNotifier(BaseNotifier):
    def __init__(self, config: dict, logger=None):
        super().__init__(config, logger)
        self.webhook = config.get('webhook', '')
        self.secret = config.get('secret', '')
    
    def _generate_sign(self) -> tuple:
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign
    
    async def send(self, title: str, message: str) -> bool:
        if not self.webhook:
            if self.logger:
                self.logger.error("钉钉 Webhook 未配置")
            return False
        
        url = self.webhook
        
        if self.secret:
            timestamp, sign = self._generate_sign()
            url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"## {title}\n\n{message}"
            }
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
                        if data.get('errcode') == 0:
                            return True
                        else:
                            if self.logger:
                                self.logger.error(f"钉钉 API 返回错误: {data.get('errmsg', '')}")
                            return False
                    else:
                        if self.logger:
                            self.logger.error(f"钉钉 HTTP 错误: {resp.status}")
                        return False
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"钉钉发送失败: {e}")
            return False
