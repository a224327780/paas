# Proxy Detector

一个基于 Python + aiohttp 构建的高性能代理检测工具，支持多种协议包括 HTTP、HTTPS、SOCKS5、Shadowsocks、ShadowsocksR、VMess、VLESS、Trojan、Hysteria 和 Hysteria2。

A high-performance proxy detection tool built with Python and aiohttp, supporting multiple protocols including HTTP, HTTPS, SOCKS5, Shadowsocks, ShadowsocksR, VMess, VLESS, Trojan, Hysteria, and Hysteria2.

## Features

- **Multi-Protocol Support**: HTTP, HTTPS, SOCKS5, SS, SSR, VMess, VLESS, Trojan, Hysteria, Hysteria2
- **High Performance**: Asynchronous I/O with configurable concurrent tasks
- **Mihomo Integration**: Converts complex protocols (SS, SSR, VMess, VLESS, Trojan, Hysteria) to HTTP for testing
- **Flexible Data Sources**: File-based, URL-based, and API-based proxy sources
- **Comprehensive Logging**: Detailed logging with rotation and retention
- **Statistics & Reports**: Detailed statistics by protocol with success rates
- **Configurable**: YAML-based configuration for all aspects

## Architecture

```
proxy-detector/
├── config/                 # Configuration files
│   ├── config.yaml        # Main configuration
│   └── mihomo-template.yaml  # Mihomo configuration template
├── core/                   # Core detection logic
│   └── detector.py        # Main detector class
├── protocols/              # Protocol handlers
│   ├── http_handler.py    # HTTP/HTTPS/SOCKS5 handler
│   └── mihomo_handler.py  # Mihomo-based protocol handler
├── data_sources/           # Data source adapters
│   ├── base.py            # Base classes
│   ├── file_source.py     # File-based source
│   ├── url_source.py      # URL-based source
│   └── api_source.py      # API-based source
├── utils/                  # Utilities
│   ├── logger.py          # Logging setup
│   └── config_loader.py   # Configuration loader
├── main.py                 # Entry point
└── requirements.txt        # Python dependencies
```

## Requirements

- Python 3.8+
- aiohttp
- Mihomo binary (for SS, SSR, VMess, VLESS, Trojan, Hysteria protocols)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download Mihomo binary (optional, required for mihomo-based protocols):
```bash
# Linux
wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64 -O mihomo
chmod +x mihomo

# macOS
wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-darwin-amd64 -O mihomo
chmod +x mihomo
```

## Configuration

Edit `config/config.yaml` to configure:

- **Data Sources**: Configure file, URL, or API-based proxy sources
- **Detection Settings**: Timeout, concurrent tasks, retry attempts
- **Mihomo Settings**: Binary path, ports, supported protocols
- **Logging**: Log level, format, rotation
- **Output**: Save locations for working/failed proxies and statistics

## Usage

### Run once (single detection cycle):
```bash
python main.py --once
```

### Run continuously with default interval:
```bash
python main.py
```

### Run continuously with custom interval:
```bash
python main.py --interval 600  # Check every 10 minutes
```

### Use custom configuration file:
```bash
python main.py --config /path/to/config.yaml
```

## Data Source Formats

### File Format (line-based):
```
http://proxy1.com:8080
https://user:pass@proxy2.com:8443
socks5://proxy3.com:1080
ss://BASE64_ENCODED_CONFIG
vmess://BASE64_ENCODED_CONFIG
trojan://password@host:port
```

### JSON Format:
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

### YAML Format:
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

## Protocol Support

### Direct Testing (Native):
- **HTTP/HTTPS**: Direct connection testing
- **SOCKS5**: Using python-socks library

### Mihomo-Based Testing (Conversion to HTTP):
- **Shadowsocks (SS)**: Converted to HTTP proxy via Mihomo
- **ShadowsocksR (SSR)**: Converted to HTTP proxy via Mihomo
- **VMess**: Converted to HTTP proxy via Mihomo
- **VLESS**: Converted to HTTP proxy via Mihomo
- **Trojan**: Converted to HTTP proxy via Mihomo
- **Hysteria**: Converted to HTTP proxy via Mihomo
- **Hysteria2**: Converted to HTTP proxy via Mihomo

## Output

Results are saved to the `output/` directory:

- **working_proxies.txt**: List of working proxies with latency
- **failed_proxies.txt**: List of failed proxies with error reasons
- **statistics.json**: Detailed statistics including success rates by protocol

## Example Statistics Output

```
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
```

## Performance Tuning

Adjust these settings in `config/config.yaml`:

- `concurrent_tasks`: Number of simultaneous proxy tests (default: 50)
- `timeout`: Connection timeout in seconds (default: 10)
- `retry_attempts`: Number of retry attempts for failed proxies (default: 2)

## Logging

Logs are saved to `logs/proxy_detector.log` with automatic rotation:
- Rotation: 10 MB
- Retention: 7 days
- Compression: zip

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
