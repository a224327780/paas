# 🚀 从这里开始

欢迎使用 CheckHub 自动签到系统！

## ⚡ 30秒快速开始

```bash
cd checkhub
./quickstart.sh
```

就这么简单！脚本会引导你完成所有设置。

---

## 📖 如果你喜欢阅读文档

### 第一步：了解项目

- **[项目说明.md](项目说明.md)** ⭐ 推荐首读（中文完整说明）
- **[COMPLETED.md](COMPLETED.md)** - 项目完成情况
- **[README.md](README.md)** - 项目概览

### 第二步：选择运行模式

#### 选项 A：命令行模式（推荐用于自动化）

```bash
# 查看所有站点
python checkin.py --list

# 运行签到
python checkin.py
```

📖 详细文档：**[CLI_GUIDE.md](CLI_GUIDE.md)**

#### 选项 B：Web 管理模式（推荐用于可视化管理）

```bash
python run.py
```

访问 http://localhost:8000  
账号：admin / admin123

📖 详细文档：**[USAGE.md](USAGE.md)**

### 第三步：配置站点

编辑 `config/sites.toml` 添加你的站点：

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

📖 配置示例：`config/sites.example.toml`

### 第四步：设置通知（可选）

编辑 `config/settings.toml` 配置通知：

```toml
[notifications.telegram]
enabled = true
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"
```

📖 配置示例：`config/settings.example.toml`

### 第五步：设置定时任务（可选）

```bash
# Linux
crontab -e
# 添加：0 8 * * * cd /path/to/checkhub && python3 checkin.py
```

📖 详细说明：**[CLI_GUIDE.md](CLI_GUIDE.md)**

---

## 📚 完整文档列表

### 必读文档

1. **[项目说明.md](项目说明.md)** - 中文项目完整说明
2. **[CLI_GUIDE.md](CLI_GUIDE.md)** - 命令行使用详细指南
3. **[QUICKSTART.md](QUICKSTART.md)** - 5分钟快速上手

### 参考文档

- **[OVERVIEW.md](OVERVIEW.md)** - 项目总览
- **[FEATURES.md](FEATURES.md)** - 功能特性详解
- **[DEMO.md](DEMO.md)** - 功能演示
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - 架构设计
- **[API.md](API.md)** - API 文档
- **[CHANGELOG.md](CHANGELOG.md)** - 更新日志
- **[TASK_SUMMARY.md](TASK_SUMMARY.md)** - 任务总结

---

## ⚡ 常用命令

```bash
# 查看帮助
python checkin.py --help

# 列出所有站点
python checkin.py --list

# 运行所有启用的站点
python checkin.py

# 运行指定站点
python checkin.py example

# 启动 Web 管理界面
python run.py
```

---

## ✅ 项目特点

- ✅ **多站点支持** - 配置多个站点
- ✅ **多账户管理** - 每个站点支持多账户
- ✅ **双模式运行** - Web + 命令行
- ✅ **通知推送** - Telegram + 钉钉
- ✅ **日志记录** - 按天按站点分割
- ✅ **易于扩展** - 插件式架构

---

## 🎯 快速提示

- 💡 **新手**：运行 `./quickstart.sh` 开始
- 💡 **自动化**：使用命令行模式 + Cron
- 💡 **管理**：使用 Web 模式配置
- 💡 **开发**：查看 ARCHITECTURE.md
- 💡 **问题**：查看 CLI_GUIDE.md 的常见问题

---

## 📞 需要帮助？

1. 查看 **[项目说明.md](项目说明.md)** - 最详细的中文说明
2. 查看 **[CLI_GUIDE.md](CLI_GUIDE.md)** - 命令行完整指南
3. 查看 **[DEMO.md](DEMO.md)** - 查看实际使用示例

---

<div align="center">

**现在就开始使用 CheckHub！**

```bash
./quickstart.sh
```

或

```bash
python checkin.py --list
```

**让自动签到变得简单！** 🎉

</div>
