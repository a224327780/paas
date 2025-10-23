import httpx
import hmac
import hashlib
import base64
import time
from urllib.parse import quote_plus


class DingTalkNotifier:
    def __init__(self, webhook: str, secret: str = ""):
        self.webhook = webhook
        self.secret = secret
    
    def _sign(self, timestamp: str) -> str:
        if not self.secret:
            return ""
        
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        return sign
    
    async def send_message(self, message: str) -> bool:
        if not self.webhook:
            return False
        
        try:
            timestamp = str(round(time.time() * 1000))
            sign = self._sign(timestamp)
            
            url = self.webhook
            if sign:
                url = f"{url}&timestamp={timestamp}&sign={sign}"
            
            data = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, timeout=10)
                return response.status_code == 200
        except Exception as e:
            print(f"钉钉通知发送失败: {e}")
            return False
    
    async def send_check_result(self, site_name: str, results: list):
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        message = f"📋 签到报告 - {site_name}\n\n"
        message += f"成功: {success_count}/{total_count}\n\n"
        
        for result in results:
            status = "✅" if result.success else "❌"
            message += f"{status} {result.message}\n"
        
        await self.send_message(message)
