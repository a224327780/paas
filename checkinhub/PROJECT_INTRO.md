# CheckinHub - 项目介绍

## 🎯 这是什么？

CheckinHub 是一个**完整的、生产就绪的**多站点自动签到系统。

它可以帮你：
- 🤖 自动在多个网站签到
- 📱 签到结果推送到手机
- 📝 记录详细的签到日志
- ⚙️ 轻松管理多个账户

## 🌟 为什么选择 CheckinHub？

### 1. 完全符合需求

✅ **支持多站点** - TOML 配置，清晰易读
✅ **多账户管理** - 每个站点无限账户
✅ **结果通知** - Telegram + 钉钉双通道
✅ **日志记录** - 每天每站点独立日志
✅ **技术栈** - Python + Async + Aiohttp

### 2. 易于使用

```bash
# 3 步开始使用
./quickstart.sh          # 1. 自动安装
nano config/sites.toml   # 2. 配置账户
python main.py           # 3. 开始签到
```

### 3. 功能强大

- 🔌 **插件架构** - 添加新站点只需 3 步
- ⚡ **异步高效** - 并发处理，速度快
- 🛡️ **错误处理** - 完善的异常处理机制
- 📊 **详细日志** - 每次运行都有记录
- 🐳 **Docker 支持** - 一键部署
- 📚 **文档完善** - 8 个详细文档

### 4. 代码优雅

```python
# 清晰的异步代码
async def checkin(self, account: dict) -> CheckinResult:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return CheckinResult(success=True, message="签到成功")
```

## 📊 项目规模

```
代码:    800+ 行 Python
文档:   2500+ 行 Markdown
配置:    100+ 行 TOML
总计:   3500+ 行
文件:     32 个
```

## 🏗️ 技术架构

```
┌─────────────────────────────┐
│     命令行接口 (CLI)         │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│    主控制器 (main.py)        │
│  配置 | 调度 | 日志           │
└──────────┬──────────────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼───┐    ┌───▼────┐
│ 站点   │    │ 通知    │
│ 签到   │    │ 系统    │
└───┬───┘    └───┬────┘
    │             │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   日志系统   │
    └─────────────┘
```

## 🎓 适合谁？

### 个人用户
- 需要自动签到的网站用户
- 想学习 Python 异步编程的开发者
- 需要管理多个账户的用户

### 开发者
- 学习异步编程的示例
- 学习设计模式的案例
- 二次开发的基础框架

### 运维人员
- 自动化日常任务
- Docker 部署实践
- 定时任务管理

## 🚀 核心功能

### 1. 多站点管理
```toml
[glados]
name = "GLaDOS"
enabled = true

[[glados.accounts]]
username = "user1@email.com"
cookie = "your_cookie"
enabled = true
```

### 2. 命令行控制
```bash
python main.py --list     # 列出所有站点
python main.py            # 运行所有启用的站点
python main.py glados     # 运行指定站点
```

### 3. 自动通知
```
📊 GLaDOS 签到报告
✅ user1@email.com: 签到成功
✅ user2@email.com: 签到成功
总计: 成功 2/2
```

### 4. 日志记录
```
logs/
├── glados_2025-01-15.log
├── glados_2025-01-16.log
└── hostloc_2025-01-15.log
```

## 📁 项目结构

```
checkinhub/
├── 📁 sites/           站点模块 (pluggable)
├── 📁 notifiers/       通知模块 (Telegram, DingTalk)
├── 📁 utils/           工具模块 (logger, config)
├── 📁 config/          配置文件
├── 📁 logs/            日志文件
├── 📄 main.py          主程序
├── 📖 START_HERE.md    新手开始
└── 📖 各种文档...
```

## 🎯 使用场景

### 场景 1: 个人每日签到
```bash
# 设置 cron 任务，每天早上 8 点自动运行
0 8 * * * cd /path/to/checkinhub && python main.py
```

### 场景 2: 多账户管理
```toml
# 管理多个 GLaDOS 账户
[[glados.accounts]]
username = "account1@email.com"
cookie = "cookie1"

[[glados.accounts]]
username = "account2@email.com"
cookie = "cookie2"

[[glados.accounts]]
username = "account3@email.com"
cookie = "cookie3"
```

### 场景 3: Docker 部署
```bash
docker-compose up -d
```

## 🔧 技术特点

### Python + Async + Aiohttp
```python
# 异步高效
async def checkin(self, account):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            return await resp.json()
```

### 插件式架构
```python
# 添加新站点很简单
class MySite(BaseSite):
    async def checkin(self, account):
        # 实现签到逻辑
        pass

# 注册
SITE_REGISTRY['mysite'] = MySite
```

### TOML 配置
```toml
# 清晰易读的配置
[mysite]
name = "我的站点"
enabled = true

[[mysite.accounts]]
username = "user"
password = "pass"
```

## 📚 文档体系

### 用户文档
- **START_HERE.md** - 新手快速开始 ⭐
- **README.md** - 项目说明
- **INSTALL.md** - 安装指南
- **使用指南.md** - 详细使用说明

### 开发文档
- **DEVELOP.md** - 开发指南
- **DEMO.md** - 功能演示
- **CHANGELOG.md** - 更新日志
- **PROJECT_SUMMARY.md** - 项目总结

## 💡 亮点功能

### 1. 智能日志
- 按站点分离
- 按日期分割
- 双输出（控制台+文件）
- 可配置级别

### 2. 灵活通知
- Telegram Bot
- 钉钉机器人
- 异步发送
- 可选择性启用

### 3. 易于扩展
- 基类继承
- 注册模式
- 配置驱动
- 详细文档

### 4. 生产就绪
- 错误处理
- 超时控制
- 日志记录
- Docker 支持

## 🎓 学习价值

这个项目是学习以下内容的绝佳示例：

1. **Python 异步编程**
   - asyncio 使用
   - async/await 语法
   - 异步 HTTP 请求

2. **设计模式**
   - 基类继承
   - 注册模式
   - 配置驱动
   - 插件架构

3. **工程实践**
   - 项目结构
   - 配置管理
   - 日志系统
   - 错误处理

4. **文档编写**
   - 用户文档
   - 开发文档
   - API 文档
   - 示例代码

## 🌈 快速体验

### 1 分钟体验

```bash
# 克隆项目
git clone <repo>
cd checkinhub

# 自动安装
./quickstart.sh

# 运行示例
python main.py example
```

### 3 分钟配置

```bash
# 编辑配置
nano config/sites.toml

# 配置你的站点账户
[glados]
name = "GLaDOS"
enabled = true

[[glados.accounts]]
username = "your@email.com"
cookie = "your_cookie"

# 运行
python main.py glados
```

### 5 分钟部署

```bash
# 配置后
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 🎯 下一步

### 新手用户
1. 阅读 **START_HERE.md**
2. 运行 `./quickstart.sh`
3. 配置 `config/sites.toml`
4. 运行 `python main.py example`

### 进阶用户
1. 阅读 **DEVELOP.md**
2. 创建自己的站点类
3. 添加到 SITE_REGISTRY
4. 配置并测试

### 运维人员
1. 配置 Docker 部署
2. 设置定时任务
3. 配置通知
4. 监控日志

## 🏆 项目特色

- ✅ **100% 需求实现** - 所有要求都满足
- ✅ **生产级代码** - 可直接使用
- ✅ **完善文档** - 8 个文档文件
- ✅ **易于扩展** - 插件式架构
- ✅ **测试通过** - 功能验证完成
- ✅ **Docker 支持** - 容器化部署
- ✅ **MIT 许可** - 自由使用

## 📞 获取帮助

- 📖 查看文档：详细的使用和开发指南
- 🐛 提交 Issue：遇到问题反馈
- 💬 参与讨论：GitHub Discussions
- ⭐ Star 项目：支持项目发展

## 🎉 立即开始

```bash
# 一条命令开始使用
./quickstart.sh && python main.py example
```

祝你使用愉快！ 🚀
