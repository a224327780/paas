# Proxy Detector - 技术规格文档

## 1. 项目概述

### 1.1 项目名称
Proxy Detector - 多协议代理检测工具

### 1.2 技术栈
- **编程语言**: Python 3.8+
- **核心框架**: aiohttp (异步 HTTP 客户端)
- **协议转换**: Mihomo 内核

### 1.3 核心依赖
```
aiohttp==3.9.1          # 异步 HTTP 客户端
aiofiles==23.2.1         # 异步文件操作
pyyaml==6.0.1            # YAML 解析
python-socks[asyncio]==2.4.3  # SOCKS5 支持
loguru==0.7.2            # 日志记录
pydantic==2.5.2          # 数据验证
pydantic-settings==2.1.0 # 配置管理
```

## 2. 支持的协议

### 2.1 直接支持的协议

#### HTTP/HTTPS
- **RFC 标准**: RFC 2616, RFC 7230-7237
- **认证方式**: Basic Auth
- **实现方式**: aiohttp 原生支持
- **测试方法**: 直接通过代理发送 HTTP 请求

#### SOCKS5
- **RFC 标准**: RFC 1928
- **认证方式**: Username/Password (RFC 1929)
- **实现方式**: python-socks 库
- **测试方法**: SOCKS5 隧道 + HTTP 请求

### 2.2 Mihomo 支持的协议

#### Shadowsocks (SS)
- **加密方法**: 
  - aes-128-gcm
  - aes-192-gcm
  - aes-256-gcm
  - chacha20-ietf-poly1305
  - xchacha20-ietf-poly1305
- **配置格式**: `ss://METHOD:PASSWORD@HOST:PORT`
- **转换方式**: Mihomo → HTTP Proxy

#### ShadowsocksR (SSR)
- **加密方法**: 
  - aes-256-cfb
  - aes-128-cfb
  - chacha20
- **协议插件**: origin, verify_sha1, auth_sha1_v4
- **混淆插件**: plain, http_simple, tls1.2_ticket_auth
- **转换方式**: Mihomo → HTTP Proxy

#### VMess
- **UUID**: RFC 4122 UUID v4
- **加密方法**: auto, aes-128-gcm, chacha20-poly1305, none
- **传输协议**: TCP, WebSocket, HTTP/2, QUIC
- **配置格式**: Base64 编码的 JSON
- **转换方式**: Mihomo → HTTP Proxy

#### VLESS
- **UUID**: RFC 4122 UUID v4
- **加密**: 无加密 (依赖 TLS)
- **传输协议**: TCP, WebSocket, gRPC
- **配置格式**: vless:// URL scheme
- **转换方式**: Mihomo → HTTP Proxy

#### Trojan
- **加密**: TLS 1.2+
- **认证**: Password-based
- **端口**: 通常使用 443
- **配置格式**: `trojan://PASSWORD@HOST:PORT`
- **转换方式**: Mihomo → HTTP Proxy

#### Hysteria
- **基于**: QUIC (RFC 9000)
- **加密**: TLS 1.3
- **拥塞控制**: BBR
- **认证**: 字符串认证
- **转换方式**: Mihomo → HTTP Proxy

#### Hysteria2
- **基于**: QUIC (RFC 9000)
- **改进**: 
  - 简化握手
  - 改进拥塞控制
  - 更好的性能
- **转换方式**: Mihomo → HTTP Proxy

## 3. 架构设计

### 3.1 模块结构

```
proxy-detector/
│
├── core/                      # 核心模块
│   └── detector.py           # 主检测器
│       ├── ProxyDetector     # 检测器类
│       │   ├── initialize()  # 初始化
│       │   ├── fetch_all_proxies()  # 获取代理
│       │   ├── detect_proxy()       # 检测单个代理
│       │   └── run_detection()      # 运行检测周期
│
├── protocols/                 # 协议处理模块
│   ├── http_handler.py       # HTTP/HTTPS/SOCKS5 处理器
│   │   └── HttpProtocolHandler
│   │       ├── test_proxy()  # 测试代理
│   │       ├── _test_http_proxy()
│   │       └── _test_socks5_proxy()
│   │
│   └── mihomo_handler.py     # Mihomo 协议处理器
│       └── MihomoProtocolHandler
│           ├── start()       # 启动处理器
│           ├── stop()        # 停止处理器
│           ├── test_proxy()  # 测试代理
│           ├── _generate_mihomo_config()
│           ├── _convert_to_mihomo_format()
│           └── _test_through_mihomo()
│
├── data_sources/              # 数据源模块
│   ├── base.py               # 基类
│   │   ├── ProxyInfo         # 代理信息模型
│   │   └── DataSource        # 数据源基类
│   │
│   ├── file_source.py        # 文件数据源
│   │   └── FileDataSource
│   │       ├── fetch_proxies()
│   │       └── _parse_proxy_string()
│   │
│   ├── url_source.py         # URL 数据源
│   │   └── UrlDataSource
│   │       └── fetch_proxies()
│   │
│   └── api_source.py         # API 数据源
│       └── ApiDataSource
│           └── fetch_proxies()
│
└── utils/                     # 工具模块
    ├── config_loader.py      # 配置加载器
    │   └── ConfigLoader
    │       └── load_config()
    │
    └── logger.py             # 日志工具
        └── Logger
            └── setup_logger()
```

### 3.2 类关系图

```
┌─────────────────────┐
│   ProxyDetector     │
│   (core/detector)   │
└──────────┬──────────┘
           │
           ├──────────────────────────────────┐
           │                                  │
           ▼                                  ▼
┌──────────────────────┐        ┌────────────────────────┐
│  DataSource (base)   │        │  ProtocolHandler       │
└──────────┬───────────┘        └────────────┬───────────┘
           │                                  │
    ┌──────┴──────┐                    ┌─────┴─────┐
    │             │                    │           │
    ▼             ▼                    ▼           ▼
┌─────────┐  ┌─────────┐    ┌──────────────┐ ┌──────────────┐
│  File   │  │   URL   │    │     HTTP     │ │    Mihomo    │
│ Source  │  │  Source │    │   Handler    │ │   Handler    │
└─────────┘  └─────────┘    └──────────────┘ └──────────────┘
     │            │                │                  │
     └────────┬───┘                └────────┬─────────┘
              ▼                             ▼
      ┌──────────────┐            ┌────────────────┐
      │  ProxyInfo   │            │  Test Results  │
      └──────────────┘            └────────────────┘
```

### 3.3 数据流图

```
┌─────────────┐
│   Config    │
│   Files     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      ConfigLoader               │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│      ProxyDetector.initialize() │
│  ┌────────────────────────────┐ │
│  │ • Init DataSources         │ │
│  │ • Init HttpHandler         │ │
│  │ • Init MihomoHandler       │ │
│  │ • Init Logger              │ │
│  └────────────────────────────┘ │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   fetch_all_proxies()           │
│  ┌────────────────────────────┐ │
│  │ FileSource.fetch_proxies() │ │
│  │ UrlSource.fetch_proxies()  │ │
│  │ ApiSource.fetch_proxies()  │ │
│  └──────────┬─────────────────┘ │
└─────────────┼───────────────────┘
              │
              ▼
      ┌───────────────┐
      │ List[Proxy    │
      │ Info]         │
      └───────┬───────┘
              │
              ▼
┌─────────────────────────────────┐
│   Concurrent Detection          │
│  ┌────────────────────────────┐ │
│  │ Semaphore(concurrent_tasks)│ │
│  │ asyncio.gather()           │ │
│  └────────────────────────────┘ │
└──────┬──────────────────────────┘
       │
       ├──────────────┬─────────────┐
       ▼              ▼             ▼
┌─────────────┐ ┌─────────┐ ┌─────────┐
│detect_proxy │ │detect   │ │detect   │
│   (task 1)  │ │(task 2) │ │(task N) │
└──────┬──────┘ └────┬────┘ └────┬────┘
       │             │           │
       └─────────────┴───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Aggregate Results    │
         │  ┌─────────────────┐  │
         │  │ Working proxies │  │
         │  │ Failed proxies  │  │
         │  │ Statistics      │  │
         │  └─────────────────┘  │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Save Output         │
         │  ┌─────────────────┐  │
         │  │ working.txt     │  │
         │  │ failed.txt      │  │
         │  │ statistics.json │  │
         │  └─────────────────┘  │
         └───────────────────────┘
```

## 4. 并发模型

### 4.1 异步执行模型

```python
# 信号量控制并发
semaphore = asyncio.Semaphore(concurrent_tasks)

async def bounded_detect(proxy):
    async with semaphore:
        return await detect_proxy(proxy)

# 并发执行
tasks = [bounded_detect(proxy) for proxy in proxies]
results = await asyncio.gather(*tasks)
```

### 4.2 并发控制策略

| 策略 | 描述 | 参数 |
|------|------|------|
| 信号量限制 | 限制同时运行的任务数 | `concurrent_tasks: 50` |
| 超时控制 | 单个任务的最大执行时间 | `timeout: 10` |
| 重试机制 | 失败后的重试次数 | `retry_attempts: 2` |
| 延迟重试 | 重试之间的等待时间 | `1 second` |

### 4.3 性能指标

**测试环境**: 4 Core CPU, 8GB RAM, 100Mbps Network

| 并发数 | 代理数 | 总时间 | 平均延迟 | CPU 使用率 | 内存使用 |
|--------|--------|--------|----------|-----------|---------|
| 10 | 100 | 120s | 150ms | 20% | 150MB |
| 50 | 100 | 45s | 160ms | 40% | 200MB |
| 100 | 100 | 30s | 180ms | 60% | 300MB |
| 200 | 100 | 25s | 220ms | 80% | 450MB |

## 5. Mihomo 集成

### 5.1 Mihomo 配置生成

```yaml
# 生成的 Mihomo 配置模板
port: 7890
socks-port: 7891
allow-lan: false
mode: Rule
log-level: warning
external-controller: '127.0.0.1:9090'

proxies:
  - name: test-proxy
    type: ss              # 协议类型
    server: example.com   # 服务器地址
    port: 8388           # 端口
    cipher: aes-256-gcm  # 加密方法
    password: password    # 密码

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - test-proxy

rules:
  - MATCH,DIRECT
```

### 5.2 Mihomo 进程管理

```python
# 启动 Mihomo 进程
process = await asyncio.create_subprocess_exec(
    './mihomo',
    '-f', config_file,
    '-d', temp_dir,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
)

# 等待启动
await asyncio.sleep(2)

# 使用本地 HTTP 代理测试
proxy_url = f'http://127.0.0.1:{local_port}'

# 清理进程
process.terminate()
await process.wait()
```

### 5.3 端口分配策略

```
Port Range: 10000-10100 (可配置)

┌─────────────────────────────────┐
│  Port Pool                      │
│  ┌───┬───┬───┬───┬───┬───┬───┐  │
│  │10000│10001│10002│...│10100│  │
│  └─┬─┘└─┬─┘└─┬─┘   └──┬─┘     │
└────┼────┼────┼────────┼────────┘
     │    │    │        │
     ▼    ▼    ▼        ▼
   Task1 Task2 Task3  TaskN

循环分配:
current_port = (current_port + 1) % (end - start) + start
```

## 6. 错误处理

### 6.1 错误分类

```
┌─────────────────────────────────┐
│  Error Categories               │
├─────────────────────────────────┤
│                                 │
│  1. Configuration Errors        │
│     • Invalid YAML              │
│     • Missing required fields   │
│     • Type mismatch             │
│     → Action: Fail fast         │
│                                 │
│  2. Data Source Errors          │
│     • File not found            │
│     • URL unreachable           │
│     • Parse error               │
│     → Action: Log, continue     │
│                                 │
│  3. Network Errors              │
│     • Connection timeout        │
│     • Connection refused        │
│     • DNS resolution failed     │
│     → Action: Retry, then fail  │
│                                 │
│  4. Protocol Errors             │
│     • Unsupported protocol      │
│     • Invalid config format     │
│     • Mihomo process failed     │
│     → Action: Skip, log error   │
│                                 │
│  5. System Errors               │
│     • Out of memory             │
│     • Disk full                 │
│     • Permission denied         │
│     → Action: Log, attempt fix  │
│                                 │
└─────────────────────────────────┘
```

### 6.2 重试策略

```python
for attempt in range(retry_attempts + 1):
    try:
        result = await test_proxy(proxy)
        if result.success:
            return result
        if attempt == retry_attempts:
            return result  # 最后一次尝试，返回失败结果
        await asyncio.sleep(1)  # 重试延迟
    except Exception as e:
        if attempt == retry_attempts:
            return FailedResult(error=str(e))
```

### 6.3 错误码定义

| 错误码 | 描述 | HTTP 状态码 | 处理方式 |
|--------|------|------------|---------|
| E001 | 配置文件不存在 | - | 退出 |
| E002 | YAML 解析错误 | - | 退出 |
| E003 | 数据源获取失败 | - | 使用缓存 |
| E004 | 代理连接超时 | - | 重试 |
| E005 | 代理连接被拒绝 | - | 标记失败 |
| E006 | Mihomo 二进制缺失 | - | 禁用 Mihomo |
| E007 | Mihomo 启动失败 | - | 跳过代理 |
| E008 | 不支持的协议 | - | 跳过代理 |

## 7. 性能优化

### 7.1 连接池

```python
# aiohttp ClientSession 复用
connector = aiohttp.TCPConnector(
    limit=100,              # 总连接数限制
    limit_per_host=10,      # 每个主机的连接数限制
    ttl_dns_cache=300,      # DNS 缓存时间
)

session = aiohttp.ClientSession(connector=connector)
```

### 7.2 缓存策略

```python
class UrlDataSource:
    def __init__(self):
        self._cache = []
        self._last_fetch = 0
        self._cache_ttl = 3600  # 1 hour
    
    async def fetch_proxies(self):
        current_time = time.time()
        if self._cache and (current_time - self._last_fetch) < self._cache_ttl:
            return self._cache  # 返回缓存
        
        # 获取新数据
        self._cache = await self._fetch_from_url()
        self._last_fetch = current_time
        return self._cache
```

### 7.3 内存管理

```python
# 增量处理结果
async def save_results_incrementally(results):
    async with aiofiles.open('output.txt', 'w') as f:
        for result in results:
            await f.write(f"{result}\n")
            await f.flush()  # 立即写入磁盘
```

## 8. 安全考虑

### 8.1 配置文件安全

```yaml
# 敏感信息应通过环境变量注入
data_sources:
  - type: api
    url: ${API_URL}
    headers:
      Authorization: "Bearer ${API_TOKEN}"
```

### 8.2 进程隔离

- Mihomo 运行在独立子进程
- 每个检测任务使用独立配置文件
- 临时文件存储在 `/tmp` 目录
- 检测完成后立即清理

### 8.3 网络安全

```python
# SSL 验证可配置
connector = aiohttp.TCPConnector(ssl=False)  # 开发环境
connector = aiohttp.TCPConnector(ssl=True)   # 生产环境

# 超时保护
timeout = aiohttp.ClientTimeout(
    total=30,      # 总超时
    connect=10,    # 连接超时
    sock_read=10,  # 读取超时
)
```

## 9. 监控与日志

### 9.1 日志级别

| 级别 | 描述 | 使用场景 |
|------|------|---------|
| DEBUG | 详细调试信息 | 开发调试 |
| INFO | 一般信息 | 正常运行 |
| WARNING | 警告信息 | 潜在问题 |
| ERROR | 错误信息 | 错误发生 |

### 9.2 日志格式

```
{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}

示例:
2024-01-01 12:00:00 | INFO     | detector:run_detection:123 - Starting proxy detection...
2024-01-01 12:00:05 | ERROR    | http_handler:test_proxy:45 - Connection timeout: proxy1.com:8080
```

### 9.3 指标收集

```python
statistics = {
    'total': 100,                    # 总代理数
    'working': 45,                   # 可用代理数
    'failed': 55,                    # 失败代理数
    'by_protocol': {                 # 按协议统计
        'http': {'total': 30, 'working': 20, 'failed': 10},
        'socks5': {'total': 25, 'working': 15, 'failed': 10},
    },
    'start_time': '2024-01-01T12:00:00',
    'end_time': '2024-01-01T12:05:30',
    'duration_seconds': 330,         # 总耗时
    'success_rate': 0.45,            # 成功率
}
```

## 10. 部署规格

### 10.1 系统要求

**最小配置**:
- CPU: 1 Core
- RAM: 512 MB
- Disk: 1 GB
- Network: 10 Mbps

**推荐配置**:
- CPU: 2+ Cores
- RAM: 2 GB+
- Disk: 5 GB+
- Network: 100 Mbps+

### 10.2 Docker 镜像

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# 安装依赖
RUN apt-get update && \
    apt-get install -y wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 下载 Mihomo
RUN wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64 \
    -O /usr/local/bin/mihomo && \
    chmod +x /usr/local/bin/mihomo

# Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 应用代码
COPY . .

CMD ["python", "main.py"]
```

### 10.3 资源限制

```yaml
# Docker Compose 资源限制
services:
  proxy-detector:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 512M
```

## 11. 测试规范

### 11.1 单元测试

```python
import pytest
from data_sources.file_source import FileDataSource

@pytest.mark.asyncio
async def test_file_source():
    source = FileDataSource({
        'enabled': True,
        'path': 'test_proxies.txt',
        'format': 'line'
    })
    proxies = await source.fetch_proxies()
    assert len(proxies) > 0
```

### 11.2 集成测试

```python
@pytest.mark.asyncio
async def test_http_detection():
    detector = ProxyDetector(config)
    await detector.initialize()
    
    proxy = ProxyInfo(
        protocol='http',
        host='test.proxy.com',
        port=8080
    )
    
    result = await detector.detect_proxy(proxy)
    assert 'success' in result
```

## 12. API 规范

### 12.1 ProxyInfo 数据模型

```python
class ProxyInfo(BaseModel):
    protocol: str           # 协议类型
    host: str              # 主机地址
    port: int              # 端口号
    username: str = None   # 用户名(可选)
    password: str = None   # 密码(可选)
    raw_config: str = None # 原始配置(可选)
    extra_params: dict = None  # 额外参数(可选)
```

### 12.2 检测结果模型

```python
DetectionResult = {
    'proxy': ProxyInfo,           # 代理信息
    'success': bool,              # 是否成功
    'error': Optional[str],       # 错误信息
    'latency': Optional[float],   # 延迟(毫秒)
    'attempts': int,              # 尝试次数
    'timestamp': str,             # 时间戳
}
```

## 13. 版本兼容性

| 组件 | 最小版本 | 推荐版本 | 测试版本 |
|------|---------|---------|---------|
| Python | 3.8 | 3.11+ | 3.8, 3.9, 3.10, 3.11, 3.12 |
| aiohttp | 3.8.0 | 3.9.1 | 3.9.1 |
| Mihomo | 1.0.0 | Latest | Latest |

## 14. 许可证

本项目采用开源许可证，详见 LICENSE 文件。

## 15. 文档版本

- **文档版本**: 1.0.0
- **最后更新**: 2024-01-01
- **作者**: Proxy Detector Team
