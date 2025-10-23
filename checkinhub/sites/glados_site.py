import aiohttp
import json
from typing import Dict, Any
from .base import BaseSite, CheckinResult


class GladosSite(BaseSite):
    site_name = "glados"
    
    BASE_URL = "https://glados.rocks"
    CHECKIN_URL = f"{BASE_URL}/api/user/checkin"
    STATUS_URL = f"{BASE_URL}/api/user/status"
    
    async def checkin(self, account: Dict[str, Any]) -> CheckinResult:
        cookie = account.get('cookie', '')
        
        if not cookie:
            return CheckinResult(
                success=False,
                message="Cookie 未配置"
            )
        
        headers = {
            'Cookie': cookie,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.CHECKIN_URL,
                    headers=headers,
                    json={"token": "glados.one"},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        if data.get('code') == 0:
                            message = data.get('message', '签到成功')
                            
                            try:
                                async with session.get(
                                    self.STATUS_URL,
                                    headers=headers,
                                    timeout=aiohttp.ClientTimeout(total=30)
                                ) as status_resp:
                                    if status_resp.status == 200:
                                        status_data = await status_resp.json()
                                        leftdays = status_data.get('data', {}).get('leftDays', 'N/A')
                                        message = f"{message}, 剩余天数: {leftdays}"
                            except:
                                pass
                            
                            return CheckinResult(
                                success=True,
                                message=message,
                                data=data
                            )
                        else:
                            return CheckinResult(
                                success=False,
                                message=data.get('message', '签到失败')
                            )
                    else:
                        return CheckinResult(
                            success=False,
                            message=f"HTTP 错误: {resp.status}"
                        )
        
        except asyncio.TimeoutError:
            return CheckinResult(
                success=False,
                message="请求超时"
            )
        except Exception as e:
            return CheckinResult(
                success=False,
                message=f"请求异常: {str(e)}"
            )
