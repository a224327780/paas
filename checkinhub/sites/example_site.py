import aiohttp
import asyncio
from typing import Dict, Any
from .base import BaseSite, CheckinResult


class ExampleSite(BaseSite):
    site_name = "example"
    
    async def checkin(self, account: Dict[str, Any]) -> CheckinResult:
        username = account.get('username', '')
        password = account.get('password', '')
        
        await asyncio.sleep(0.5)
        
        return CheckinResult(
            success=True,
            message=f"示例签到成功 (这是一个演示)",
            data={
                'username': username,
                'points': 10,
                'total_days': 100
            }
        )
