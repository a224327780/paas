from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import asyncio


@dataclass
class CheckinResult:
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class BaseSite(ABC):
    site_name: str = "base"
    
    def __init__(self, logger, config: Dict[str, Any]):
        self.logger = logger
        self.config = config
        self.site_config = config.get(self.site_name, {})
    
    @abstractmethod
    async def checkin(self, account: Dict[str, Any]) -> CheckinResult:
        pass
    
    async def run(self, accounts: List[Dict[str, Any]]) -> List[CheckinResult]:
        results = []
        enabled_accounts = [acc for acc in accounts if acc.get('enabled', True)]
        
        if not enabled_accounts:
            self.logger.info("没有启用的账户")
            return results
        
        self.logger.info(f"开始签到，共 {len(enabled_accounts)} 个账户")
        
        for account in enabled_accounts:
            username = account.get('username', 'unknown')
            try:
                self.logger.info(f"正在签到账户: {username}", extra={'account': username})
                result = await self.checkin(account)
                
                if result.success:
                    self.logger.info(f"签到成功: {result.message}", extra={'account': username})
                else:
                    self.logger.error(f"签到失败: {result.message}", extra={'account': username})
                
                results.append(result)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                error_msg = f"签到异常: {str(e)}"
                self.logger.error(error_msg, extra={'account': username}, exc_info=True)
                results.append(CheckinResult(success=False, message=error_msg))
        
        success_count = sum(1 for r in results if r.success)
        self.logger.info(f"签到完成: 成功 {success_count}/{len(results)}")
        
        return results
    
    def format_results_message(self, results: List[CheckinResult], accounts: List[Dict[str, Any]]) -> str:
        site_name = self.site_config.get('name', self.site_name)
        lines = [f"📊 {site_name} 签到报告\n"]
        
        for i, result in enumerate(results):
            username = accounts[i].get('username', 'unknown') if i < len(accounts) else 'unknown'
            status = "✅" if result.success else "❌"
            lines.append(f"{status} {username}: {result.message}")
        
        success_count = sum(1 for r in results if r.success)
        lines.append(f"\n总计: 成功 {success_count}/{len(results)}")
        
        return "\n".join(lines)
