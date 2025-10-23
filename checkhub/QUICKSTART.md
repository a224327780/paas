# CheckHub 快速开始指南

## 5分钟快速上手

### 方法一：使用安装脚本（推荐）

```bash
# 1. 进入项目目录
cd checkhub

# 2. 运行安装脚本
./install.sh

# 3. 启动应用
python run.py
```

### 方法二：手动安装

```bash
# 1. 进入项目目录
cd checkhub

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python run.py
```

### 方法三：Docker（最简单）

```bash
# 方式1: Docker Compose
docker-compose up -d

# 方式2: Docker
docker build -t checkhub .
docker run -p 8000:8000 checkhub
```

---

## 访问应用

启动成功后，访问: **http://localhost:8000**

### 默认登录信息

- **用户名**: `admin`
- **密码**: `admin123`

> ⚠️ **重要**: 首次登录后请立即修改密码！

---

## 第一次使用

### 1. 登录系统

打开浏览器，访问 http://localhost:8000，输入默认用户名和密码登录。

### 2. 添加站点

1. 点击顶部导航的 **"站点管理"**
2. 点击 **"+ 添加站点"** 按钮
3. 填写站点信息：
   - **站点ID**: `mysite`（英文标识）
   - **站点名称**: `我的站点`
   - **签到器类**: `ExampleChecker`（使用示例签到器）
4. 点击 **"添加"**

### 3. 添加账户

1. 在站点卡片中找到刚添加的站点
2. 点击 **"添加账户"** 按钮
3. 填写账户信息：
   - **用户名**: `user1`
   - **密码**: `pass1`
4. 点击 **"添加"**

### 4. 立即签到

1. 在站点卡片中点击 **"立即签到"** 按钮
2. 等待签到完成
3. 查看签到结果

### 5. 查看日志

1. 返回 **"仪表板"**
2. 在 **"最近日志"** 部分
3. 点击日志文件的 **"查看"** 按钮

---

## 配置说明

### 修改管理员密码

编辑文件: `config/settings.toml`

```toml
[admin]
username = "admin"
password = "your-new-password"  # 修改这里
```

重启应用生效。

### 配置定时任务

编辑文件: `config/settings.toml`

```toml
[scheduler]
enabled = true          # 是否启用定时任务
check_time = "08:00"    # 每天签到时间（24小时制）
```

### 配置Telegram通知

编辑文件: `config/settings.toml`

```toml
[notifications.telegram]
enabled = true                                    # 启用通知
bot_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
chat_id = "123456789"
```

### 配置钉钉通知

编辑文件: `config/settings.toml`

```toml
[notifications.dingtalk]
enabled = true                                          # 启用通知
webhook = "https://oapi.dingtalk.com/robot/send?access_token=xxxxx"
secret = "SECxxxxxxxxxxxxxxxxxxxxx"
```

---

## 添加真实站点

### 示例：GLaDOS站点

1. **编辑配置文件**: `config/sites.toml`

```toml
[glados]
name = "GLaDOS"
enabled = true
checker_class = "GladosChecker"

[[glados.accounts]]
username = "your-email@example.com"
password = "your-password"
enabled = true
```

2. **重启应用**

```bash
# 停止应用（Ctrl+C）
# 重新启动
python run.py
```

3. **手动签到测试**

在Web界面找到GLaDOS站点，点击"立即签到"测试。

---

## 开发新签到器

### 1. 创建签到器文件

创建文件: `app/checkers/mysite.py`

```python
import httpx
from .base import BaseChecker, CheckResult


class MySiteChecker(BaseChecker):
    """我的站点签到器"""
    
    async def _do_check_in(self) -> CheckResult:
        # 实现签到逻辑
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://mysite.com/api/checkin",
                json={
                    "username": self.username,
                    "password": self.password
                }
            )
            
            if response.status_code == 200:
                return CheckResult(
                    success=True,
                    message="签到成功!"
                )
            else:
                return CheckResult(
                    success=False,
                    message="签到失败"
                )
```

### 2. 注册签到器

编辑文件: `app/checkers/__init__.py`

```python
from .mysite import MySiteChecker

CHECKER_REGISTRY = {
    "BaseChecker": BaseChecker,
    "ExampleChecker": ExampleChecker,
    "GladosChecker": GladosChecker,
    "MySiteChecker": MySiteChecker,  # 添加这行
}
```

### 3. 配置站点

编辑文件: `config/sites.toml`

```toml
[mysite]
name = "我的站点"
enabled = true
checker_class = "MySiteChecker"

[[mysite.accounts]]
username = "user"
password = "pass"
enabled = true
```

### 4. 重启并测试

```bash
# 重启应用
python run.py

# 在Web界面测试签到
```

---

## 常见问题

### Q1: 安装依赖失败

**解决方法**:

```bash
# 升级pip
pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

### Q2: 端口被占用

**解决方法**:

修改 `run.py`，更改端口：

```python
app.run(
    host="0.0.0.0",
    port=8001,  # 改成其他端口
    debug=True
)
```

### Q3: 签到失败

**排查步骤**:

1. 检查网络连接
2. 查看日志文件（`logs/` 目录）
3. 确认账户密码正确
4. 检查签到器实现

### Q4: 通知不生效

**排查步骤**:

1. 确认 `enabled = true`
2. 检查 token/webhook 配置
3. 测试网络连通性
4. 查看系统日志

### Q5: 找不到签到器

**解决方法**:

确认签到器已注册：

```python
# 在 app/checkers/__init__.py 中
from .your_checker import YourChecker

CHECKER_REGISTRY = {
    # ...
    "YourChecker": YourChecker,
}
```

---

## 性能优化

### 1. 日志清理

定期清理旧日志：

```bash
# 删除7天前的日志
find logs/ -name "*.log" -mtime +7 -delete
```

### 2. 配置文件备份

定期备份配置：

```bash
cp -r config/ config_backup_$(date +%Y%m%d)/
```

### 3. 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name checkhub.example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 高级用法

### 1. 使用环境变量

```bash
export ADMIN_USERNAME=myadmin
export ADMIN_PASSWORD=mypassword
python run.py
```

### 2. 系统服务（Systemd）

创建文件: `/etc/systemd/system/checkhub.service`

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

启用服务：

```bash
sudo systemctl enable checkhub
sudo systemctl start checkhub
sudo systemctl status checkhub
```

### 3. 定时备份

创建备份脚本: `backup.sh`

```bash
#!/bin/bash
BACKUP_DIR="/backup/checkhub"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config/
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# 保留最近7天的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

添加到crontab：

```bash
# 每天凌晨2点备份
0 2 * * * /path/to/backup.sh
```

---

## 更多资源

- 📖 [完整使用指南](USAGE.md)
- 🏗️ [架构设计文档](ARCHITECTURE.md)
- 🔌 [API文档](API.md)
- 📊 [项目总结](PROJECT_SUMMARY.md)

---

## 获取帮助

- 查看文档
- 提交Issue
- 加入讨论

---

**祝你使用愉快！** 🎉
