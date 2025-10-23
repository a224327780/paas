from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config import load_settings, load_sites_config
from app.models import Site
from app.checkers import get_checker
from app.notifiers import TelegramNotifier, DingTalkNotifier
from app.utils.logger import setup_logger, get_main_logger


class CheckScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.logger = get_main_logger()
    
    def start(self):
        settings = load_settings()
        scheduler_config = settings.get("scheduler", {})
        
        if not scheduler_config.get("enabled", True):
            self.logger.info("定时任务已禁用")
            return
        
        check_time = scheduler_config.get("check_time", "08:00")
        hour, minute = check_time.split(":")
        
        self.scheduler.add_job(
            self.run_all_checks,
            CronTrigger(hour=int(hour), minute=int(minute)),
            id="daily_check",
            replace_existing=True
        )
        
        self.scheduler.start()
        self.logger.info(f"定时任务已启动，每天 {check_time} 执行签到")
    
    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.logger.info("定时任务已停止")
    
    async def run_all_checks(self):
        self.logger.info("开始执行所有站点签到任务")
        sites_config = load_sites_config()
        
        for site_id, site_data in sites_config.items():
            site = Site.from_config(site_id, site_data)
            if site.enabled:
                await self.check_site(site)
        
        self.logger.info("所有站点签到任务执行完成")
    
    async def check_site(self, site: Site):
        logger = setup_logger(site.id)
        logger.info(f"开始签到: {site.name}")
        
        results = []
        
        for account in site.accounts:
            if not account.enabled:
                continue
            
            checker_class = get_checker(site.checker_class)
            checker = checker_class(
                site.id,
                site.name,
                account.model_dump()
            )
            
            result = await checker.check_in()
            results.append(result)
            
            logger.info(f"账户 {account.username}: {result}")
        
        await self._send_notifications(site.name, results)
        
        logger.info(f"签到完成: {site.name}")
        return results
    
    async def _send_notifications(self, site_name: str, results: list):
        if not results:
            return
        
        settings = load_settings()
        notifications = settings.get("notifications", {})
        
        telegram_config = notifications.get("telegram", {})
        if telegram_config.get("enabled", False):
            notifier = TelegramNotifier(
                telegram_config.get("bot_token", ""),
                telegram_config.get("chat_id", "")
            )
            await notifier.send_check_result(site_name, results)
        
        dingtalk_config = notifications.get("dingtalk", {})
        if dingtalk_config.get("enabled", False):
            notifier = DingTalkNotifier(
                dingtalk_config.get("webhook", ""),
                dingtalk_config.get("secret", "")
            )
            await notifier.send_check_result(site_name, results)
