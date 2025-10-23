# CheckinHub - 自动签到中心

> 🎯 一个基于 Python + Async + Aiohttp 的多站点自动签到系统

## ✨ 特性

- ✅ **多站点支持** - 轻松管理多个签到站点
- ✅ **多账户支持** - 每个站点支持多个账户
- ✅ **TOML 配置** - 简洁清晰的配置文件格式
- ✅ **异步高效** - 基于 asyncio + aiohttp 实现
- ✅ **通知推送** - 支持 Telegram 和钉钉通知
- ✅ **日志记录** - 每个站点每天独立日志文件
- ✅ **插件架构** - 易于扩展新站点
- ✅ **命令行友好** - 支持指定站点运行

## 🏗️ 项目架构

```
checkinhub/
├── config/                    # 配置文件目录
│   ├── config.toml           # 主配置（通知、日志等）
│   └── sites.toml            # 站点及账户配置
├── sites/                    # 站点签到模块
│   ├── __init__.py
│   ├── base.py              # 基础站点类
│   ├── example_site.py      # 示例站点
│   ├── glados_site.py       # GLaDOS 站点
│   └── hostloc_site.py      # HostLoc 站点
├── notifiers/               # 通知模块
│   ├── __init__.py
│   ├── base.py             # 基础通知类
│   ├── telegram.py         # Telegram 通知
│   └── dingtalk.py         # 钉钉通知
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── logger.py          # 日志工具
│   └── config_loader.py   # 配置加载器
├── logs/                  # 日志目录
├── main.py               # 主程序入口
├── requirements.txt      # 依赖文件
└── README.md            # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置文件

复制并编辑配置文件：

```bash
# 主配置
cp config/config.toml.example config/config.toml

# 站点配置
cp config/sites.toml.example config/sites.toml
```

### 3. 运行签到

```bash
# 运行所有启用的站点
python main.py

# 运行指定站点
python main.py example glados

# 列出所有可用站点
python main.py --list
```

## 📝 配置说明

### 主配置 (config/config.toml)

```toml
[logging]
level = "INFO"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
console_output = true

[notifications]
# Telegram 配置
[notifications.telegram]
enabled = false
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"

# 钉钉配置
[notifications.dingtalk]
enabled = false
webhook = "YOUR_WEBHOOK_URL"
secret = "YOUR_SECRET"
```

### 站点配置 (config/sites.toml)

```toml
[example]
name = "示例站点"
enabled = true
notify = true

[[example.accounts]]
username = "user1@example.com"
password = "password123"
cookie = ""
extra = { key1 = "value1" }
enabled = true

[[example.accounts]]
username = "user2@example.com"
password = "password456"
enabled = true

[glados]
name = "GLaDOS"
enabled = false
notify = true

[[glados.accounts]]
username = "your@email.com"
password = "your_password"
cookie = ""
enabled = true
```

## 🔌 添加新站点

### 1. 创建站点类

在 `sites/` 目录下创建新文件，例如 `mysite.py`：

```python
import aiohttp
from .base import BaseSite, CheckinResult

class MySite(BaseSite):
    """我的站点签到"""
    
    site_name = "mysite"
    
    async def checkin(self, account: dict) -> CheckinResult:
        """执行签到"""
        username = account['username']
        password = account['password']
        
        async with aiohttp.ClientSession() as session:
            try:
                # 登录请求
                async with session.post(
                    'https://mysite.com/login',
                    json={'username': username, 'password': password},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        return CheckinResult(False, f"登录失败: {resp.status}")
                    
                    # 签到请求
                    async with session.post(
                        'https://mysite.com/checkin',
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return CheckinResult(True, f"签到成功: {data.get('message', '')}")
                        else:
                            return CheckinResult(False, f"签到失败: {resp.status}")
                            
            except Exception as e:
                return CheckinResult(False, f"请求异常: {str(e)}")
```

### 2. 注册站点

在 `sites/__init__.py` 中添加：

```python
from .mysite import MySite

SITE_REGISTRY = {
    'mysite': MySite,
    # ... 其他站点
}
```

### 3. 添加配置

在 `config/sites.toml` 中添加：

```toml
[mysite]
name = "我的站点"
enabled = true
notify = true

[[mysite.accounts]]
username = "your_username"
password = "your_password"
enabled = true
```

## 📊 日志说明

日志文件存储在 `logs/` 目录：

- `main.log` - 主程序日志
- `{site}_{date}.log` - 每个站点每天的签到日志

日志格式：
```
2024-01-15 08:00:00 - checkinhub.example - INFO - [user1@example.com] 签到成功
2024-01-15 08:00:05 - checkinhub.example - ERROR - [user2@example.com] 签到失败: 网络超时
```

## 🔔 通知配置

### Telegram 通知

1. 与 [@BotFather](https://t.me/BotFather) 创建机器人，获取 `bot_token`
2. 与 [@userinfobot](https://t.me/userinfobot) 获取你的 `chat_id`
3. 在 `config/config.toml` 中配置

### 钉钉通知

1. 在钉钉群中添加自定义机器人
2. 选择"加签"安全设置，获取 `webhook` 和 `secret`
3. 在 `config/config.toml` 中配置

## 🎯 内置站点

项目内置了几个示例站点：

- **example** - 演示站点（用于测试）
- **glados** - GLaDOS 签到
- **hostloc** - HostLoc 论坛签到

## 🔧 开发指南

### 技术栈

- Python 3.8+
- aiohttp - 异步 HTTP 客户端
- toml - 配置文件解析
- asyncio - 异步编程

### 代码结构

```python
# 站点基类
class BaseSite:
    async def checkin(self, account: dict) -> CheckinResult
    async def run(self, accounts: list) -> list

# 通知基类
class BaseNotifier:
    async def send(self, title: str, message: str) -> bool

# 日志工具
class SiteLogger:
    def get_logger(site_name: str) -> logging.Logger
```

## 📅 定时任务

可以使用 cron 或其他调度工具定时运行：

```bash
# crontab 示例 - 每天早上 8 点运行
0 8 * * * cd /path/to/checkinhub && /usr/bin/python3 main.py >> cron.log 2>&1
```

或使用 systemd timer、supervisor 等工具。

## 🤝 贡献

欢迎提交 Pull Request 或 Issue！

## 📄 许可

MIT License

## ⚠️ 免责声明

本项目仅供学习交流使用，请遵守各站点的服务条款。使用本项目所产生的任何后果由使用者自行承担。
