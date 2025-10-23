# CheckHub 架构设计文档

## 项目概述

CheckHub 是一个基于 Python + Sanic 的自动签到管理系统，采用模块化设计，支持多站点、多账户管理。

## 技术栈

- **Web框架**: Sanic (异步 Web 框架)
- **模板引擎**: Jinja2
- **HTTP客户端**: httpx (支持异步)
- **定时任务**: APScheduler
- **配置管理**: TOML
- **数据验证**: Pydantic

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Web 界面                              │
│  (登录、仪表板、站点管理、日志查看)                           │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                    API 层 (Sanic Views)                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │  Auth   │  │Dashboard│  │  Sites  │                      │
│  └─────────┘  └─────────┘  └─────────┘                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                  业务逻辑层                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Scheduler  │  │   Checkers   │  │  Notifiers   │      │
│  │  (定时任务)   │  │  (签到器)     │  │  (通知器)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                  数据层                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Config    │  │     Logs     │  │    Models    │      │
│  │   (TOML)     │  │   (Files)    │  │  (Pydantic)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────────────────────────────────────────┘
```

## 核心模块

### 1. 配置管理 (app/config.py)

负责加载和保存 TOML 配置文件：

- `sites.toml`: 站点和账户配置
- `settings.toml`: 系统设置（管理员、通知、定时任务）

**核心函数：**
- `load_sites_config()`: 加载站点配置
- `save_sites_config()`: 保存站点配置
- `load_settings()`: 加载系统设置
- `save_settings()`: 保存系统设置

### 2. 数据模型 (app/models/)

使用 Pydantic 进行数据验证和序列化：

**Account 模型：**
```python
class Account(BaseModel):
    username: str
    password: str
    enabled: bool = True
    cookies: Optional[str] = None
    extra_data: Optional[dict] = None
```

**Site 模型：**
```python
class Site(BaseModel):
    id: str
    name: str
    enabled: bool = True
    checker_class: str
    accounts: List[Account] = []
    config: Optional[dict] = None
```

### 3. 签到器 (app/checkers/)

采用插件式架构，每个站点实现独立的签到器。

**基类 BaseChecker：**
```python
class BaseChecker:
    async def check_in(self) -> CheckResult
    async def _do_check_in(self) -> CheckResult  # 子类实现
    async def login(self) -> bool
    def get_headers(self) -> Dict[str, str]
```

**签到结果 CheckResult：**
```python
class CheckResult:
    success: bool
    message: str
    data: Dict
    timestamp: datetime
```

**实现新签到器：**
1. 继承 `BaseChecker`
2. 实现 `_do_check_in()` 方法
3. 在 `CHECKER_REGISTRY` 中注册

### 4. 通知器 (app/notifiers/)

支持多种通知方式：

**TelegramNotifier：**
- 通过 Telegram Bot API 发送消息
- 支持 HTML 格式

**DingTalkNotifier：**
- 通过钉钉 Webhook 发送消息
- 支持加签验证

**通知内容：**
- 签到成功/失败统计
- 每个账户的签到结果
- 时间戳

### 5. 定时任务 (app/utils/scheduler.py)

使用 APScheduler 实现定时签到：

**CheckScheduler：**
- `start()`: 启动定时任务
- `stop()`: 停止定时任务
- `run_all_checks()`: 执行所有站点签到
- `check_site()`: 签到单个站点

**执行流程：**
1. 加载站点配置
2. 遍历所有启用的站点
3. 对每个账户执行签到
4. 记录日志
5. 发送通知

### 6. 日志系统 (app/utils/logger.py)

分层日志记录：

**日志文件：**
- `main.log`: 系统主日志（定时任务启动/停止等）
- `{site_id}_{date}.log`: 每个站点每天的签到日志

**日志级别：**
- INFO: 正常操作
- ERROR: 错误信息

**日志格式：**
```
2024-01-01 08:00:00 - checkhub.example - INFO - 开始签到: 示例站点
```

### 7. Web 视图 (app/views/)

**auth.py - 认证模块：**
- 登录/登出
- Session 管理
- 认证装饰器 `@require_auth`

**dashboard.py - 仪表板：**
- 显示系统概览
- 站点统计
- 日志列表
- 查看日志内容

**sites.py - 站点管理：**
- 站点列表
- 添加/删除站点
- 启用/禁用站点
- 添加账户
- 立即签到

### 8. 前端界面 (app/templates/ & app/static/)

**模板文件：**
- `login.html`: 登录页面
- `dashboard.html`: 仪表板
- `sites.html`: 站点管理

**样式设计：**
- 现代化 UI
- 响应式布局
- 卡片式设计
- 模态对话框

**交互功能：**
- AJAX 请求
- 实时更新
- 表单验证

## 数据流

### 签到流程

```
1. 定时触发 / 手动触发
        ↓
2. CheckScheduler.check_site()
        ↓
3. 遍历站点账户
        ↓
4. 创建签到器实例 (根据 checker_class)
        ↓
5. 执行 checker.check_in()
        ↓
6. 返回 CheckResult
        ↓
7. 记录日志 (每个站点一个文件)
        ↓
8. 发送通知 (Telegram/钉钉)
```

### API 请求流程

```
1. 浏览器发送 HTTP 请求
        ↓
2. Sanic 路由匹配
        ↓
3. 认证检查 (@require_auth)
        ↓
4. 视图函数处理
        ↓
5. 调用业务逻辑
        ↓
6. 返回 JSON/HTML 响应
        ↓
7. 前端更新界面
```

## 安全设计

### 1. 认证机制

- Session-based 认证
- Cookie 存储 session_id
- HttpOnly Cookie 防止 XSS

### 2. 密码存储

- 明文存储在配置文件中
- 建议：生产环境使用加密存储

### 3. CSRF 防护

- 当前版本未实现
- 建议：生产环境添加 CSRF Token

### 4. 访问控制

- 所有管理接口需要登录
- 使用 `@require_auth` 装饰器

## 扩展性

### 添加新签到器

1. 在 `app/checkers/` 创建新文件
2. 继承 `BaseChecker`
3. 实现签到逻辑
4. 在 `CHECKER_REGISTRY` 注册

### 添加新通知方式

1. 在 `app/notifiers/` 创建新文件
2. 实现 `send_message()` 方法
3. 在 `CheckScheduler` 中集成

### 添加新功能页面

1. 在 `app/views/` 创建新蓝图
2. 创建对应模板
3. 在 `app/__init__.py` 注册

## 性能优化

### 1. 异步处理

- 所有 HTTP 请求使用 httpx 异步客户端
- 签到任务并发执行
- 减少阻塞时间

### 2. 配置缓存

- 配置文件按需加载
- 避免频繁磁盘 I/O

### 3. 日志优化

- 按天分割日志文件
- 避免单个日志文件过大

## 部署方案

### 1. 直接运行

```bash
python run.py
```

### 2. Docker 部署

```bash
docker-compose up -d
```

### 3. 系统服务 (Systemd)

```ini
[Unit]
Description=CheckHub Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/checkhub
ExecStart=/usr/bin/python3 run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. 反向代理 (Nginx)

```nginx
upstream checkhub {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name checkhub.example.com;

    location / {
        proxy_pass http://checkhub;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 监控与维护

### 1. 日志监控

- 定期检查日志文件
- 关注签到失败记录

### 2. 配置备份

- 定期备份 `config/` 目录
- 版本控制管理

### 3. 系统监控

- 监控进程状态
- 监控磁盘空间
- 监控网络连接

## 未来规划

### 短期计划

- [ ] 添加更多站点签到器
- [ ] 支持更多通知方式（邮件、微信等）
- [ ] 增加账户管理功能（编辑、禁用）
- [ ] 添加签到历史记录

### 中期计划

- [ ] 数据库支持（SQLite/PostgreSQL）
- [ ] 多用户支持
- [ ] RBAC 权限管理
- [ ] API 文档（Swagger）

### 长期计划

- [ ] 插件市场
- [ ] 可视化报表
- [ ] 移动端适配
- [ ] Docker 一键部署

## 贡献指南

欢迎贡献代码！请遵循以下规范：

1. **代码风格**: PEP 8
2. **提交信息**: 清晰描述改动
3. **测试**: 确保功能正常
4. **文档**: 更新相关文档

## 许可证

MIT License
