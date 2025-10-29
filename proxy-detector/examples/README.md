# Proxy Detector Examples

This directory contains example configurations and usage scripts for the Proxy Detector.

## Files

- `proxies.txt` - Example proxy list in line format
- `test_detector.py` - Test script to verify the detector functionality

## Quick Start

1. Copy the example proxy list:
```bash
cp examples/proxies.txt ./proxies.txt
```

2. Edit the proxy list with your actual proxies

3. Run the detector:
```bash
python main.py --once
```

## Configuration Examples

### Minimal Configuration

Create a minimal `config/config.yaml`:

```yaml
data_sources:
  - type: file
    enabled: true
    path: ./proxies.txt
    format: line

detection:
  timeout: 10
  concurrent_tasks: 50

mihomo:
  enabled: false

logging:
  level: INFO

output:
  save_working: true
  working_proxies_file: ./output/working.txt
```

### Multiple Data Sources

```yaml
data_sources:
  # Local file
  - type: file
    enabled: true
    path: ./proxies.txt
    format: line
  
  # Remote URL
  - type: url
    enabled: true
    url: https://raw.githubusercontent.com/user/repo/main/proxies.txt
    interval: 3600
    format: line
  
  # API endpoint
  - type: api
    enabled: true
    url: https://api.proxy-provider.com/list
    method: GET
    headers:
      Authorization: "Bearer YOUR_API_KEY"
    interval: 1800
```

### High-Performance Configuration

For testing large proxy lists:

```yaml
detection:
  timeout: 5
  concurrent_tasks: 200
  retry_attempts: 1
  check_interval: 600
```

### Mihomo-Enabled Configuration

For testing SS/SSR/VMess/VLESS/Trojan/Hysteria protocols:

```yaml
mihomo:
  enabled: true
  binary_path: ./mihomo
  config_template: ./config/mihomo-template.yaml
  api_host: 127.0.0.1
  api_port: 9090
  http_port_start: 10000
  http_port_end: 10100
  supported_protocols:
    - ss
    - ssr
    - vmess
    - vless
    - trojan
    - hysteria
    - hysteria2
```

## Testing Without Mihomo

If you only want to test HTTP/HTTPS/SOCKS5 proxies without Mihomo:

```yaml
mihomo:
  enabled: false

direct_protocols:
  - http
  - https
  - socks5
```

## Running Tests

Test the detector functionality:

```bash
python examples/test_detector.py
```

## Docker Usage

Build and run with Docker:

```bash
docker build -t proxy-detector .
docker run -v $(pwd)/config:/app/config -v $(pwd)/proxies.txt:/app/proxies.txt proxy-detector
```

Or use docker-compose:

```bash
docker-compose up -d
```

View logs:

```bash
docker-compose logs -f
```

## Output Examples

### Working Proxies (working_proxies.txt)
```
http://proxy1.example.com:8080 # Latency: 145.23ms
socks5://proxy2.example.com:1080 # Latency: 89.45ms
ss://aes-256-gcm:password@ss.example.com:8388 # Latency: 234.67ms
```

### Statistics (statistics.json)
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
    }
  },
  "start_time": "2024-01-01T12:00:00",
  "end_time": "2024-01-01T12:05:30"
}
```

## Troubleshooting

### Issue: No proxies detected

**Solution**: Check your proxies.txt file format and ensure at least one data source is enabled.

### Issue: Mihomo protocols not working

**Solution**: 
1. Ensure Mihomo binary is downloaded and executable
2. Check the binary path in config.yaml
3. Verify the protocol format in your proxy list

### Issue: Too many timeouts

**Solution**: 
- Increase timeout value in config.yaml
- Reduce concurrent_tasks to avoid overwhelming your network
- Check your internet connection

### Issue: High memory usage

**Solution**:
- Reduce concurrent_tasks
- Enable result streaming instead of storing all results in memory
- Process proxies in batches

## Advanced Usage

### Custom Test URLs

Test against specific websites:

```yaml
detection:
  test_urls:
    - https://www.google.com
    - https://www.cloudflare.com
    - https://api.ipify.org
```

### Protocol-Specific Configuration

Configure different timeouts for different protocols:

```yaml
protocol_config:
  http:
    timeout: 5
  socks5:
    timeout: 10
  ss:
    timeout: 15
```

## Performance Tips

1. **Start Small**: Test with 10-20 proxies first to tune your configuration
2. **Adjust Concurrency**: Find the sweet spot for your system (usually 50-200)
3. **Use Retries Wisely**: More retries = more accurate but slower
4. **Cache Results**: Use the API/URL data source caching to avoid repeated fetches
5. **Monitor Resources**: Watch CPU/memory/network usage during detection

## Integration Examples

### Use as a Library

```python
import asyncio
from utils.config_loader import ConfigLoader
from core.detector import ProxyDetector

async def main():
    config = ConfigLoader('./config/config.yaml').config
    detector = ProxyDetector(config)
    
    await detector.initialize()
    await detector.run_detection()
    await detector.cleanup()

asyncio.run(main())
```

### Scheduled Runs (Cron)

```bash
# Run every hour
0 * * * * cd /path/to/proxy-detector && python main.py --once
```

### API Integration

Create a simple web API wrapper:

```python
from aiohttp import web
from core.detector import ProxyDetector

app = web.Application()
detector = None

async def check_proxies(request):
    await detector.run_detection()
    return web.json_response({'status': 'completed'})

app.router.add_post('/check', check_proxies)
web.run_app(app)
```
