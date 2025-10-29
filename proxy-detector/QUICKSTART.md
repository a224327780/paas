# Proxy Detector - 快速入门指南

## 5 分钟快速开始

### 1. 安装依赖

```bash
cd proxy-detector
pip install -r requirements.txt
```

### 2. 准备代理列表

创建 `proxies.txt` 文件：

```bash
# 复制示例文件
cp examples/proxies.txt ./proxies.txt

# 或手动创建
cat > proxies.txt << EOF
http://proxy1.example.com:8080
https://proxy2.example.com:8443
socks5://user:pass@proxy3.example.com:1080
EOF
```

### 3. 运行检测

```bash
# 运行一次检测
python main.py --once
```

### 4. 查看结果

```bash
# 查看可用的代理
cat output/working_proxies.txt

# 查看统计信息
cat output/statistics.json

# 查看日志
tail -f logs/proxy_detector.log
```

## 完整安装指南

### 方式 1: 本地安装

#### 系统要求
- Python 3.8 或更高版本
- pip 包管理器

#### 安装步骤

```bash
# 1. 克隆或下载项目
cd proxy-detector

# 2. (推荐) 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. (可选) 下载 Mihomo 二进制文件
# 用于支持 SS, SSR, VMess, VLESS, Trojan, Hysteria 协议

# Linux x64
wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64 -O mihomo
chmod +x mihomo

# macOS x64
wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-darwin-amd64 -O mihomo
chmod +x mihomo

# Windows x64 (PowerShell)
Invoke-WebRequest -Uri "https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-windows-amd64.exe" -OutFile "mihomo.exe"
```

### 方式 2: Docker 安装

```bash
# 构建镜像
docker build -t proxy-detector .

# 运行容器
docker run -d \
  --name proxy-detector \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/proxies.txt:/app/proxies.txt:ro \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  proxy-detector

# 查看日志
docker logs -f proxy-detector
```

### 方式 3: Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 基本配置

编辑 `config/config.yaml`:

```yaml
# 最小配置
data_sources:
  - type: file
    enabled: true
    path: ./proxies.txt
    format: line

detection:
  timeout: 10
  concurrent_tasks: 50

mihomo:
  enabled: false  # 如果只测试 HTTP/HTTPS/SOCKS5，设为 false

logging:
  level: INFO

output:
  save_working: true
  working_proxies_file: ./output/working_proxies.txt
```

## 使用示例

### 示例 1: 一次性检测

```bash
python main.py --once
```

输出:
```
============================================================
Proxy Detector - Multi-protocol proxy detection
Supported protocols: HTTP, HTTPS, SOCKS5, SS, SSR, VMESS, VLESS, TROJAN, Hysteria, Hysteria2
============================================================
2024-01-01 12:00:00 | INFO     | Initializing Proxy Detector...
2024-01-01 12:00:00 | INFO     | Loaded 100 proxies from file
2024-01-01 12:00:00 | INFO     | Starting proxy detection...
2024-01-01 12:00:05 | INFO     | ✓ http://proxy1.com:8080 - Latency: 145.23ms
2024-01-01 12:00:05 | INFO     | ✓ socks5://proxy2.com:1080 - Latency: 89.45ms
...
============================================================
Detection Statistics:
Total Proxies: 100
Working: 45
Failed: 55
Success Rate: 45.00%

By Protocol:
  HTTP: 20/30 working
  SOCKS5: 15/25 working
  SS: 5/20 working
  VMESS: 5/25 working
============================================================
```

### 示例 2: 持续检测模式

```bash
# 使用默认间隔 (300秒)
python main.py

# 自定义间隔 (每小时检测一次)
python main.py --interval 3600
```

### 示例 3: 使用自定义配置文件

```bash
python main.py --config /path/to/custom-config.yaml --once
```

### 示例 4: 从 URL 获取代理列表

修改 `config/config.yaml`:

```yaml
data_sources:
  - type: url
    enabled: true
    url: https://raw.githubusercontent.com/user/repo/main/proxies.txt
    interval: 3600
    format: line
```

### 示例 5: 高并发检测

适用于大量代理的场景:

```yaml
detection:
  timeout: 5
  concurrent_tasks: 200
  retry_attempts: 1
```

```bash
python main.py --once
```

## 代理列表格式

### 格式 1: 行格式 (推荐)

`proxies.txt`:
```
# HTTP 代理
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:8080

# HTTPS 代理
https://proxy3.example.com:8443

# SOCKS5 代理
socks5://proxy4.example.com:1080
socks5://user:pass@proxy5.example.com:1080

# Shadowsocks
ss://aes-256-gcm:password@ss.example.com:8388

# VMess (Base64 编码的配置)
vmess://eyJ2IjoiMiIsInBzIjoidGVzdCIsImFkZCI6ImV4YW1wbGUuY29tIiwicG9ydCI6IjQ0MyIsImlkIjoiMTIzNDU2NzgtYWJjZC0xMjM0LWFiY2QtMTIzNDU2Nzg5YWJjIiwiYWlkIjoiMCIsIm5ldCI6IndzIiwidHlwZSI6Im5vbmUiLCJob3N0IjoiZXhhbXBsZS5jb20iLCJwYXRoIjoiL3BhdGgiLCJ0bHMiOiJ0bHMifQ==

# Trojan
trojan://password@trojan.example.com:443

# Hysteria2
hysteria2://password@hy2.example.com:443
```

### 格式 2: JSON 格式

`proxies.json`:
```json
[
  {
    "protocol": "http",
    "host": "proxy1.com",
    "port": 8080
  },
  {
    "protocol": "socks5",
    "host": "proxy2.com",
    "port": 1080,
    "username": "user",
    "password": "pass"
  }
]
```

配置:
```yaml
data_sources:
  - type: file
    enabled: true
    path: ./proxies.json
    format: json
```

### 格式 3: YAML 格式

`proxies.yaml`:
```yaml
proxies:
  - protocol: http
    host: proxy1.com
    port: 8080
  - protocol: socks5
    host: proxy2.com
    port: 1080
    username: user
    password: pass
```

配置:
```yaml
data_sources:
  - type: file
    enabled: true
    path: ./proxies.yaml
    format: yaml
```

## 查看结果

### 可用的代理

`output/working_proxies.txt`:
```
http://proxy1.example.com:8080 # Latency: 145.23ms
socks5://proxy2.example.com:1080 # Latency: 89.45ms
ss://aes-256-gcm:password@ss.example.com:8388 # Latency: 234.67ms
```

### 失败的代理

`output/failed_proxies.txt`:
```
http://bad-proxy.example.com:8080 # Error: Timeout
socks5://dead-proxy.example.com:1080 # Error: Connection refused
```

### 统计信息

`output/statistics.json`:
```json
{
  "total": 100,
  "working": 45,
  "failed": 55,
  "by_protocol": {
    "http": {
      "total": 30,
      "working": 20,
      "failed": 10
    },
    "socks5": {
      "total": 25,
      "working": 15,
      "failed": 10
    },
    "ss": {
      "total": 20,
      "working": 5,
      "failed": 15
    },
    "vmess": {
      "total": 25,
      "working": 5,
      "failed": 20
    }
  },
  "start_time": "2024-01-01T12:00:00.123456",
  "end_time": "2024-01-01T12:05:30.789012"
}
```

## 常见问题

### Q1: 为什么所有代理都显示超时？

**A**: 可能的原因：
1. 网络连接问题
2. 超时设置太短
3. 代理确实不可用

**解决方案**:
```yaml
detection:
  timeout: 20  # 增加超时时间
  concurrent_tasks: 20  # 减少并发数
```

### Q2: Mihomo 协议不工作？

**A**: 确保：
1. 已下载 Mihomo 二进制文件
2. 文件有执行权限
3. 配置文件中 `mihomo.enabled: true`

```bash
# 检查 Mihomo
ls -l mihomo
chmod +x mihomo
./mihomo -v
```

### Q3: 如何只测试特定协议？

**A**: 从代理列表中只包含需要测试的协议，或者禁用 Mihomo:

```yaml
mihomo:
  enabled: false  # 只测试 HTTP/HTTPS/SOCKS5
```

### Q4: 如何提高检测速度？

**A**: 调整这些参数：

```yaml
detection:
  timeout: 5              # 减少超时
  concurrent_tasks: 200   # 增加并发
  retry_attempts: 1       # 减少重试
```

### Q5: 内存占用太高？

**A**: 减少并发数和批处理大小：

```yaml
detection:
  concurrent_tasks: 20    # 降低并发
```

## 定时任务

### Linux/Mac (Cron)

```bash
# 每小时运行一次
0 * * * * cd /path/to/proxy-detector && python main.py --once >> /tmp/proxy-detector.log 2>&1

# 每 6 小时运行一次
0 */6 * * * cd /path/to/proxy-detector && python main.py --once
```

### Windows (Task Scheduler)

1. 打开任务计划程序
2. 创建基本任务
3. 触发器：每小时
4. 操作：启动程序
   - 程序：`python`
   - 参数：`main.py --once`
   - 起始于：`C:\path\to\proxy-detector`

### Systemd 服务 (Linux)

创建 `/etc/systemd/system/proxy-detector.service`:

```ini
[Unit]
Description=Proxy Detector Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/proxy-detector
ExecStart=/usr/bin/python3 main.py --interval 3600
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable proxy-detector
sudo systemctl start proxy-detector
sudo systemctl status proxy-detector
```

## 下一步

- 阅读 [项目架构文档](ARCHITECTURE.md) 了解详细设计
- 阅读 [项目概览](PROJECT_OVERVIEW.md) 了解完整功能
- 查看 [示例目录](examples/) 获取更多用法
- 自定义配置以满足你的需求

## 获取帮助

```bash
python main.py --help
```

## 许可证

详见 LICENSE 文件。
