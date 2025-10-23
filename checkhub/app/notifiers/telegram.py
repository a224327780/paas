import httpx
from typing import Optional


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send_message(self, message: str) -> bool:
        if not self.bot_token or not self.chat_id:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "HTML"
                    },
                    timeout=10
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Telegram通知发送失败: {e}")
            return False
    
    async def send_check_result(self, site_name: str, results: list):
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        message = f"<b>📋 签到报告 - {site_name}</b>\n\n"
        message += f"成功: {success_count}/{total_count}\n\n"
        
        for result in results:
            status = "✅" if result.success else "❌"
            message += f"{status} {result.message}\n"
        
        await self.send_message(message)
