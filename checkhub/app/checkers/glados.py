import httpx
from .base import BaseChecker, CheckResult


class GladosChecker(BaseChecker):
    """GLaDOS 签到器示例"""
    
    BASE_URL = "https://glados.rocks"
    
    async def _do_check_in(self) -> CheckResult:
        try:
            headers = self.get_headers()
            
            if self.cookies:
                headers["Cookie"] = self.cookies
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.BASE_URL}/api/user/checkin",
                    headers=headers,
                    json={"token": "glados.one"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("code") == 0:
                        message = data.get("message", "签到成功")
                        return CheckResult(
                            success=True,
                            message=f"用户 {self.username}: {message}",
                            data=data
                        )
                    else:
                        return CheckResult(
                            success=False,
                            message=f"签到失败: {data.get('message', '未知错误')}"
                        )
                else:
                    return CheckResult(
                        success=False,
                        message=f"请求失败: HTTP {response.status_code}"
                    )
                    
        except Exception as e:
            return CheckResult(
                success=False,
                message=f"签到异常: {str(e)}"
            )
