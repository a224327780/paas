# CheckinHub 安装指南

## 系统要求

- Python 3.8 或更高版本
- pip（Python 包管理器）

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone <repository_url>
cd checkinhub
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置文件

复制示例配置文件并根据需要修改：

```bash
# 复制主配置文件
cp config/config.toml.example config/config.toml

# 复制站点配置文件
cp config/sites.toml.example config/sites.toml
```

编辑配置文件：

```bash
# 编辑主配置
nano config/config.toml

# 编辑站点配置
nano config/sites.toml
```

### 5. 测试运行

```bash
# 查看可用站点
python main.py --list

# 运行示例站点
python main.py example
```

## 配置说明

### 主配置文件 (config/config.toml)

包含日志和通知的配置：

- 日志级别（DEBUG, INFO, WARNING, ERROR）
- Telegram 通知配置
- 钉钉通知配置

### 站点配置文件 (config/sites.toml)

包含各个站点和账户的配置：

- 站点名称
- 启用状态
- 是否发送通知
- 账户列表（用户名、密码、Cookie等）

## 通知配置

### Telegram

1. 与 [@BotFather](https://t.me/BotFather) 对话创建机器人
2. 记录 `bot_token`
3. 与 [@userinfobot](https://t.me/userinfobot) 获取 `chat_id`
4. 在 `config/config.toml` 中配置

### 钉钉

1. 在钉钉群中添加自定义机器人
2. 选择"加签"安全设置
3. 记录 `webhook` URL 和 `secret`
4. 在 `config/config.toml` 中配置

## 定时运行

### 使用 cron (Linux/Mac)

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上 8 点）
0 8 * * * cd /path/to/checkinhub && /path/to/python main.py >> /path/to/logs/cron.log 2>&1
```

### 使用 Task Scheduler (Windows)

1. 打开任务计划程序
2. 创建基本任务
3. 设置触发器（每天特定时间）
4. 操作：启动程序，选择 Python 和 main.py

### 使用 systemd timer (Linux)

创建服务文件 `/etc/systemd/system/checkinhub.service`：

```ini
[Unit]
Description=CheckinHub Service
After=network.target

[Service]
Type=oneshot
User=your_user
WorkingDirectory=/path/to/checkinhub
ExecStart=/path/to/python main.py
```

创建定时器文件 `/etc/systemd/system/checkinhub.timer`：

```ini
[Unit]
Description=CheckinHub Timer

[Timer]
OnCalendar=daily
OnCalendar=08:00
Persistent=true

[Install]
WantedBy=timers.target
```

启用和启动定时器：

```bash
sudo systemctl enable checkinhub.timer
sudo systemctl start checkinhub.timer
```

## 故障排除

### 导入错误

如果遇到模块导入错误，确保：
1. 已激活虚拟环境
2. 已安装所有依赖
3. 在项目根目录运行

### 配置文件错误

确保：
1. TOML 语法正确
2. 配置文件路径正确
3. 配置项完整

### 网络错误

如果签到失败：
1. 检查网络连接
2. 验证账户信息
3. 查看详细日志

## 升级

```bash
# 拉取最新代码
git pull

# 更新依赖
pip install -r requirements.txt --upgrade
```

## 卸载

```bash
# 删除虚拟环境
rm -rf venv

# 删除项目目录
cd ..
rm -rf checkinhub
```
