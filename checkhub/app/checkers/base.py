import httpx
from typing import Dict, Any, Optional
from datetime import datetime


class CheckResult:
    def __init__(self, success: bool, message: str, data: Optional[Dict] = None):
        self.success = success
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now()
    
    def __str__(self):
        status = "✅ 成功" if self.success else "❌ 失败"
        return f"{status}: {self.message}"


class BaseChecker:
    def __init__(self, site_id: str, site_name: str, account: Dict[str, Any]):
        self.site_id = site_id
        self.site_name = site_name
        self.account = account
        self.username = account.get("username")
        self.password = account.get("password")
        self.cookies = account.get("cookies")
        self.extra_data = account.get("extra_data", {})
        
    async def check_in(self) -> CheckResult:
        try:
            result = await self._do_check_in()
            return result
        except Exception as e:
            return CheckResult(False, f"签到异常: {str(e)}")
    
    async def _do_check_in(self) -> CheckResult:
        raise NotImplementedError("子类必须实现 _do_check_in 方法")
    
    async def login(self) -> bool:
        return False
    
    def get_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
