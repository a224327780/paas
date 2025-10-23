import os
import toml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "config/config.toml") -> Dict[str, Any]:
    if not os.path.exists(config_path):
        return get_default_config()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
        return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return get_default_config()


def load_sites_config(sites_path: str = "config/sites.toml") -> Dict[str, Any]:
    if not os.path.exists(sites_path):
        print(f"站点配置文件不存在: {sites_path}")
        return {}
    
    try:
        with open(sites_path, 'r', encoding='utf-8') as f:
            sites = toml.load(f)
        return sites
    except Exception as e:
        print(f"加载站点配置失败: {e}")
        return {}


def get_default_config() -> Dict[str, Any]:
    return {
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "console_output": True
        },
        "notifications": {
            "telegram": {
                "enabled": False,
                "bot_token": "",
                "chat_id": ""
            },
            "dingtalk": {
                "enabled": False,
                "webhook": "",
                "secret": ""
            }
        }
    }


def save_example_config(config_path: str = "config/config.toml.example"):
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    
    example_config = {
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "console_output": True
        },
        "notifications": {
            "telegram": {
                "enabled": False,
                "bot_token": "YOUR_BOT_TOKEN",
                "chat_id": "YOUR_CHAT_ID"
            },
            "dingtalk": {
                "enabled": False,
                "webhook": "YOUR_WEBHOOK_URL",
                "secret": "YOUR_SECRET"
            }
        }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        toml.dump(example_config, f)


def save_example_sites_config(sites_path: str = "config/sites.toml.example"):
    Path(sites_path).parent.mkdir(parents=True, exist_ok=True)
    
    example_sites = {
        "example": {
            "name": "示例站点",
            "enabled": True,
            "notify": True,
            "accounts": [
                {
                    "username": "user1@example.com",
                    "password": "password123",
                    "cookie": "",
                    "extra": {"key1": "value1"},
                    "enabled": True
                },
                {
                    "username": "user2@example.com",
                    "password": "password456",
                    "cookie": "",
                    "enabled": True
                }
            ]
        },
        "glados": {
            "name": "GLaDOS",
            "enabled": False,
            "notify": True,
            "accounts": [
                {
                    "username": "your@email.com",
                    "password": "your_password",
                    "cookie": "",
                    "enabled": True
                }
            ]
        }
    }
    
    with open(sites_path, 'w', encoding='utf-8') as f:
        toml.dump(example_sites, f)
