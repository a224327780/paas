# 🎉 欢迎使用 CheckinHub！

## 这是什么？

CheckinHub 是一个**自动签到系统**，可以帮你自动在多个网站上签到。

- ✅ 支持多个站点
- ✅ 支持多个账户
- ✅ 自动签到
- ✅ 结果通知（Telegram / 钉钉）
- ✅ 详细日志

## 🚀 快速开始（3分钟）

### 方式一：自动安装（推荐）

```bash
./quickstart.sh
```

### 方式二：手动安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 复制配置文件
cp config/config.toml.example config/config.toml
cp config/sites.toml.example config/sites.toml

# 3. 编辑配置（重要！）
nano config/sites.toml
```

## ⚙️ 配置你的账户

打开 `config/sites.toml`，编辑你要签到的站点：

```toml
[example]
name = "示例站点"
enabled = true    # 改为 false 可以禁用

[[example.accounts]]
username = "你的用户名"
password = "你的密码"
enabled = true
```

**支持的站点：**
- `example` - 示例站点（用于测试）
- `glados` - GLaDOS
- `hostloc` - HostLoc 论坛

## 🎯 运行签到

```bash
# 查看所有站点
python main.py --list

# 运行所有启用的站点
python main.py

# 只运行指定站点
python main.py example
```

## 📱 设置通知（可选）

### Telegram

1. 找 `@BotFather` 创建机器人，获取 token
2. 找 `@userinfobot` 获取你的 chat_id
3. 编辑 `config/config.toml`：

```toml
[notifications.telegram]
enabled = true
bot_token = "你的 token"
chat_id = "你的 chat_id"
```

### 钉钉

1. 在群里添加自定义机器人
2. 选择"加签"，获取 webhook 和 secret
3. 编辑 `config/config.toml`：

```toml
[notifications.dingtalk]
enabled = true
webhook = "你的 webhook"
secret = "你的 secret"
```

## 📅 设置定时运行（可选）

### Linux/Mac - 使用 cron

```bash
crontab -e
```

添加这一行（每天早上8点运行）：

```bash
0 8 * * * cd /path/to/checkinhub && python main.py
```

### Windows - 使用任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置每天 08:00 运行
4. 程序：python.exe
5. 参数：main.py
6. 起始目录：checkinhub 项目路径

## 📝 查看日志

日志保存在 `logs/` 目录：

```bash
# 查看今天的日志
cat logs/example_$(date +%Y-%m-%d).log

# 实时查看
tail -f logs/example_$(date +%Y-%m-%d).log
```

## 🆘 需要帮助？

### 快速问题

**Q: 如何添加新账户？**
A: 编辑 `config/sites.toml`，在对应站点下添加 `[[站点.accounts]]` 块

**Q: 签到失败怎么办？**
A: 查看日志文件，检查账户信息是否正确

**Q: 如何禁用某个站点？**
A: 在配置中设置 `enabled = false`

**Q: 通知没收到？**
A: 检查配置是否正确，站点的 `notify = true`，通知的 `enabled = true`

### 详细文档

- 📖 [完整使用指南](使用指南.md) - 详细的使用说明
- 🔧 [安装指南](INSTALL.md) - 详细的安装步骤
- 💻 [开发指南](DEVELOP.md) - 如何添加新站点
- 📝 [项目说明](README.md) - 项目介绍

## 🎁 项目文件说明

```
checkinhub/
├── main.py              ← 主程序，运行这个
├── config/              ← 配置文件目录
│   ├── config.toml     ← 主配置（通知、日志）
│   └── sites.toml      ← 站点配置（重要！）
├── logs/                ← 日志文件目录
├── sites/               ← 站点签到模块
├── notifiers/           ← 通知模块
├── utils/               ← 工具模块
└── 文档...              ← 各种说明文档
```

## ✨ 特色功能

1. **异步高效** - 使用 Python asyncio + aiohttp
2. **配置简单** - TOML 格式，清晰易读
3. **日志详细** - 每个站点每天一个日志文件
4. **通知及时** - 支持 Telegram 和钉钉
5. **易于扩展** - 插件式架构，添加新站点很简单

## 🎯 下一步

1. ✅ 安装依赖
2. ✅ 配置站点账户
3. ✅ 测试运行
4. ⬜ 设置通知（可选）
5. ⬜ 设置定时任务（可选）

## 🐳 Docker 部署

如果你熟悉 Docker：

```bash
# 编辑配置文件后
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 💡 小贴士

1. **先测试**：使用示例站点测试，确保程序正常运行
2. **查日志**：遇到问题先看日志，90% 的问题日志里有答案
3. **备份配置**：配置好后记得备份 `config/` 目录
4. **定时清理**：定期清理旧日志文件，节省空间

## 🌟 开始使用

```bash
# 运行这个命令开始！
python main.py example
```

祝你使用愉快！🎉

---

**遇到问题？** 查看 [使用指南.md](使用指南.md) 或提交 Issue
