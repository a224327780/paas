#!/usr/bin/env python3
"""
CheckHub 命令行签到工具

用法:
    python checkin.py                # 运行所有启用的站点签到
    python checkin.py example        # 运行指定站点签到
    python checkin.py example glados # 运行多个指定站点签到
"""

import sys
import asyncio
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.config import load_settings, load_sites_config
from app.models.site import Site
from app.checkers import get_checker
from app.notifiers.telegram import TelegramNotifier
from app.notifiers.dingtalk import DingTalkNotifier
from app.utils.logger import setup_logger, get_main_logger


class CheckInCLI:
    """命令行签到工具"""
    
    def __init__(self):
        self.logger = get_main_logger()
        self.settings = load_settings()
        self.sites_config = load_sites_config()
    
    async def check_site(self, site: Site):
        """执行单个站点的签到"""
        logger = setup_logger(site.id)
        logger.info(f"开始签到: {site.name}")
        print(f"\n{'='*60}")
        print(f"🌐 站点: {site.name} ({site.id})")
        print(f"{'='*60}")
        
        results = []
        
        for account in site.accounts:
            if not account.enabled:
                logger.info(f"跳过已禁用账户: {account.username}")
                print(f"⏭️  跳过: {account.username} (已禁用)")
                continue
            
            print(f"\n👤 账户: {account.username}")
            
            try:
                checker_class = get_checker(site.checker_class)
                checker = checker_class(
                    site.id,
                    site.name,
                    account.model_dump()
                )
                
                result = await checker.check_in()
                results.append(result)
                
                status = "✅ 成功" if result.success else "❌ 失败"
                logger.info(f"账户 {account.username}: {result}")
                print(f"   状态: {status}")
                print(f"   消息: {result.message}")
                
                if result.data:
                    print(f"   详情: {result.data}")
            
            except Exception as e:
                logger.error(f"账户 {account.username} 签到异常: {e}")
                print(f"   状态: ❌ 异常")
                print(f"   错误: {e}")
        
        await self._send_notifications(site.name, results)
        
        logger.info(f"签到完成: {site.name}")
        
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        print(f"\n📊 统计: {success_count}/{total_count} 成功")
        print(f"{'='*60}\n")
        
        return results
    
    async def _send_notifications(self, site_name: str, results: list):
        """发送通知"""
        if not results:
            return
        
        notifications = self.settings.get("notifications", {})
        
        telegram_config = notifications.get("telegram", {})
        if telegram_config.get("enabled", False):
            try:
                notifier = TelegramNotifier(
                    telegram_config.get("bot_token", ""),
                    telegram_config.get("chat_id", "")
                )
                await notifier.send_check_result(site_name, results)
                self.logger.info(f"Telegram 通知已发送: {site_name}")
            except Exception as e:
                self.logger.error(f"Telegram 通知发送失败: {e}")
        
        dingtalk_config = notifications.get("dingtalk", {})
        if dingtalk_config.get("enabled", False):
            try:
                notifier = DingTalkNotifier(
                    dingtalk_config.get("webhook", ""),
                    dingtalk_config.get("secret", "")
                )
                await notifier.send_check_result(site_name, results)
                self.logger.info(f"钉钉通知已发送: {site_name}")
            except Exception as e:
                self.logger.error(f"钉钉通知发送失败: {e}")
    
    async def run_all_sites(self):
        """运行所有启用的站点签到"""
        self.logger.info("开始执行所有站点签到任务")
        print("\n" + "="*60)
        print("🚀 CheckHub 自动签到工具")
        print("="*60)
        
        enabled_sites = []
        for site_id, site_data in self.sites_config.items():
            site = Site.from_config(site_id, site_data)
            if site.enabled:
                enabled_sites.append(site)
        
        if not enabled_sites:
            print("\n⚠️  没有启用的站点，请在 config/sites.toml 中配置")
            return
        
        print(f"\n📋 共找到 {len(enabled_sites)} 个启用的站点")
        
        for site in enabled_sites:
            await self.check_site(site)
        
        self.logger.info("所有站点签到任务执行完成")
        print("✅ 所有站点签到任务执行完成\n")
    
    async def run_specific_sites(self, site_ids: list):
        """运行指定的站点签到"""
        self.logger.info(f"开始执行指定站点签到任务: {', '.join(site_ids)}")
        print("\n" + "="*60)
        print("🚀 CheckHub 自动签到工具")
        print("="*60)
        print(f"\n📋 指定站点: {', '.join(site_ids)}")
        
        for site_id in site_ids:
            if site_id not in self.sites_config:
                print(f"\n⚠️  站点 '{site_id}' 不存在，跳过")
                self.logger.warning(f"站点 '{site_id}' 不存在")
                continue
            
            site_data = self.sites_config[site_id]
            site = Site.from_config(site_id, site_data)
            
            if not site.enabled:
                print(f"\n⚠️  站点 '{site_id}' 已禁用，跳过")
                self.logger.warning(f"站点 '{site_id}' 已禁用")
                continue
            
            await self.check_site(site)
        
        self.logger.info("指定站点签到任务执行完成")
        print("✅ 指定站点签到任务执行完成\n")
    
    def list_sites(self):
        """列出所有站点"""
        print("\n" + "="*60)
        print("📋 可用站点列表")
        print("="*60 + "\n")
        
        if not self.sites_config:
            print("⚠️  没有配置任何站点，请在 config/sites.toml 中配置\n")
            return
        
        for site_id, site_data in self.sites_config.items():
            site = Site.from_config(site_id, site_data)
            status = "✅ 启用" if site.enabled else "❌ 禁用"
            accounts_count = len([a for a in site.accounts if a.enabled])
            
            print(f"站点ID: {site_id}")
            print(f"  名称: {site.name}")
            print(f"  状态: {status}")
            print(f"  签到器: {site.checker_class}")
            print(f"  账户数: {accounts_count}/{len(site.accounts)}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description='CheckHub 自动签到命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s                     # 运行所有启用的站点签到
  %(prog)s example             # 运行指定站点签到
  %(prog)s example glados      # 运行多个指定站点签到
  %(prog)s --list              # 列出所有站点
  %(prog)s --help              # 显示帮助信息
        '''
    )
    
    parser.add_argument(
        'sites',
        nargs='*',
        help='指定要运行的站点ID（不指定则运行所有启用的站点）'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='列出所有站点'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='CheckHub v1.0.0'
    )
    
    args = parser.parse_args()
    
    cli = CheckInCLI()
    
    if args.list:
        cli.list_sites()
        return
    
    if args.sites:
        asyncio.run(cli.run_specific_sites(args.sites))
    else:
        asyncio.run(cli.run_all_sites())


if __name__ == "__main__":
    main()
