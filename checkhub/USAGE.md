# CheckHub 使用指南

## 快速开始

### 1. 安装依赖

```bash
cd checkhub
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python run.py
```

或使用启动脚本：

```bash
./start.sh
```

### 3. 访问管理界面

打开浏览器访问: http://localhost:8000

默认登录信息：
- 用户名: `admin`
- 密码: `admin123`

> ⚠️ 首次登录后请立即修改密码！在 `config/settings.toml` 中修改。

## 配置说明

### 系统配置 (config/settings.toml)

```toml
[admin]
username = "admin"           # 管理员用户名
password = "admin123"        # 管理员密码

[notifications.telegram]
enabled = false              # 是否启用 Telegram 通知
bot_token = ""              # Telegram Bot Token
chat_id = ""                # Telegram Chat ID

[notifications.dingtalk]
enabled = false              # 是否启用钉钉通知
webhook = ""                # 钉钉 Webhook URL
secret = ""                 # 钉钉签名密钥

[scheduler]
enabled = true              # 是否启用定时任务
check_time = "08:00"        # 每天签到时间 (HH:MM)
```

### 站点配置 (config/sites.toml)

```toml
[站点ID]
name = "站点名称"
enabled = true              # 是否启用此站点
checker_class = "签到器类名"

[[站点ID.accounts]]
username = "用户名"
password = "密码"
enabled = true              # 是否启用此账户
```

**示例配置：**

```toml
[glados]
name = "GLaDOS"
enabled = true
checker_class = "GladosChecker"

[[glados.accounts]]
username = "user@example.com"
password = "your_password"
enabled = true

[[glados.accounts]]
username = "user2@example.com"
password = "password2"
enabled = true
```

## Web 管理界面使用

### 登录

1. 访问 http://localhost:8000
2. 输入用户名和密码
3. 点击登录

### 仪表板

仪表板显示：
- 总站点数
- 启用站点数
- 总账户数
- 日志文件数
- 站点列表
- 最近日志

可以在仪表板上快速执行签到操作。

### 站点管理

#### 添加站点

1. 点击"添加站点"按钮
2. 填写站点信息：
   - 站点ID: 唯一标识符（英文）
   - 站点名称: 显示名称
   - 签到器类: 使用的签到器类名
3. 点击"添加"

#### 添加账户

1. 在站点卡片中点击"添加账户"
2. 填写账户信息：
   - 用户名
   - 密码
3. 点击"添加"

#### 管理站点

每个站点卡片支持以下操作：
- **立即签到**: 手动触发签到
- **启用/禁用**: 切换站点状态
- **删除**: 删除站点（谨慎操作）

### 查看日志

1. 在仪表板的"最近日志"部分
2. 点击"查看"按钮
3. 在新标签页中查看日志内容

## 开发自定义签到器

### 1. 创建签到器文件

在 `app/checkers/` 目录下创建新文件，例如 `mysite.py`:

```python
import httpx
from .base import BaseChecker, CheckResult


class MySiteChecker(BaseChecker):
    """我的站点签到器"""
    
    async def _do_check_in(self) -> CheckResult:
        try:
            # 发送签到请求
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://mysite.com/api/checkin",
                    headers=self.get_headers(),
                    json={
                        "username": self.username,
                        "password": self.password
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        return CheckResult(
                            success=True,
                            message=f"签到成功! 获得 {data.get('points')} 积分",
                            data=data
                        )
                    else:
                        return CheckResult(
                            success=False,
                            message=f"签到失败: {data.get('message')}"
                        )
                else:
                    return CheckResult(
                        success=False,
                        message=f"请求失败: HTTP {response.status_code}"
                    )
                    
        except Exception as e:
            return CheckResult(
                success=False,
                message=f"签到异常: {str(e)}"
            )
    
    async def login(self) -> bool:
        """可选: 实现登录逻辑"""
        # 如果需要先登录再签到，实现此方法
        return True
```

### 2. 注册签到器

在 `app/checkers/__init__.py` 中注册：

```python
from .mysite import MySiteChecker

CHECKER_REGISTRY = {
    "BaseChecker": BaseChecker,
    "ExampleChecker": ExampleChecker,
    "MySiteChecker": MySiteChecker,  # 添加这行
}
```

### 3. 使用签到器

在站点配置中指定：

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

## 通知配置

### Telegram 通知

#### 1. 创建 Bot

1. 在 Telegram 中找到 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 按提示设置名称
4. 获取 Bot Token

#### 2. 获取 Chat ID

1. 在 Telegram 中找到 @userinfobot
2. 发送任意消息
3. 获取你的 Chat ID

#### 3. 配置

在 `config/settings.toml` 中：

```toml
[notifications.telegram]
enabled = true
bot_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
chat_id = "123456789"
```

### 钉钉通知

#### 1. 创建机器人

1. 打开钉钉群聊
2. 群设置 -> 智能群助手 -> 添加机器人
3. 选择"自定义"
4. 设置机器人名称
5. 安全设置选择"加签"
6. 获取 Webhook URL 和加签密钥

#### 2. 配置

在 `config/settings.toml` 中：

```toml
[notifications.dingtalk]
enabled = true
webhook = "https://oapi.dingtalk.com/robot/send?access_token=xxxxx"
secret = "SECxxxxxxxxxxxxxxxxxxxxx"
```

## 定时任务

定时任务默认启用，每天在设定时间自动执行所有启用站点的签到。

### 修改签到时间

在 `config/settings.toml` 中：

```toml
[scheduler]
enabled = true
check_time = "08:00"  # 修改为你想要的时间（24小时制）
```

### 禁用定时任务

```toml
[scheduler]
enabled = false
```

## Docker 部署

### 使用 Docker Compose

```bash
docker-compose up -d
```

### 使用 Docker

```bash
# 构建镜像
docker build -t checkhub .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  --name checkhub \
  checkhub
```

## 常见问题

### Q: 如何修改管理员密码？

A: 编辑 `config/settings.toml` 文件中的 `[admin]` 部分。

### Q: 签到失败怎么办？

A: 
1. 查看日志文件确认错误信息
2. 检查账户密码是否正确
3. 检查网络连接
4. 确认签到器实现是否正确

### Q: 如何手动触发签到？

A: 
1. 通过 Web 界面点击"立即签到"按钮
2. 或使用 API: `POST /sites/api/check/{site_id}`

### Q: 日志在哪里？

A: 日志存储在 `logs/` 目录：
- `main.log` - 系统日志
- `{site_id}_{date}.log` - 每个站点每天的签到日志

### Q: 如何添加新的签到站点？

A: 参考"开发自定义签到器"部分，创建新的签到器类。

## 安全建议

1. **修改默认密码**: 首次部署后立即修改管理员密码
2. **使用 HTTPS**: 生产环境建议使用反向代理（如 Nginx）并配置 HTTPS
3. **定期备份**: 定期备份 `config/` 目录
4. **限制访问**: 使用防火墙限制管理界面的访问
5. **保护配置文件**: 确保配置文件权限正确，防止泄露

## 高级配置

### 使用环境变量

可以通过环境变量覆盖配置：

```bash
export ADMIN_USERNAME=myadmin
export ADMIN_PASSWORD=mypassword
python run.py
```

### 使用反向代理

Nginx 配置示例：

```nginx
server {
    listen 80;
    server_name checkhub.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
