# Proxy Detector - Architecture Design

## Overview

Proxy Detector is a high-performance, asynchronous proxy detection system built with Python and aiohttp. It supports multiple proxy protocols and uses the Mihomo kernel to convert complex protocols to HTTP for testing.

## Technology Stack

- **Language**: Python 3.8+
- **HTTP Client**: aiohttp (async HTTP client)
- **Configuration**: YAML
- **Logging**: loguru
- **Protocol Conversion**: Mihomo kernel
- **Data Validation**: Pydantic

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       Main Entry Point                        │
│                          (main.py)                            │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Configuration Layer                       │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │  Config Loader   │  │     Logger       │                 │
│  │ (config_loader)  │  │   (logger.py)    │                 │
│  └──────────────────┘  └──────────────────┘                 │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Core Detector                            │
│                     (core/detector.py)                        │
│                                                               │
│  ┌────────────────────────────────────────────────┐          │
│  │  • Initialize data sources                     │          │
│  │  • Initialize protocol handlers                │          │
│  │  • Fetch proxies from all sources              │          │
│  │  • Distribute detection tasks                  │          │
│  │  • Collect and aggregate results               │          │
│  │  • Generate statistics and reports             │          │
│  └────────────────────────────────────────────────┘          │
└───────┬───────────────────────────────┬─────────────────────┘
        │                               │
        ▼                               ▼
┌──────────────────┐         ┌────────────────────────────┐
│  Data Sources    │         │   Protocol Handlers        │
│                  │         │                            │
│ ┌──────────────┐ │         │ ┌────────────────────────┐ │
│ │ File Source  │ │         │ │   HTTP Handler         │ │
│ │ (file_source)│ │         │ │  • HTTP/HTTPS          │ │
│ └──────────────┘ │         │ │  • SOCKS5              │ │
│                  │         │ └────────────────────────┘ │
│ ┌──────────────┐ │         │                            │
│ │  URL Source  │ │         │ ┌────────────────────────┐ │
│ │ (url_source) │ │         │ │   Mihomo Handler       │ │
│ └──────────────┘ │         │ │  • SS/SSR              │ │
│                  │         │ │  • VMess/VLESS         │ │
│ ┌──────────────┐ │         │ │  • Trojan              │ │
│ │  API Source  │ │         │ │  • Hysteria/Hysteria2  │ │
│ │ (api_source) │ │         │ └────────────────────────┘ │
│ └──────────────┘ │         │                            │
└──────────────────┘         └────────────────────────────┘
        │                               │
        └───────────────┬───────────────┘
                        ▼
        ┌──────────────────────────────┐
        │      Output Layer            │
        │  • Working proxies file      │
        │  • Failed proxies file       │
        │  • Statistics (JSON)         │
        │  • Logs                      │
        └──────────────────────────────┘
```

## Component Design

### 1. Core Layer (core/)

#### ProxyDetector (detector.py)
- **Responsibility**: Main orchestrator for the entire detection process
- **Key Functions**:
  - Initialize all components
  - Fetch proxies from multiple data sources
  - Distribute detection tasks with concurrency control
  - Aggregate results and generate statistics
  - Save output files

**Design Pattern**: Facade Pattern - provides a unified interface to the subsystems

### 2. Data Source Layer (data_sources/)

#### Base Classes (base.py)
- `ProxyInfo`: Data model for proxy information (using Pydantic)
- `DataSource`: Abstract base class for all data sources

#### Implementations:
- **FileDataSource**: Reads proxies from local files (TXT, JSON, YAML)
- **UrlDataSource**: Fetches proxies from HTTP endpoints with caching
- **ApiDataSource**: Fetches proxies from REST APIs with authentication

**Design Pattern**: Strategy Pattern - different data source implementations

### 3. Protocol Handler Layer (protocols/)

#### HTTP Handler (http_handler.py)
- Direct testing for HTTP, HTTPS, SOCKS5
- Uses aiohttp for HTTP/HTTPS
- Uses python-socks for SOCKS5

#### Mihomo Handler (mihomo_handler.py)
- Converts complex protocols to HTTP proxy
- Manages Mihomo process lifecycle
- Generates Mihomo configuration dynamically
- Port allocation for multiple concurrent tests

**Design Pattern**: Adapter Pattern - converts different protocols to HTTP

### 4. Utility Layer (utils/)

#### Config Loader (config_loader.py)
- YAML-based configuration
- Nested configuration access
- Default value support

#### Logger (logger.py)
- Structured logging
- Log rotation and retention
- Console and file output

## Protocol Support Architecture

### Direct Protocols (No Conversion)

```
┌──────────┐         ┌──────────────────┐         ┌──────────┐
│  Proxy   │ ──────► │  aiohttp Client  │ ──────► │ Test URL │
│  Info    │         │  (HTTP/HTTPS)    │         │          │
└──────────┘         └──────────────────┘         └──────────┘

┌──────────┐         ┌──────────────────┐         ┌──────────┐
│  Proxy   │ ──────► │  python-socks    │ ──────► │ Test URL │
│  Info    │         │    (SOCKS5)      │         │          │
└──────────┘         └──────────────────┘         └──────────┘
```

### Mihomo-Based Protocols (With Conversion)

```
┌──────────┐    ┌─────────────────┐    ┌─────────────┐    ┌──────────┐
│  Proxy   │───►│ Mihomo Config   │───►│   Mihomo    │───►│ Test URL │
│  Info    │    │   Generator     │    │   Process   │    │          │
│ (SS/SSR/ │    │ • Parse config  │    │ • Start     │    │          │
│  VMess/  │    │ • Generate YAML │    │ • Convert   │    │          │
│  VLESS/  │    │ • Port alloc    │    │   to HTTP   │    │          │
│ Trojan/  │    └─────────────────┘    │ • Proxy req │    │          │
│ Hysteria)│                            │ • Stop      │    │          │
└──────────┘                            └─────────────┘    └──────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Local HTTP │
                                        │  Proxy Port │
                                        └─────────────┘
```

## Concurrency Design

### Async/Await Model

```python
# Semaphore-based concurrency control
semaphore = asyncio.Semaphore(concurrent_tasks)

async def bounded_detect(proxy):
    async with semaphore:
        return await detect_proxy(proxy)

# Parallel execution
tasks = [bounded_detect(proxy) for proxy in proxies]
results = await asyncio.gather(*tasks)
```

### Benefits:
- **High throughput**: Test hundreds of proxies simultaneously
- **Resource control**: Semaphore prevents overwhelming the system
- **Non-blocking I/O**: Efficient network operations

## Data Flow

### Detection Cycle

```
1. Load Configuration
   ↓
2. Initialize Components
   ├─ Data Sources
   ├─ Protocol Handlers
   └─ Logger
   ↓
3. Fetch Proxies
   ├─ File Source
   ├─ URL Source (with cache)
   └─ API Source (with cache)
   ↓
4. Parse & Validate
   └─ ProxyInfo models
   ↓
5. Distribute Detection Tasks
   ├─ Create semaphore-bounded tasks
   └─ asyncio.gather()
   ↓
6. Detect Each Proxy
   ├─ Determine protocol
   ├─ Select handler
   │  ├─ HTTP Handler (direct)
   │  └─ Mihomo Handler (conversion)
   ├─ Test connection
   ├─ Measure latency
   └─ Retry on failure
   ↓
7. Aggregate Results
   ├─ Working proxies
   ├─ Failed proxies
   └─ Statistics
   ↓
8. Save Output
   ├─ working_proxies.txt
   ├─ failed_proxies.txt
   └─ statistics.json
   ↓
9. Cleanup & Report
```

## Configuration Architecture

### Hierarchical Configuration

```yaml
# Global settings
logging:
  level: INFO
  file: ./logs/app.log

# Data source configuration
data_sources:
  - type: file
    enabled: true
    path: ./proxies.txt

# Detection configuration
detection:
  timeout: 10
  concurrent_tasks: 50
  retry_attempts: 2

# Protocol-specific configuration
mihomo:
  enabled: true
  binary_path: ./mihomo
  supported_protocols: [ss, ssr, vmess, vless, trojan, hysteria, hysteria2]

# Output configuration
output:
  save_working: true
  working_proxies_file: ./output/working.txt
```

### Configuration Loading Flow

```
config.yaml ──► ConfigLoader ──► Typed Config Objects ──► Components
```

## Error Handling Strategy

### Levels of Error Handling

1. **Data Source Level**
   - Invalid proxy format → Skip proxy, log warning
   - Source unavailable → Use cache, log error
   - Parse error → Skip entry, continue processing

2. **Detection Level**
   - Connection timeout → Retry, then mark as failed
   - Protocol error → Mark as failed, log reason
   - Unexpected error → Catch, log, mark as failed

3. **System Level**
   - Configuration error → Fail fast, exit with error
   - Mihomo binary missing → Disable mihomo, continue with direct protocols
   - File I/O error → Log error, use defaults

### Retry Strategy

```python
for attempt in range(retry_attempts + 1):
    try:
        result = await test_proxy(proxy)
        if result.success or attempt == retry_attempts:
            return result
        await asyncio.sleep(1)  # Brief delay between retries
    except Exception as e:
        if attempt == retry_attempts:
            return FailedResult(error=str(e))
```

## Performance Optimizations

### 1. Connection Pooling
- aiohttp ClientSession reuse
- TCP connection pooling

### 2. Caching
- URL/API source results cached with TTL
- Avoid redundant fetches

### 3. Concurrent Execution
- Semaphore-based concurrency control
- Configurable concurrent task limit

### 4. Process Management
- Mihomo process reuse for batch testing
- Proper cleanup on shutdown

### 5. Memory Management
- Streaming results processing
- Bounded task queue
- Incremental file writes

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- Distribute proxy lists across instances
- Aggregate results from multiple workers

### Vertical Scaling
- Increase concurrent_tasks for more parallelism
- Adjust timeouts based on network capacity
- Tune semaphore limits

## Security Considerations

1. **Configuration**
   - Sensitive data (API keys) in config file
   - File permissions for config files
   - No hardcoded credentials

2. **Network**
   - SSL verification can be toggled
   - Proxy authentication support
   - Rate limiting for external sources

3. **Process Isolation**
   - Mihomo runs in subprocess
   - Separate temporary config files
   - Cleanup after testing

## Extension Points

### Adding New Data Sources
```python
class CustomDataSource(DataSource):
    async def fetch_proxies(self) -> List[ProxyInfo]:
        # Implement custom logic
        pass
    
    async def close(self):
        # Cleanup
        pass
```

### Adding New Protocols
```python
class CustomProtocolHandler:
    async def test_proxy(self, proxy: ProxyInfo, test_url: str):
        # Implement custom protocol testing
        pass
```

### Custom Output Formats
```python
class CustomOutputFormatter:
    async def save_results(self, results: List[Dict]):
        # Implement custom output format
        pass
```

## Deployment Architecture

### Standalone Deployment
```
┌─────────────────────────────────┐
│      Proxy Detector Server      │
│  • Python runtime               │
│  • Mihomo binary                │
│  • Config files                 │
│  • Cron job for scheduling      │
└─────────────────────────────────┘
```

### Container Deployment (Docker)
```
┌─────────────────────────────────┐
│   Docker Container              │
│  ┌──────────────────────────┐   │
│  │  proxy-detector          │   │
│  │  • Python 3.11           │   │
│  │  • Mihomo binary         │   │
│  │  • Dependencies          │   │
│  └──────────────────────────┘   │
│  Volumes:                       │
│  • /app/config (config files)   │
│  • /app/logs (log output)       │
│  • /app/output (results)        │
└─────────────────────────────────┘
```

### Cloud Deployment
- **Fly.io**: Worker with volume for results
- **Railway**: Container deployment with persistent storage
- **Render**: Background worker service

## Monitoring & Observability

### Metrics
- Total proxies tested
- Success/failure rates
- Average latency by protocol
- Detection cycle duration

### Logging
- Structured logs with context
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- Log rotation and retention
- Both console and file output

### Statistics
- JSON-formatted statistics
- Per-protocol breakdown
- Timestamps for tracking
- Historical data collection

## Future Enhancements

1. **Advanced Features**
   - Geographic location detection
   - Bandwidth testing
   - Anonymity level detection
   - Proxy chain support

2. **Performance**
   - Distributed detection across multiple nodes
   - Result streaming to database
   - Real-time web dashboard

3. **Protocol Support**
   - Wireguard support
   - Tor bridge support
   - Custom protocol plugins

4. **Intelligence**
   - ML-based proxy quality prediction
   - Automatic optimal proxy selection
   - Pattern detection for proxy farms

## Conclusion

This architecture provides a robust, scalable, and extensible foundation for proxy detection across multiple protocols. The use of async/await patterns ensures high performance, while the modular design allows for easy extension and maintenance.
