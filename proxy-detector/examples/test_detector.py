import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_sources.base import ProxyInfo
from protocols.http_handler import HttpProtocolHandler


async def test_http_handler():
    print("Testing HTTP Protocol Handler...")
    
    handler = HttpProtocolHandler(timeout=10)
    
    test_proxies = [
        ProxyInfo(
            protocol="http",
            host="proxy.example.com",
            port=8080,
            raw_config="http://proxy.example.com:8080"
        ),
        ProxyInfo(
            protocol="socks5",
            host="socks.example.com",
            port=1080,
            username="user",
            password="pass",
            raw_config="socks5://user:pass@socks.example.com:1080"
        ),
    ]
    
    test_url = "https://www.google.com"
    
    for proxy in test_proxies:
        print(f"\nTesting {proxy}...")
        success, error, latency = await handler.test_proxy(proxy, test_url)
        
        if success:
            print(f"  ✓ Success! Latency: {latency:.2f}ms")
        else:
            print(f"  ✗ Failed: {error}")


async def test_proxy_info_parsing():
    print("\nTesting ProxyInfo parsing...")
    
    from data_sources.file_source import FileDataSource
    
    test_strings = [
        "http://proxy1.example.com:8080",
        "https://user:pass@proxy2.example.com:8443",
        "socks5://proxy3.example.com:1080",
        "ss://aes-256-gcm:password@ss.example.com:8388",
        "vmess://eyJ2IjoiMiIsInBzIjoidGVzdCJ9",
        "trojan://password@trojan.example.com:443",
    ]
    
    source = FileDataSource({'enabled': True, 'format': 'line', 'path': 'dummy'})
    
    for test_str in test_strings:
        proxy = source._parse_proxy_string(test_str)
        if proxy:
            print(f"  ✓ {test_str}")
            print(f"    → Protocol: {proxy.protocol}, Host: {proxy.host}, Port: {proxy.port}")
        else:
            print(f"  ✗ Failed to parse: {test_str}")


if __name__ == '__main__':
    print("=" * 60)
    print("Proxy Detector Test Suite")
    print("=" * 60)
    
    asyncio.run(test_http_handler())
    asyncio.run(test_proxy_info_parsing())
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)
