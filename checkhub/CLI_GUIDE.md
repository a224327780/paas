# CheckHub 命令行使用指南

## 简介

CheckHub 提供了两种运行模式：

1. **Web 管理模式** (`run.py`) - 启动 Web 界面进行可视化管理
2. **命令行模式** (`checkin.py`) - 直接运行签到任务，适合定时任务和自动化

## 命令行模式使用

### 基本用法

```bash
# 运行所有启用的站点签到
python checkin.py

# 运行指定站点签到
python checkin.py example

# 运行多个指定站点签到
python checkin.py example glados

# 列出所有站点
python checkin.py --list
python checkin.py -l

# 查看帮助信息
python checkin.py --help
python checkin.py -h

# 查看版本信息
python checkin.py --version
python checkin.py -v
```

### 详细说明

#### 1. 运行所有站点签到

```bash
python checkin.py
```

这将运行 `config/sites.toml` 中所有 `enabled = true` 的站点。

**输出示例：**
```
============================================================
🚀 CheckHub 自动签到工具
============================================================

📋 共找到 2 个启用的站点

============================================================
🌐 站点: 示例站点 (example)
============================================================

👤 账户: user1
   状态: ✅ 成功
   消息: 签到成功
   详情: {'points': '+10'}

👤 账户: user2
   状态: ✅ 成功
   消息: 签到成功
   详情: {'points': '+10'}

📊 统计: 2/2 成功
============================================================

✅ 所有站点签到任务执行完成
```

#### 2. 运行指定站点签到

```bash
python checkin.py example
```

只运行指定的站点，适合测试或单独执行某个站点的签到。

#### 3. 运行多个指定站点

```bash
python checkin.py example glados
```

可以同时指定多个站点ID，用空格分隔。

#### 4. 列出所有站点

```bash
python checkin.py --list
```

**输出示例：**
```
============================================================
📋 可用站点列表
============================================================

站点ID: example
  名称: 示例站点
  状态: ✅ 启用
  签到器: ExampleChecker
  账户数: 2/2

站点ID: glados
  名称: GLaDOS
  状态: ✅ 启用
  签到器: GladosChecker
  账户数: 1/1
```

## 配置文件

### sites.toml - 站点配置

```toml
[example]
name = "示例站点"
enabled = true
checker_class = "ExampleChecker"

[[example.accounts]]
username = "user1"
password = "pass1"
enabled = true

[[example.accounts]]
username = "user2"
password = "pass2"
enabled = true

[glados]
name = "GLaDOS"
enabled = true
checker_class = "GladosChecker"

[[glados.accounts]]
username = "user@example.com"
password = "yourpassword"
enabled = true
```

**配置说明：**
- `[站点ID]`: 站点的唯一标识符
- `name`: 站点显示名称
- `enabled`: 是否启用该站点（true/false）
- `checker_class`: 签到器类名（必须在代码中已注册）
- `[[站点ID.accounts]]`: 账户列表
  - `username`: 账户用户名
  - `password`: 账户密码
  - `enabled`: 是否启用该账户（true/false）
  - `cookies`: (可选) Cookie 字符串
  - `extra_data`: (可选) 额外数据字典

### settings.toml - 系统设置

```toml
[admin]
username = "admin"
password = "admin123"

[notifications.telegram]
enabled = true
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"

[notifications.dingtalk]
enabled = false
webhook = "YOUR_WEBHOOK_URL"
secret = "YOUR_SECRET"

[scheduler]
enabled = true
check_time = "08:00"
```

**配置说明：**
- `[admin]`: Web 管理界面登录信息
- `[notifications.telegram]`: Telegram 通知配置
  - `enabled`: 是否启用
  - `bot_token`: Telegram Bot Token
  - `chat_id`: 接收消息的 Chat ID
- `[notifications.dingtalk]`: 钉钉通知配置
  - `enabled`: 是否启用
  - `webhook`: 钉钉机器人 Webhook URL
  - `secret`: 钉钉机器人加签密钥
- `[scheduler]`: 定时任务配置（仅 Web 模式）
  - `enabled`: 是否启用定时任务
  - `check_time`: 签到时间（24小时制，如 "08:00"）

## 日志系统

### 日志文件位置

所有日志文件存储在 `logs/` 目录：

```
logs/
├── main.log                    # 系统主日志
├── example_2024-01-15.log      # 示例站点 2024-01-15 的签到日志
├── example_2024-01-16.log      # 示例站点 2024-01-16 的签到日志
└── glados_2024-01-15.log       # GLaDOS 站点 2024-01-15 的签到日志
```

### 日志格式

```
2024-01-15 08:00:00 - checkhub.example - INFO - 开始签到: 示例站点
2024-01-15 08:00:01 - checkhub.example - INFO - 账户 user1: ✅ 成功: 签到成功
2024-01-15 08:00:02 - checkhub.example - INFO - 账户 user2: ✅ 成功: 签到成功
2024-01-15 08:00:03 - checkhub.example - INFO - 签到完成: 示例站点
```

### 日志特点

- ✅ **按天分割**: 每个站点每天一个日志文件
- ✅ **自动创建**: 首次运行时自动创建日志文件
- ✅ **UTF-8 编码**: 支持中文日志
- ✅ **详细记录**: 记录每个账户的签到结果

## 通知系统

### Telegram 通知

#### 1. 创建 Bot

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建新 Bot
3. 按提示设置 Bot 名称和用户名
4. 获取 Bot Token

#### 2. 获取 Chat ID

1. 在 Telegram 中搜索 `@userinfobot`
2. 发送任意消息，获取 Chat ID

#### 3. 配置

在 `config/settings.toml` 中配置：

```toml
[notifications.telegram]
enabled = true
bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
chat_id = "123456789"
```

#### 4. 通知内容示例

```
📋 签到报告 - 示例站点

成功: 2/2

✅ 用户 user1 签到成功
✅ 用户 user2 签到成功
```

### 钉钉通知

#### 1. 创建机器人

1. 打开钉钉群聊
2. 群设置 -> 智能群助手 -> 添加机器人
3. 选择"自定义"机器人
4. 设置机器人名称和安全设置（推荐使用加签）
5. 获取 Webhook URL 和密钥

#### 2. 配置

在 `config/settings.toml` 中配置：

```toml
[notifications.dingtalk]
enabled = true
webhook = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
secret = "SECxxxxxxxxxxxxxxxxx"
```

#### 3. 通知内容示例

```
📋 签到报告 - 示例站点

成功: 2/2

✅ 用户 user1 签到成功
✅ 用户 user2 签到成功
```

## 定时任务

### Linux Cron

编辑 crontab：

```bash
crontab -e
```

添加定时任务（每天早上 8 点执行）：

```cron
0 8 * * * cd /path/to/checkhub && python3 checkin.py >> logs/cron.log 2>&1
```

### Windows 任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天早上 8:00）
4. 设置操作：
   - 程序：`python.exe`
   - 参数：`checkin.py`
   - 起始位置：CheckHub 项目路径

### Systemd Timer (Linux)

创建服务文件 `/etc/systemd/system/checkhub.service`：

```ini
[Unit]
Description=CheckHub Auto Check-in
After=network.target

[Service]
Type=oneshot
User=youruser
WorkingDirectory=/path/to/checkhub
ExecStart=/usr/bin/python3 checkin.py
```

创建定时器文件 `/etc/systemd/system/checkhub.timer`：

```ini
[Unit]
Description=CheckHub Auto Check-in Timer

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 08:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

启用并启动：

```bash
sudo systemctl enable checkhub.timer
sudo systemctl start checkhub.timer
sudo systemctl status checkhub.timer
```

## 开发自定义签到器

### 1. 创建签到器文件

在 `app/checkers/` 目录下创建新文件，例如 `mysite.py`：

```python
from app.checkers.base import BaseChecker, CheckResult
import httpx


class MySiteChecker(BaseChecker):
    """我的站点签到器"""
    
    async def _do_check_in(self) -> CheckResult:
        """实现签到逻辑"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://mysite.com/api/checkin",
                    headers=self.get_headers(),
                    json={
                        "username": self.username,
                        "password": self.password
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return CheckResult(
                        success=True,
                        message=f"签到成功！获得 {data['points']} 积分",
                        data={"points": data['points']}
                    )
                else:
                    return CheckResult(
                        success=False,
                        message=f"签到失败：{response.text}"
                    )
        
        except Exception as e:
            return CheckResult(
                success=False,
                message=f"签到异常：{str(e)}"
            )
    
    async def login(self) -> bool:
        """如果需要先登录，可以实现这个方法"""
        pass
```

### 2. 注册签到器

在 `app/checkers/__init__.py` 中注册：

```python
from .base import BaseChecker
from .example import ExampleChecker
from .glados import GladosChecker
from .mysite import MySiteChecker  # 导入你的签到器

CHECKER_REGISTRY = {
    "BaseChecker": BaseChecker,
    "ExampleChecker": ExampleChecker,
    "GladosChecker": GladosChecker,
    "MySiteChecker": MySiteChecker,  # 注册你的签到器
}
```

### 3. 配置站点

在 `config/sites.toml` 中添加站点：

```toml
[mysite]
name = "我的站点"
enabled = true
checker_class = "MySiteChecker"

[[mysite.accounts]]
username = "myuser"
password = "mypass"
enabled = true
```

### 4. 测试签到器

```bash
python checkin.py mysite
```

## 常见问题

### 1. 如何查看签到是否成功？

- **控制台输出**: 运行时会实时显示签到结果
- **日志文件**: 查看 `logs/` 目录下对应的日志文件
- **通知消息**: 如果配置了通知，会收到通知消息

### 2. 签到失败怎么办？

1. 检查日志文件，查看详细错误信息
2. 确认账户用户名和密码是否正确
3. 确认站点是否需要 Cookie 或其他认证信息
4. 查看签到器代码，确认逻辑是否正确

### 3. 如何只运行某个站点？

```bash
python checkin.py 站点ID
```

### 4. 如何临时禁用某个账户？

在 `config/sites.toml` 中将对应账户的 `enabled` 设置为 `false`：

```toml
[[example.accounts]]
username = "user1"
password = "pass1"
enabled = false  # 禁用该账户
```

### 5. 如何查看所有可用站点？

```bash
python checkin.py --list
```

### 6. 通知没有发送怎么办？

1. 确认 `settings.toml` 中通知配置正确
2. 确认 `enabled = true`
3. 查看日志文件中是否有错误信息
4. 测试 Bot Token 和 Webhook 是否有效

### 7. 日志文件太多怎么办？

可以定期清理旧日志文件：

```bash
# 删除 30 天前的日志
find logs/ -name "*.log" -type f -mtime +30 -delete
```

或者在 crontab 中添加自动清理：

```cron
# 每周日凌晨 2 点清理 30 天前的日志
0 2 * * 0 find /path/to/checkhub/logs/ -name "*.log" -type f -mtime +30 -delete
```

## 最佳实践

### 1. 配置备份

定期备份配置文件：

```bash
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/
```

### 2. 日志监控

定期检查日志文件，关注签到失败记录：

```bash
# 查看最近的失败记录
grep "失败\|异常" logs/*.log
```

### 3. 安全性

- ✅ 不要将配置文件提交到 Git 仓库
- ✅ 使用强密码
- ✅ 定期更换密码
- ✅ 限制配置文件权限（`chmod 600 config/*.toml`）

### 4. 性能优化

- 如果有大量站点，可以考虑分批执行
- 可以针对不同站点设置不同的执行时间

## 技术支持

- 📖 查看 [README.md](README.md) 了解项目概览
- 📘 查看 [USAGE.md](USAGE.md) 了解 Web 模式使用
- 🏗️ 查看 [ARCHITECTURE.md](ARCHITECTURE.md) 了解架构设计
- 💬 提交 [Issue](../../issues) 报告问题或建议

## 更新日志

### v1.0.0 (2024-01-15)

- ✅ 命令行模式支持
- ✅ 多站点支持
- ✅ 多账户支持
- ✅ 日志记录（按天分割）
- ✅ Telegram 通知
- ✅ 钉钉通知
- ✅ 插件式签到器架构

---

**Happy Checking! 🎉**
