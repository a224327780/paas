#!/usr/bin/env python3
"""基础功能测试"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.config import load_sites_config, load_settings
from app.models import Site
from app.checkers import get_checker
from app.utils.logger import setup_logger


async def test_config():
    """测试配置加载"""
    print("=" * 50)
    print("测试配置加载...")
    
    sites = load_sites_config()
    print(f"✓ 成功加载 {len(sites)} 个站点配置")
    
    settings = load_settings()
    print(f"✓ 成功加载系统设置")
    print(f"  - 管理员: {settings['admin']['username']}")
    print(f"  - 定时任务: {'启用' if settings['scheduler']['enabled'] else '禁用'}")
    print()


async def test_site_model():
    """测试站点模型"""
    print("=" * 50)
    print("测试站点模型...")
    
    sites_config = load_sites_config()
    
    for site_id, site_data in sites_config.items():
        site = Site.from_config(site_id, site_data)
        print(f"✓ 站点: {site.name} ({site.id})")
        print(f"  - 签到器: {site.checker_class}")
        print(f"  - 账户数: {len(site.accounts)}")
        print(f"  - 状态: {'启用' if site.enabled else '禁用'}")
    print()


async def test_checker():
    """测试签到器"""
    print("=" * 50)
    print("测试签到器...")
    
    sites_config = load_sites_config()
    
    for site_id, site_data in sites_config.items():
        site = Site.from_config(site_id, site_data)
        
        if not site.enabled:
            print(f"⊘ 跳过禁用的站点: {site.name}")
            continue
        
        print(f"→ 测试站点: {site.name}")
        
        for i, account in enumerate(site.accounts, 1):
            if not account.enabled:
                print(f"  ⊘ 跳过禁用的账户: {account.username}")
                continue
            
            checker_class = get_checker(site.checker_class)
            checker = checker_class(
                site.id,
                site.name,
                account.model_dump()
            )
            
            result = await checker.check_in()
            
            status = "✓" if result.success else "✗"
            print(f"  {status} 账户 {i}: {account.username}")
            print(f"     {result.message}")
        
        print()


async def test_logger():
    """测试日志系统"""
    print("=" * 50)
    print("测试日志系统...")
    
    logger = setup_logger("test")
    logger.info("这是一条测试日志")
    print("✓ 日志系统正常")
    print()


async def main():
    """运行所有测试"""
    print("\n🎯 CheckHub 基础功能测试\n")
    
    try:
        await test_config()
        await test_site_model()
        await test_logger()
        await test_checker()
        
        print("=" * 50)
        print("✅ 所有测试通过!")
        print()
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
