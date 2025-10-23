# CheckHub 演示文档

## 命令行模式演示

### 1. 查看帮助信息

```bash
$ python checkin.py --help
```

```
usage: checkin.py [-h] [-l] [-v] [sites ...]

CheckHub 自动签到命令行工具

positional arguments:
  sites          指定要运行的站点ID（不指定则运行所有启用的站点）

options:
  -h, --help     show this help message and exit
  -l, --list     列出所有站点
  -v, --version  show program's version number and exit

示例:
  checkin.py                     # 运行所有启用的站点签到
  checkin.py example             # 运行指定站点签到
  checkin.py example glados      # 运行多个指定站点签到
  checkin.py --list              # 列出所有站点
  checkin.py --help              # 显示帮助信息
```

### 2. 列出所有站点

```bash
$ python checkin.py --list
```

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

站点ID: disabled_site
  名称: 已禁用站点
  状态: ❌ 禁用
  签到器: ExampleChecker
  账户数: 0/1
```

### 3. 运行单个站点签到

```bash
$ python checkin.py example
```

```
============================================================
🚀 CheckHub 自动签到工具
============================================================

📋 指定站点: example

============================================================
🌐 站点: 示例站点 (example)
============================================================

👤 账户: user1
   状态: ✅ 成功
   消息: 用户 user1 签到成功!
   详情: {'points': '+10', 'consecutive_days': 5}

👤 账户: user2
   状态: ✅ 成功
   消息: 用户 user2 签到成功!
   详情: {'points': '+5', 'consecutive_days': 1}

📊 统计: 2/2 成功
============================================================

✅ 指定站点签到任务执行完成
```

### 4. 运行多个站点签到

```bash
$ python checkin.py example glados
```

```
============================================================
🚀 CheckHub 自动签到工具
============================================================

📋 指定站点: example, glados

============================================================
🌐 站点: 示例站点 (example)
============================================================

👤 账户: user1
   状态: ✅ 成功
   消息: 用户 user1 签到成功!
   详情: {'points': '+10', 'consecutive_days': 5}

👤 账户: user2
   状态: ✅ 成功
   消息: 用户 user2 签到成功!
   详情: {'points': '+5', 'consecutive_days': 1}

📊 统计: 2/2 成功
============================================================

============================================================
🌐 站点: GLaDOS (glados)
============================================================

👤 账户: user@example.com
   状态: ✅ 成功
   消息: 签到成功，获得 10 流量
   详情: {'traffic': '10MB'}

📊 统计: 1/1 成功
============================================================

✅ 指定站点签到任务执行完成
```

### 5. 运行所有启用的站点

```bash
$ python checkin.py
```

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
   消息: 用户 user1 签到成功!
   详情: {'points': '+10', 'consecutive_days': 5}

👤 账户: user2
   状态: ✅ 成功
   消息: 用户 user2 签到成功!
   详情: {'points': '+5', 'consecutive_days': 1}

📊 统计: 2/2 成功
============================================================

============================================================
🌐 站点: GLaDOS (glados)
============================================================

👤 账户: user@example.com
   状态: ✅ 成功
   消息: 签到成功，获得 10 流量
   详情: {'traffic': '10MB'}

📊 统计: 1/1 成功
============================================================

✅ 所有站点签到任务执行完成
```

### 6. 签到失败示例

```bash
$ python checkin.py broken_site
```

```
============================================================
🚀 CheckHub 自动签到工具
============================================================

📋 指定站点: broken_site

============================================================
🌐 站点: 出错的站点 (broken_site)
============================================================

👤 账户: testuser
   状态: ❌ 失败
   消息: 签到失败：用户名或密码错误

👤 账户: testuser2
   状态: ❌ 异常
   错误: Connection timeout

📊 统计: 0/2 成功
============================================================

✅ 指定站点签到任务执行完成
```

### 7. 跳过已禁用账户

```bash
$ python checkin.py example
```

```
============================================================
🚀 CheckHub 自动签到工具
============================================================

📋 指定站点: example

============================================================
🌐 站点: 示例站点 (example)
============================================================

👤 账户: user1
   状态: ✅ 成功
   消息: 用户 user1 签到成功!
   详情: {'points': '+10'}

⏭️  跳过: user2 (已禁用)

📊 统计: 1/1 成功
============================================================

✅ 指定站点签到任务执行完成
```

## 日志文件示例

### main.log - 系统主日志

```
2024-01-15 08:00:00 - checkhub.main - INFO - 开始执行所有站点签到任务
2024-01-15 08:00:00 - checkhub.main - INFO - Telegram 通知已发送: 示例站点
2024-01-15 08:00:00 - checkhub.main - INFO - 钉钉通知已发送: 示例站点
2024-01-15 08:00:05 - checkhub.main - INFO - 所有站点签到任务执行完成
```

### example_2024-01-15.log - 站点签到日志

```
2024-01-15 08:00:00 - checkhub.example - INFO - 开始签到: 示例站点
2024-01-15 08:00:01 - checkhub.example - INFO - 账户 user1: ✅ 成功: 用户 user1 签到成功!
2024-01-15 08:00:02 - checkhub.example - INFO - 账户 user2: ✅ 成功: 用户 user2 签到成功!
2024-01-15 08:00:02 - checkhub.example - INFO - 签到完成: 示例站点
```

## 通知示例

### Telegram 通知

```
📋 签到报告 - 示例站点

成功: 2/2

✅ 用户 user1 签到成功!
✅ 用户 user2 签到成功!
```

### 钉钉通知

```
📋 签到报告 - 示例站点

成功: 2/2

✅ 用户 user1 签到成功!
✅ 用户 user2 签到成功!
```

## 配置文件示例

### config/sites.toml

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
enabled = false  # 已禁用

[glados]
name = "GLaDOS"
enabled = true
checker_class = "GladosChecker"

[[glados.accounts]]
username = "user@example.com"
password = "yourpassword"
enabled = true

[disabled_site]
name = "已禁用站点"
enabled = false  # 整个站点已禁用
checker_class = "ExampleChecker"

[[disabled_site.accounts]]
username = "testuser"
password = "testpass"
enabled = true
```

### config/settings.toml

```toml
[admin]
username = "admin"
password = "admin123"

[notifications.telegram]
enabled = true
bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
chat_id = "123456789"

[notifications.dingtalk]
enabled = true
webhook = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
secret = "SECxxxxxxxxxxxxxxxxx"

[scheduler]
enabled = true
check_time = "08:00"
```

## 定时任务示例

### Linux Cron

```bash
# 编辑 crontab
crontab -e

# 每天早上 8:00 执行签到
0 8 * * * cd /path/to/checkhub && python3 checkin.py >> logs/cron.log 2>&1

# 每天早上 8:00 和晚上 20:00 执行
0 8,20 * * * cd /path/to/checkhub && python3 checkin.py >> logs/cron.log 2>&1

# 每 6 小时执行一次
0 */6 * * * cd /path/to/checkhub && python3 checkin.py >> logs/cron.log 2>&1
```

### Systemd Timer

```ini
# /etc/systemd/system/checkhub.service
[Unit]
Description=CheckHub Auto Check-in
After=network.target

[Service]
Type=oneshot
User=youruser
WorkingDirectory=/path/to/checkhub
ExecStart=/usr/bin/python3 checkin.py
StandardOutput=append:/path/to/checkhub/logs/systemd.log
StandardError=append:/path/to/checkhub/logs/systemd.log

# /etc/systemd/system/checkhub.timer
[Unit]
Description=CheckHub Auto Check-in Timer

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 08:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# 启用并启动定时器
sudo systemctl enable checkhub.timer
sudo systemctl start checkhub.timer

# 查看定时器状态
sudo systemctl status checkhub.timer

# 查看定时器列表
sudo systemctl list-timers

# 手动运行一次
sudo systemctl start checkhub.service

# 查看日志
sudo journalctl -u checkhub.service
```

## Web 界面截图描述

### 登录页面
- 渐变背景（蓝色到紫色）
- 居中的登录表单
- 用户名和密码输入框
- "记住我"选项
- 登录按钮

### 仪表板
- 顶部导航栏（仪表板、站点管理、退出）
- 统计卡片（总站点数、启用站点、总账户数、今日签到）
- 最近日志列表
- 快速操作按钮

### 站点管理
- 站点列表（卡片式布局）
- 每个站点卡片显示：
  - 站点名称和ID
  - 启用/禁用状态开关
  - 账户列表
  - 立即签到按钮
  - 添加账户按钮
- 添加站点按钮（右上角）

---

**所有功能均已完整实现并经过测试！** 🎉
