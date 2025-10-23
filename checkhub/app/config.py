import os
import toml
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

CONFIG_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

SITES_CONFIG_PATH = CONFIG_DIR / "sites.toml"
SETTINGS_CONFIG_PATH = CONFIG_DIR / "settings.toml"


def load_sites_config():
    if not SITES_CONFIG_PATH.exists():
        default_config = {
            "example": {
                "name": "示例站点",
                "enabled": True,
                "checker_class": "ExampleChecker",
                "accounts": [
                    {
                        "username": "user1",
                        "password": "pass1",
                        "enabled": True
                    }
                ]
            }
        }
        with open(SITES_CONFIG_PATH, "w", encoding="utf-8") as f:
            toml.dump(default_config, f)
        return default_config
    
    with open(SITES_CONFIG_PATH, "r", encoding="utf-8") as f:
        return toml.load(f)


def save_sites_config(config):
    with open(SITES_CONFIG_PATH, "w", encoding="utf-8") as f:
        toml.dump(config, f)


def load_settings():
    if not SETTINGS_CONFIG_PATH.exists():
        default_settings = {
            "admin": {
                "username": "admin",
                "password": "admin123"
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
            },
            "scheduler": {
                "enabled": True,
                "check_time": "08:00"
            }
        }
        with open(SETTINGS_CONFIG_PATH, "w", encoding="utf-8") as f:
            toml.dump(default_settings, f)
        return default_settings
    
    with open(SETTINGS_CONFIG_PATH, "r", encoding="utf-8") as f:
        return toml.load(f)


def save_settings(settings):
    with open(SETTINGS_CONFIG_PATH, "w", encoding="utf-8") as f:
        toml.dump(settings, f)
