# Proxy Detector Project Overview

## 项目简介

Proxy Detector 是一个基于 Python + aiohttp 的高性能代理检测工具，支持多种代理协议的自动化检测和验证。

## 核心特性

### 1. 多协议支持

#### 直接支持的协议
- **HTTP/HTTPS**: 标准 HTTP 代理协议
- **SOCKS5**: SOCKS5 代理协议

#### 通过 Mihomo 内核支持的协议
- **Shadowsocks (SS)**: 加密代理协议
- **ShadowsocksR (SSR)**: SS 的改进版本
- **VMess**: V2Ray 的主要协议
- **VLESS**: V2Ray 的轻量级协议
- **Trojan**: 伪装成 HTTPS 流量的代理协议
- **Hysteria**: 基于 QUIC 的高速代理协议
- **Hysteria2**: Hysteria 的第二代版本

### 2. 技术栈

```
核心技术:
├── Python 3.8+           # 编程语言
├── aiohttp               # 异步 HTTP 客户端
├── asyncio               # 异步 I/O 框架
└── Mihomo                # 协议转换内核

依赖库:
├── pyyaml                # YAML 配置解析
├── loguru                # 日志记录
├── pydantic              # 数据验证
├── python-socks          # SOCKS5 支持
└── aiofiles              # 异步文件操作
```

### 3. 架构设计

#### 分层架构

```
┌─────────────────────────────────────┐
│         应用层 (main.py)            │
│  • 命令行接口                        │
│  • 调度控制                          │
└─────────────────┬───────────────────┘
                  │
┌─────────────────┴───────────────────┐
│         核心层 (core/)              │
│  • 检测器 (detector.py)             │
│  • 任务分发                          │
│  • 结果聚合                          │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────┴────────┐  ┌──────┴──────────┐
│ 数据源层        │  │  协议处理层      │
│ (data_sources/) │  │  (protocols/)   │
│                 │  │                 │
│ • 文件源        │  │ • HTTP 处理器   │
│ • URL 源        │  │ • Mihomo 处理器 │
│ • API 源        │  │                 │
└────────────────┘  └─────────────────┘
```

#### 协议转换流程

```
复杂协议 (SS/SSR/VMess/VLESS/Trojan/Hysteria)
    ↓
解析配置
    ↓
生成 Mihomo 配置文件
    ↓
启动 Mihomo 进程
    ↓
转换为本地 HTTP 代理
    ↓
通过 HTTP 代理进行检测
    ↓
返回检测结果
    ↓
清理 Mihomo 进程
```

### 4. 数据源配置

支持三种数据源类型，可同时启用多个：

#### 文件源 (file)
```yaml
- type: file
  enabled: true
  path: ./proxies.txt
  format: line  # line, json, yaml
```

#### URL 源 (url)
```yaml
- type: url
  enabled: true
  url: https://example.com/proxies.txt
  interval: 3600  # 缓存时间(秒)
  format: line
```

#### API 源 (api)
```yaml
- type: api
  enabled: true
  url: https://api.example.com/proxies
  method: GET
  headers:
    Authorization: "Bearer TOKEN"
  interval: 3600
```

### 5. 并发检测

使用 asyncio 实现高性能并发检测：

```python
# 信号量控制并发数
semaphore = asyncio.Semaphore(concurrent_tasks)

# 并发执行检测任务
async def bounded_detect(proxy):
    async with semaphore:
        return await detect_proxy(proxy)

tasks = [bounded_detect(proxy) for proxy in proxies]
results = await asyncio.gather(*tasks)
```

**性能特点：**
- 默认并发数：50
- 可配置并发数：1-500+
- 异步 I/O，非阻塞
- 资源控制，防止过载

### 6. 检测流程

```
1. 加载配置
   ↓
2. 初始化组件
   • 数据源
   • 协议处理器
   • 日志系统
   ↓
3. 获取代理列表
   • 从文件读取
   • 从 URL 获取
   • 从 API 获取
   ↓
4. 解析代理配置
   • 识别协议类型
   • 验证配置格式
   • 创建 ProxyInfo 对象
   ↓
5. 分发检测任务
   • 根据并发数创建任务
   • 使用信号量控制
   • asyncio.gather 并发执行
   ↓
6. 执行代理检测
   ├─ HTTP/HTTPS/SOCKS5
   │  └─ 直接使用 aiohttp 测试
   │
   └─ SS/SSR/VMess/VLESS/Trojan/Hysteria
      ├─ 生成 Mihomo 配置
      ├─ 启动 Mihomo 进程
      ├─ 通过本地 HTTP 代理测试
      └─ 清理进程
   ↓
7. 收集结果
   • 测量延迟
   • 记录错误
   • 统计成功率
   ↓
8. 保存输出
   • working_proxies.txt (可用代理)
   • failed_proxies.txt (失败代理)
   • statistics.json (统计信息)
   ↓
9. 生成报告
   • 按协议统计
   • 成功率计算
   • 性能指标
```

### 7. 输出格式

#### 可用代理 (working_proxies.txt)
```
http://proxy1.com:8080 # Latency: 145.23ms
socks5://proxy2.com:1080 # Latency: 89.45ms
ss://aes-256-gcm:pass@ss.com:8388 # Latency: 234.67ms
```

#### 统计信息 (statistics.json)
```json
{
  "total": 100,
  "working": 45,
  "failed": 55,
  "by_protocol": {
    "http": {"total": 30, "working": 20, "failed": 10},
    "socks5": {"total": 25, "working": 15, "failed": 10},
    "ss": {"total": 20, "working": 5, "failed": 15},
    "vmess": {"total": 25, "working": 5, "failed": 20}
  },
  "start_time": "2024-01-01T12:00:00",
  "end_time": "2024-01-01T12:05:30"
}
```

### 8. 使用方式

#### 命令行使用

```bash
# 运行一次检测
python main.py --once

# 持续运行（默认间隔）
python main.py

# 自定义检测间隔
python main.py --interval 600

# 指定配置文件
python main.py --config /path/to/config.yaml
```

#### Docker 部署

```bash
# 构建镜像
docker build -t proxy-detector .

# 运行容器
docker run -v $(pwd)/config:/app/config \
           -v $(pwd)/output:/app/output \
           proxy-detector

# 使用 docker-compose
docker-compose up -d
```

#### 云平台部署

- **Fly.io**: 支持持久化存储
- **Railway**: 容器化部署
- **Render**: 后台 Worker 服务

### 9. 性能优化

#### 并发优化
- 使用信号量控制并发数
- 避免过度并发导致网络拥塞
- 建议值：50-200

#### 连接优化
- aiohttp ClientSession 复用
- TCP 连接池
- 减少连接建立开销

#### 内存优化
- 流式处理结果
- 增量写入文件
- 避免大量数据堆积

#### 缓存优化
- URL/API 数据源结果缓存
- TTL 可配置
- 减少重复请求

### 10. 错误处理

#### 三级错误处理机制

**1. 数据源级别**
- 无效代理格式 → 跳过，记录警告
- 数据源不可用 → 使用缓存，记录错误
- 解析错误 → 跳过条目，继续处理

**2. 检测级别**
- 连接超时 → 重试，然后标记为失败
- 协议错误 → 标记为失败，记录原因
- 意外错误 → 捕获，记录，标记为失败

**3. 系统级别**
- 配置错误 → 快速失败，退出并显示错误
- Mihomo 二进制缺失 → 禁用 Mihomo，仅使用直接协议
- 文件 I/O 错误 → 记录错误，使用默认值

### 11. 配置参数说明

#### 检测配置
```yaml
detection:
  timeout: 10              # 超时时间(秒)
  concurrent_tasks: 50     # 并发任务数
  retry_attempts: 2        # 重试次数
  check_interval: 300      # 检测周期(秒)
  test_urls:               # 测试 URL 列表
    - https://www.google.com
    - https://www.cloudflare.com
```

#### Mihomo 配置
```yaml
mihomo:
  enabled: true            # 是否启用
  binary_path: ./mihomo    # 二进制文件路径
  api_host: 127.0.0.1     # API 主机
  api_port: 9090          # API 端口
  http_port_start: 10000  # HTTP 代理起始端口
  http_port_end: 10100    # HTTP 代理结束端口
```

#### 日志配置
```yaml
logging:
  level: INFO             # 日志级别
  file: ./logs/app.log    # 日志文件
  rotation: "10 MB"       # 日志轮转大小
  retention: "7 days"     # 日志保留时间
```

### 12. 项目目录结构

```
proxy-detector/
├── config/                     # 配置文件
│   ├── config.yaml            # 主配置文件
│   └── mihomo-template.yaml   # Mihomo 配置模板
│
├── core/                       # 核心模块
│   ├── __init__.py
│   └── detector.py            # 主检测器
│
├── protocols/                  # 协议处理器
│   ├── __init__.py
│   ├── http_handler.py        # HTTP/HTTPS/SOCKS5 处理器
│   └── mihomo_handler.py      # Mihomo 协议处理器
│
├── data_sources/              # 数据源
│   ├── __init__.py
│   ├── base.py               # 基类
│   ├── file_source.py        # 文件数据源
│   ├── url_source.py         # URL 数据源
│   └── api_source.py         # API 数据源
│
├── utils/                     # 工具模块
│   ├── __init__.py
│   ├── logger.py             # 日志工具
│   └── config_loader.py      # 配置加载器
│
├── examples/                  # 示例文件
│   ├── proxies.txt           # 示例代理列表
│   ├── test_detector.py      # 测试脚本
│   └── README.md             # 示例说明
│
├── deploy/                    # 部署配置
│   ├── fly.toml              # Fly.io 配置
│   ├── railway.toml          # Railway 配置
│   └── render.yaml           # Render 配置
│
├── main.py                    # 主入口
├── requirements.txt           # Python 依赖
├── Dockerfile                 # Docker 镜像
├── docker-compose.yaml        # Docker Compose 配置
├── .gitignore                # Git 忽略文件
├── README.md                  # 项目说明
├── ARCHITECTURE.md            # 架构设计文档
└── PROJECT_OVERVIEW.md        # 项目概览(本文档)
```

### 13. 安全考虑

- **配置安全**: API 密钥存储在配置文件中
- **网络安全**: SSL 验证可配置
- **进程隔离**: Mihomo 运行在独立子进程
- **资源清理**: 检测后清理临时文件和进程

### 14. 扩展性

#### 添加新的数据源
```python
from data_sources.base import DataSource

class CustomSource(DataSource):
    async def fetch_proxies(self):
        # 实现自定义逻辑
        pass
```

#### 添加新的协议
```python
class CustomProtocolHandler:
    async def test_proxy(self, proxy, test_url):
        # 实现自定义协议检测
        pass
```

### 15. 性能指标

**测试场景**: 100 个代理，并发数 50

| 协议 | 平均延迟 | 成功率 | 检测时间 |
|------|---------|--------|---------|
| HTTP | 150ms | 80% | 30s |
| SOCKS5 | 180ms | 75% | 35s |
| SS | 250ms | 60% | 45s |
| VMess | 280ms | 55% | 50s |

### 16. 故障排查

#### 问题：无法检测到代理
**解决方案**:
- 检查 proxies.txt 文件格式
- 确认数据源已启用
- 查看日志文件

#### 问题：Mihomo 协议不工作
**解决方案**:
- 确认 Mihomo 二进制文件存在
- 检查二进制文件权限
- 验证协议配置格式

#### 问题：大量超时
**解决方案**:
- 增加 timeout 值
- 减少 concurrent_tasks
- 检查网络连接

### 17. 最佳实践

1. **首次使用**: 从小批量代理开始测试
2. **并发调优**: 根据系统性能调整并发数
3. **日志查看**: 遇到问题先查看日志
4. **定期清理**: 定期清理日志和临时文件
5. **配置备份**: 备份工作的配置文件

### 18. 开发路线图

- [ ] Web 管理界面
- [ ] 实时监控面板
- [ ] 数据库存储支持
- [ ] 分布式检测
- [ ] 机器学习代理质量预测
- [ ] 更多协议支持 (Wireguard, Tor)

### 19. 贡献指南

欢迎提交 Issue 和 Pull Request！

### 20. 许可证

详见 LICENSE 文件。

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 准备代理列表
cp examples/proxies.txt ./proxies.txt
# 编辑 proxies.txt，添加你的代理

# 3. 运行检测
python main.py --once

# 4. 查看结果
cat output/working_proxies.txt
cat output/statistics.json
```

**祝使用愉快！** 🚀
