import aiohttp
import re
from typing import Dict, Any
from .base import BaseSite, CheckinResult


class HostLocSite(BaseSite):
    site_name = "hostloc"
    
    BASE_URL = "https://hostloc.com"
    SPACE_URL = f"{BASE_URL}/space-uid-{{}}.html"
    
    async def checkin(self, account: Dict[str, Any]) -> CheckinResult:
        cookie = account.get('cookie', '')
        uid = account.get('uid', '')
        
        if not cookie:
            return CheckinResult(
                success=False,
                message="Cookie 未配置"
            )
        
        if not uid:
            return CheckinResult(
                success=False,
                message="UID 未配置"
            )
        
        headers = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': self.BASE_URL
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                visit_count = 0
                
                for visit_uid in range(10000, 10010):
                    url = self.SPACE_URL.format(visit_uid)
                    
                    try:
                        async with session.get(
                            url,
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=10),
                            allow_redirects=False
                        ) as resp:
                            if resp.status in [200, 301, 302]:
                                visit_count += 1
                    except:
                        continue
                
                if visit_count > 0:
                    return CheckinResult(
                        success=True,
                        message=f"访问成功，共访问 {visit_count} 个空间",
                        data={'visit_count': visit_count}
                    )
                else:
                    return CheckinResult(
                        success=False,
                        message="访问失败"
                    )
        
        except Exception as e:
            return CheckinResult(
                success=False,
                message=f"请求异常: {str(e)}"
            )
