#!/usr/bin/env python3
import asyncio
import sys
import argparse
from pathlib import Path

from utils import setup_logger, get_site_logger, load_config, load_sites_config
from sites import SITE_REGISTRY
from notifiers import TelegramNotifier, DingtalkNotifier


async def run_site_checkin(site_id: str, site_config: dict, main_config: dict):
    if not site_config.get('enabled', True):
        print(f"站点 {site_id} 已禁用，跳过")
        return None
    
    if site_id not in SITE_REGISTRY:
        print(f"站点 {site_id} 未找到对应的签到器")
        return None
    
    site_class = SITE_REGISTRY[site_id]
    logger = get_site_logger(
        site_id,
        log_dir='logs',
        level=main_config.get('logging', {}).get('level', 'INFO')
    )
    
    site_name = site_config.get('name', site_id)
    logger.info(f"=" * 50)
    logger.info(f"开始签到: {site_name}")
    logger.info(f"=" * 50)
    
    site = site_class(logger, {site_id: site_config})
    accounts = site_config.get('accounts', [])
    
    if not accounts:
        logger.warning("没有配置账户")
        return None
    
    results = await site.run(accounts)
    
    should_notify = site_config.get('notify', False)
    
    if should_notify and results:
        message = site.format_results_message(results, accounts)
        
        telegram_config = main_config.get('notifications', {}).get('telegram', {})
        telegram = TelegramNotifier(telegram_config, logger)
        await telegram.send_if_enabled(f"CheckinHub - {site_name}", message)
        
        dingtalk_config = main_config.get('notifications', {}).get('dingtalk', {})
        dingtalk = DingtalkNotifier(dingtalk_config, logger)
        await dingtalk.send_if_enabled(f"CheckinHub - {site_name}", message)
    
    return results


async def main():
    parser = argparse.ArgumentParser(description='CheckinHub - 自动签到中心')
    parser.add_argument('sites', nargs='*', help='要运行的站点ID（留空表示运行所有启用的站点）')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有可用站点')
    parser.add_argument('--config', '-c', default='config/config.toml', help='主配置文件路径')
    parser.add_argument('--sites-config', '-s', default='config/sites.toml', help='站点配置文件路径')
    
    args = parser.parse_args()
    
    main_config = load_config(args.config)
    sites_config = load_sites_config(args.sites_config)
    
    if args.list:
        print("\n可用站点列表:")
        print("=" * 60)
        for site_id in SITE_REGISTRY.keys():
            site_class = SITE_REGISTRY[site_id]
            status = "✓" if site_id in sites_config else "✗"
            enabled = "启用" if sites_config.get(site_id, {}).get('enabled', False) else "禁用"
            name = sites_config.get(site_id, {}).get('name', site_id)
            accounts_count = len(sites_config.get(site_id, {}).get('accounts', []))
            print(f"  [{status}] {site_id:12} - {name:20} ({enabled}, {accounts_count} 个账户)")
        print("=" * 60)
        print(f"\n总计: {len(SITE_REGISTRY)} 个站点")
        return
    
    if not sites_config:
        print("错误: 站点配置文件不存在或为空")
        print(f"请创建配置文件: {args.sites_config}")
        return
    
    target_sites = args.sites if args.sites else list(sites_config.keys())
    
    if not target_sites:
        print("没有要运行的站点")
        return
    
    logger = setup_logger(
        "checkinhub",
        level=main_config.get('logging', {}).get('level', 'INFO')
    )
    
    logger.info(f"CheckinHub 启动")
    logger.info(f"将运行 {len(target_sites)} 个站点")
    
    Path('logs').mkdir(exist_ok=True)
    
    for site_id in target_sites:
        if site_id not in sites_config:
            print(f"警告: 站点 {site_id} 未在配置文件中找到")
            continue
        
        site_config = sites_config[site_id]
        
        try:
            await run_site_checkin(site_id, site_config, main_config)
        except Exception as e:
            logger.error(f"站点 {site_id} 运行失败: {e}", exc_info=True)
    
    logger.info("CheckinHub 运行完成")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n用户中断")
        sys.exit(0)
