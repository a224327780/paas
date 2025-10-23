import httpx
import asyncio
from .base import BaseChecker, CheckResult


class ExampleChecker(BaseChecker):
    async def _do_check_in(self) -> CheckResult:
        await asyncio.sleep(0.5)
        
        return CheckResult(
            success=True,
            message=f"用户 {self.username} 签到成功!",
            data={
                "points": "+10",
                "consecutive_days": 5
            }
        )
    
    async def login(self) -> bool:
        return True
