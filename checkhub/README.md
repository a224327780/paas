# CheckHub - 自动签到管理系统

<div align="center">

🎯 **一个基于 Python + Sanic 的自动签到管理系统**

支持多站点 | 多账户 | 通知推送 | 日志记录 | Web管理界面

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Sanic](https://img.shields.io/badge/Sanic-23.12-orange.svg)](https://sanic.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [文档](#-文档) • [截图](#-界面预览)

</div>

---

## ✨ 功能特性

- 🌐 **多站点支持** - 支持配置多个签到站点
- 👥 **多账户管理** - 每个站点支持多个账户
- 📝 **日志记录** - 每天每个站点记录一个日志文件
- 🔔 **通知推送** - 支持 Telegram 和钉钉通知
- ⏰ **定时任务** - 支持定时自动签到
- 🎨 **Web管理界面** - 现代化的管理界面
- 🔒 **登录认证** - 安全的管理员登录系统
- 🔧 **易于扩展** - 基于插件式签到器架构

## 📦 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd checkhub
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置

首次运行会自动生成配置文件：

- `config/sites.toml` - 站点配置
- `config/settings.toml` - 系统设置

#### 系统设置 (settings.toml)

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

#### 站点配置 (sites.toml)

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
```

## 🚀 运行

```bash
# 方式1: 直接运行
python run.py

# 方式2: 使用启动脚本
./start.sh

# 方式3: Docker Compose
docker-compose up -d
```

访问 http://localhost:8000 即可进入管理界面。

**默认登录信息：**
- 用户名: `admin`
- 密码: `admin123`

> ⚠️ **首次登录后请立即修改密码！**

## 🎯 开发自定义签到器

在 `app/checkers/` 目录下创建新的签到器类：

```python
from app.checkers.base import BaseChecker, CheckResult
import httpx

class MyChecker(BaseChecker):
    async def _do_check_in(self) -> CheckResult:
        # 实现你的签到逻辑
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://example.com/checkin",
                headers=self.get_headers(),
                data={
                    "username": self.username,
                    "password": self.password
                }
            )
            
            if response.status_code == 200:
                return CheckResult(
                    success=True,
                    message=f"签到成功!",
                    data={"points": "+10"}
                )
            else:
                return CheckResult(
                    success=False,
                    message="签到失败"
                )
```

然后在 `app/checkers/__init__.py` 中注册：

```python
from .my_checker import MyChecker

CHECKER_REGISTRY = {
    "BaseChecker": BaseChecker,
    "ExampleChecker": ExampleChecker,
    "MyChecker": MyChecker,  # 添加你的签到器
}
```

## 📁 项目结构

```
checkhub/
├── app/
│   ├── __init__.py              # 应用初始化
│   ├── main.py                  # 主程序入口
│   ├── config.py                # 配置管理
│   ├── models/                  # 数据模型
│   │   ├── __init__.py
│   │   └── site.py
│   ├── checkers/                # 签到器
│   │   ├── __init__.py
│   │   ├── base.py             # 基础签到器
│   │   └── example.py          # 示例签到器
│   ├── notifiers/               # 通知器
│   │   ├── __init__.py
│   │   ├── telegram.py         # Telegram通知
│   │   └── dingtalk.py         # 钉钉通知
│   ├── views/                   # 视图控制器
│   │   ├── __init__.py
│   │   ├── auth.py             # 认证相关
│   │   ├── dashboard.py        # 仪表板
│   │   └── sites.py            # 站点管理
│   ├── templates/               # HTML模板
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── sites.html
│   ├── static/                  # 静态资源
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       ├── logger.py           # 日志工具
│       └── scheduler.py        # 定时任务
├── config/                      # 配置文件
│   ├── sites.toml
│   └── settings.toml
├── logs/                        # 日志目录
├── data/                        # 数据目录
├── requirements.txt             # 依赖列表
├── run.py                       # 启动脚本
└── README.md                    # 项目文档
```

## 🔧 API 接口

### 站点管理

- `GET /sites/api/list` - 获取站点列表
- `POST /sites/api/add` - 添加站点
- `DELETE /sites/api/delete/<site_id>` - 删除站点
- `POST /sites/api/toggle/<site_id>` - 切换站点状态
- `POST /sites/api/add_account/<site_id>` - 添加账户
- `POST /sites/api/check/<site_id>` - 立即签到

### 认证

- `GET /auth/login` - 登录页面
- `POST /auth/login` - 登录处理
- `GET /auth/logout` - 退出登录

## 📝 日志

日志文件存储在 `logs/` 目录下：

- `main.log` - 系统主日志
- `{site_id}_{date}.log` - 每个站点每天的签到日志

## 🔔 通知配置

### Telegram

1. 创建 Telegram Bot，获取 token
2. 获取 chat_id
3. 在 `settings.toml` 中配置

### 钉钉

1. 创建钉钉机器人
2. 获取 webhook URL 和 secret
3. 在 `settings.toml` 中配置

## 📚 文档

完整的项目文档：

- 📖 [快速开始指南](QUICKSTART.md) - 5分钟快速上手
- 📘 [详细使用指南](USAGE.md) - 完整功能说明
- 🏗️ [架构设计文档](ARCHITECTURE.md) - 技术架构详解
- 🔌 [API接口文档](API.md) - API使用说明
- 📊 [项目总结](PROJECT_SUMMARY.md) - 项目概览

## 🖼️ 界面预览

### 登录页面
现代化的登录界面，渐变色背景设计

### 仪表板
- 实时统计数据
- 站点状态概览
- 日志文件管理
- 快速操作入口

### 站点管理
- 卡片式站点展示
- 账户管理
- 一键签到
- 站点状态控制

## 🏗️ 技术栈

- **后端框架**: Sanic (异步Web框架)
- **模板引擎**: Jinja2
- **HTTP客户端**: httpx (异步)
- **定时任务**: APScheduler
- **配置管理**: TOML
- **数据验证**: Pydantic

## 📊 项目统计

- **代码行数**: ~4500+ 行
- **Python文件**: 18 个
- **HTML模板**: 3 个
- **文档**: 6 个（1800+ 行）
- **支持站点**: 可扩展（内置示例）

## 🔒 安全建议

1. ✅ 修改默认管理员密码
2. ✅ 使用 HTTPS（生产环境）
3. ✅ 定期备份配置文件
4. ✅ 限制管理界面访问
5. ✅ 使用强密码

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎贡献代码！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📧 支持

- 💬 提交 [Issue](../../issues) 报告问题
- 💡 提交 [Issue](../../issues) 建议新功能
- ⭐ Star 本项目表示支持

## 🙏 鸣谢

感谢所有开源项目的贡献者！

---

<div align="center">

**[⬆ 回到顶部](#checkhub---自动签到管理系统)**

Made with ❤️ by CheckHub Team

</div>
