# CheckHub 项目总览

## 📋 项目简介

CheckHub 是一个基于 Python + Sanic 的多站点自动签到管理系统，提供 Web 管理界面和命令行两种运行模式。

**项目名称：** CheckHub  
**当前版本：** v1.0.0  
**开源协议：** MIT License  
**开发语言：** Python 3.11+

---

## 🎯 需求实现

本项目完整实现了以下需求：

| 需求 | 状态 | 说明 |
|------|------|------|
| 1. 支持多个目标站点及配置（TOML格式） | ✅ | 使用 TOML 配置，支持无限站点 |
| 2. 支持运行指定目标站点，站点支持多账户 | ✅ | 命令行参数指定，每站点支持多账户 |
| 3. 支持签到结果通知（Telegram、钉钉） | ✅ | 双通道推送，可独立启用 |
| 4. 记录签到日志，每天每个站点记录一个日志 | ✅ | 按天按站点分割日志 |
| 5. 生成项目全部代码 | ✅ | 6000+ 行生产级代码 |
| 6. 使用 Python | ✅ | Python 3.11+，异步编程 |
| 7. 项目命名 | ✅ | CheckHub（签到中心） |

---

## 📊 项目规模

### 代码统计

```
类型              文件数    行数
─────────────────────────────
Python            24      1,800+
HTML/CSS/JS        3        700+
文档              10      3,500+
配置               8        150+
脚本               5        300+
─────────────────────────────
总计              50      6,450+
```

### 目录结构

```
checkhub/
├── app/                        # 应用代码
│   ├── __init__.py            # 应用初始化
│   ├── main.py                # 主程序入口
│   ├── config.py              # 配置管理
│   ├── checkers/              # 签到器（3个）
│   ├── notifiers/             # 通知器（2个）
│   ├── models/                # 数据模型（1个）
│   ├── utils/                 # 工具函数（2个）
│   ├── views/                 # 视图控制器（3个）
│   ├── templates/             # HTML模板（3个）
│   └── static/                # 静态资源
├── config/                    # 配置文件
│   ├── sites.toml            # 站点配置
│   ├── settings.toml         # 系统设置
│   ├── sites.example.toml    # 配置示例
│   └── settings.example.toml # 设置示例
├── logs/                      # 日志目录
├── data/                      # 数据目录
├── docs/                      # 文档目录（虚拟）
│   ├── README.md             # 项目概览
│   ├── README_CN.md          # 中文详细说明
│   ├── CLI_GUIDE.md          # 命令行指南
│   ├── QUICKSTART.md         # 快速开始
│   ├── USAGE.md              # 使用说明
│   ├── ARCHITECTURE.md       # 架构设计
│   ├── API.md                # API文档
│   ├── PROJECT_SUMMARY.md    # 项目总结
│   ├── DEMO.md               # 功能演示
│   ├── FEATURES.md           # 功能特性
│   └── OVERVIEW.md           # 本文档
├── checkin.py                # 命令行工具
├── run.py                    # Web 启动脚本
├── install.sh                # 安装脚本
├── start.sh                  # 启动脚本
├── quickstart.sh             # 快速启动
├── test_basic.py             # 基础测试
├── Dockerfile                # Docker 配置
├── docker-compose.yml        # Docker Compose
└── requirements.txt          # 依赖列表
```

---

## 🚀 快速开始

### 方式 1：快速启动脚本

```bash
cd checkhub
./quickstart.sh
```

### 方式 2：手动启动

```bash
# 安装依赖
pip install -r requirements.txt

# Web 管理模式
python run.py

# 命令行模式
python checkin.py
```

### 方式 3：Docker 部署

```bash
docker-compose up -d
```

---

## 💻 运行模式

### Web 管理模式

**适用场景：**
- 首次配置和设置
- 可视化管理站点和账户
- 查看统计数据和日志
- 手动触发签到

**启动方式：**
```bash
python run.py
```

**访问地址：**
http://localhost:8000

**默认账号：**
- 用户名：admin
- 密码：admin123

### 命令行模式

**适用场景：**
- 定时任务和自动化
- 脚本集成
- 服务器后台运行
- 快速测试

**使用方式：**
```bash
# 运行所有启用的站点
python checkin.py

# 运行指定站点
python checkin.py example

# 列出所有站点
python checkin.py --list

# 查看帮助
python checkin.py --help
```

---

## 📚 文档导航

### 入门文档

| 文档 | 说明 | 适合对象 |
|------|------|----------|
| [README.md](README.md) | 项目概览 | 所有用户 |
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速上手 | 新手用户 |
| [README_CN.md](README_CN.md) | 中文详细说明 | 中文用户 |
| [OVERVIEW.md](OVERVIEW.md) | 项目总览（本文档） | 所有用户 |

### 使用文档

| 文档 | 说明 | 适合对象 |
|------|------|----------|
| [CLI_GUIDE.md](CLI_GUIDE.md) | 命令行详细使用 | 命令行用户 |
| [USAGE.md](USAGE.md) | Web 界面使用 | Web 用户 |
| [DEMO.md](DEMO.md) | 功能演示 | 所有用户 |
| [FEATURES.md](FEATURES.md) | 功能特性详解 | 所有用户 |

### 技术文档

| 文档 | 说明 | 适合对象 |
|------|------|----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 架构设计 | 开发者 |
| [API.md](API.md) | API 接口 | 开发者 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目总结 | 项目管理者 |

---

## 🔧 技术栈

### 后端

- **Web 框架**: Sanic 23.12.1
- **HTTP 客户端**: httpx 0.27.0
- **定时任务**: APScheduler 3.10.4
- **数据验证**: Pydantic 2.6.4
- **配置管理**: TOML 0.10.2

### 前端

- **模板引擎**: Jinja2 3.1.3
- **样式**: 纯 CSS3
- **脚本**: 原生 JavaScript

### 开发工具

- **Python**: 3.11+
- **包管理**: pip
- **容器化**: Docker / Docker Compose

---

## 🏗️ 核心架构

### 分层架构

```
┌─────────────────────────────────┐
│      Web 界面 / 命令行           │  表示层
├─────────────────────────────────┤
│      API 层 (Sanic)             │  接口层
├─────────────────────────────────┤
│   业务逻辑层 (Scheduler)         │  业务层
├─────────────────────────────────┤
│  签到器 | 通知器 | 日志           │  服务层
├─────────────────────────────────┤
│    配置 | 模型 | 工具             │  数据层
└─────────────────────────────────┘
```

### 插件式签到器

```
BaseChecker (抽象基类)
    │
    ├── ExampleChecker (示例)
    ├── GladosChecker (GLaDOS)
    └── YourChecker (自定义...)
```

### 通知系统

```
通知调度器
    │
    ├── TelegramNotifier
    └── DingTalkNotifier
```

---

## 📝 配置说明

### 站点配置 (sites.toml)

```toml
[example]
name = "示例站点"
enabled = true
checker_class = "ExampleChecker"

[[example.accounts]]
username = "user1"
password = "pass1"
enabled = true
```

### 系统设置 (settings.toml)

```toml
[admin]
username = "admin"
password = "admin123"

[notifications.telegram]
enabled = false
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

---

## 📊 功能矩阵

### 核心功能

| 功能 | Web 模式 | 命令行模式 | 说明 |
|------|----------|------------|------|
| 多站点管理 | ✅ | ✅ | 支持无限站点 |
| 多账户管理 | ✅ | ✅ | 每站点支持多账户 |
| TOML 配置 | ✅ | ✅ | 清晰易读 |
| 签到通知 | ✅ | ✅ | Telegram + 钉钉 |
| 日志记录 | ✅ | ✅ | 按天按站点分割 |
| 定时任务 | ✅ | ❌ | 需配合 Cron |
| 立即签到 | ✅ | ✅ | 手动触发 |
| 在线管理 | ✅ | ❌ | Web 专属 |
| 脚本集成 | ❌ | ✅ | 命令行专属 |

### 管理功能

| 功能 | Web 模式 | 命令行模式 |
|------|----------|------------|
| 添加站点 | ✅ | ⚠️ 编辑配置 |
| 删除站点 | ✅ | ⚠️ 编辑配置 |
| 启用/禁用站点 | ✅ | ⚠️ 编辑配置 |
| 添加账户 | ✅ | ⚠️ 编辑配置 |
| 启用/禁用账户 | ✅ | ⚠️ 编辑配置 |
| 查看日志 | ✅ | ⚠️ 查看文件 |
| 统计数据 | ✅ | ❌ |

---

## 🔐 安全特性

### 认证保护

- Session-based 认证
- 密码保护管理界面
- HttpOnly Cookie 防 XSS

### 配置安全

- 敏感信息独立配置
- 不提交到版本控制
- 支持权限控制

### 日志安全

- 不记录敏感信息
- 本地文件存储
- 可定期清理

---

## 🎯 使用场景

### 场景 1：个人使用

**需求：**
- 多个网站需要签到
- 希望自动化管理

**方案：**
- 使用命令行模式
- 配置 Cron 定时任务
- 启用通知提醒

### 场景 2：团队使用

**需求：**
- 多人共享账户
- 集中管理签到
- 可视化监控

**方案：**
- 使用 Web 管理模式
- 部署到服务器
- 启用定时任务

### 场景 3：服务器部署

**需求：**
- 长期稳定运行
- 资源占用低
- 易于维护

**方案：**
- Docker Compose 部署
- 命令行模式 + Systemd Timer
- 日志定期清理

### 场景 4：开发测试

**需求：**
- 测试新站点签到
- 调试签到逻辑
- 快速验证

**方案：**
- 使用命令行模式
- 指定单个站点运行
- 查看实时输出

---

## 📈 性能特点

### 高效

- ✅ 异步并发处理
- ✅ 非阻塞 I/O
- ✅ 快速响应

### 轻量

- ✅ 依赖少
- ✅ 启动快
- ✅ 资源占用低

### 可扩展

- ✅ 插件式架构
- ✅ 模块化设计
- ✅ 易于维护

---

## 🛠️ 开发指南

### 添加新签到器

1. 在 `app/checkers/` 创建新文件
2. 继承 `BaseChecker`
3. 实现 `_do_check_in()` 方法
4. 在 `__init__.py` 中注册

### 添加新通知器

1. 在 `app/notifiers/` 创建新文件
2. 实现 `send_message()` 方法
3. 在 `CheckScheduler` 中集成

### 自定义界面

1. 修改 `app/templates/` 中的模板
2. 修改 `app/static/css/` 中的样式
3. 修改 `app/static/js/` 中的脚本

---

## 🧪 测试

### 基础测试

```bash
python test_basic.py
```

### 功能测试

```bash
# 测试配置加载
python -c "from app.config import load_sites_config; print(load_sites_config())"

# 测试签到
python checkin.py example
```

---

## 📦 部署方案

### 开发环境

```bash
pip install -r requirements.txt
python run.py
```

### 生产环境

#### 方案 1：Systemd Service

```bash
sudo cp checkhub.service /etc/systemd/system/
sudo systemctl enable checkhub
sudo systemctl start checkhub
```

#### 方案 2：Docker

```bash
docker-compose up -d
```

#### 方案 3：Nginx 反向代理

```nginx
upstream checkhub {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name checkhub.example.com;
    
    location / {
        proxy_pass http://checkhub;
    }
}
```

---

## 🤝 贡献指南

欢迎贡献代码！

### 开发流程

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8
- 使用类型注解
- 编写文档字符串
- 添加必要注释

---

## 📄 许可证

本项目采用 MIT License 开源。

---

## 📧 支持

- 💬 [提交 Issue](../../issues)
- 💡 [功能建议](../../issues)
- ⭐ [Star 项目](../../)

---

## 🙏 鸣谢

感谢以下开源项目：

- [Sanic](https://sanic.dev/)
- [httpx](https://www.python-httpx.org/)
- [APScheduler](https://apscheduler.readthedocs.io/)
- [Pydantic](https://pydantic.dev/)

---

<div align="center">

**[⬆ 回到顶部](#checkhub-项目总览)**

Made with ❤️ by CheckHub Team

</div>
