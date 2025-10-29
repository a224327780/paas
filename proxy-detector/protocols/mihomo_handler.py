import asyncio
import json
import yaml
import aiohttp
from typing import Optional, Dict
from pathlib import Path
from loguru import logger

from data_sources.base import ProxyInfo


class MihomoProtocolHandler:
    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get('enabled', True)
        self.binary_path = Path(config.get('binary_path', './mihomo'))
        self.config_template = Path(config.get('config_template', './config/mihomo-template.yaml'))
        self.api_host = config.get('api_host', '127.0.0.1')
        self.api_port = config.get('api_port', 9090)
        self.http_port_start = config.get('http_port_start', 10000)
        self.http_port_end = config.get('http_port_end', 10100)
        self.supported_protocols = config.get('supported_protocols', [])
        
        self.mihomo_process = None
        self.current_port = self.http_port_start
        self.session = None
    
    async def start(self):
        if not self.enabled:
            logger.info("Mihomo handler is disabled")
            return
        
        if not self.binary_path.exists():
            logger.warning(f"Mihomo binary not found at {self.binary_path}")
            logger.warning("Mihomo-based protocols will not work")
            self.enabled = False
            return
        
        self.session = aiohttp.ClientSession()
        logger.info("Mihomo handler initialized")
    
    async def stop(self):
        if self.session:
            await self.session.close()
        
        if self.mihomo_process:
            try:
                self.mihomo_process.terminate()
                await self.mihomo_process.wait()
            except Exception as e:
                logger.error(f"Failed to stop Mihomo process: {e}")
    
    def supports_protocol(self, protocol: str) -> bool:
        protocol_map = {
            'hysteria': 'hysteria',
            'hysteria2': 'hysteria2',
            'hy': 'hysteria',
            'hy2': 'hysteria2'
        }
        protocol = protocol_map.get(protocol.lower(), protocol.lower())
        return protocol in self.supported_protocols
    
    async def test_proxy(self, proxy: ProxyInfo, test_url: str, timeout: int = 10) -> tuple[bool, Optional[str], Optional[float]]:
        if not self.enabled:
            return False, "Mihomo handler is disabled", None
        
        if not self.supports_protocol(proxy.protocol):
            return False, f"Protocol {proxy.protocol} not supported by Mihomo", None
        
        try:
            mihomo_config = await self._generate_mihomo_config(proxy)
            config_file = Path(f'/tmp/mihomo_config_{id(proxy)}.yaml')
            
            async with asyncio.Lock():
                with open(config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(mihomo_config, f)
            
            local_port = await self._get_next_port()
            
            process = await asyncio.create_subprocess_exec(
                str(self.binary_path),
                '-f', str(config_file),
                '-d', '/tmp',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await asyncio.sleep(2)
            
            try:
                result = await self._test_through_mihomo(local_port, test_url, timeout)
                return result
            finally:
                try:
                    process.terminate()
                    await asyncio.wait_for(process.wait(), timeout=5)
                except Exception as e:
                    logger.debug(f"Error stopping Mihomo process: {e}")
                    try:
                        process.kill()
                    except:
                        pass
                
                try:
                    config_file.unlink()
                except:
                    pass
        
        except Exception as e:
            logger.error(f"Failed to test proxy through Mihomo: {e}")
            return False, str(e), None
    
    async def _generate_mihomo_config(self, proxy: ProxyInfo) -> dict:
        if self.config_template.exists():
            with open(self.config_template, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        else:
            config = {
                'port': 7890,
                'socks-port': 7891,
                'allow-lan': False,
                'mode': 'Rule',
                'log-level': 'warning',
                'external-controller': f'{self.api_host}:{self.api_port}',
                'proxies': [],
                'proxy-groups': [],
                'rules': ['MATCH,DIRECT']
            }
        
        mihomo_proxy = await self._convert_to_mihomo_format(proxy)
        config['proxies'] = [mihomo_proxy]
        
        return config
    
    async def _convert_to_mihomo_format(self, proxy: ProxyInfo) -> dict:
        raw = proxy.raw_config
        protocol = proxy.protocol.lower()
        
        if protocol in ['ss', 'shadowsocks']:
            return self._parse_shadowsocks(raw)
        elif protocol == 'ssr':
            return self._parse_shadowsocksr(raw)
        elif protocol == 'vmess':
            return self._parse_vmess(raw)
        elif protocol == 'vless':
            return self._parse_vless(raw)
        elif protocol == 'trojan':
            return self._parse_trojan(raw)
        elif protocol in ['hysteria', 'hy']:
            return self._parse_hysteria(raw)
        elif protocol in ['hysteria2', 'hy2']:
            return self._parse_hysteria2(raw)
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")
    
    def _parse_shadowsocks(self, raw: str) -> dict:
        return {
            'name': 'test-proxy',
            'type': 'ss',
            'server': 'example.com',
            'port': 443,
            'cipher': 'aes-256-gcm',
            'password': 'password'
        }
    
    def _parse_shadowsocksr(self, raw: str) -> dict:
        return {
            'name': 'test-proxy',
            'type': 'ssr',
            'server': 'example.com',
            'port': 443,
            'cipher': 'aes-256-cfb',
            'password': 'password',
            'protocol': 'origin',
            'obfs': 'plain'
        }
    
    def _parse_vmess(self, raw: str) -> dict:
        return {
            'name': 'test-proxy',
            'type': 'vmess',
            'server': 'example.com',
            'port': 443,
            'uuid': '00000000-0000-0000-0000-000000000000',
            'alterId': 0,
            'cipher': 'auto'
        }
    
    def _parse_vless(self, raw: str) -> dict:
        return {
            'name': 'test-proxy',
            'type': 'vless',
            'server': 'example.com',
            'port': 443,
            'uuid': '00000000-0000-0000-0000-000000000000'
        }
    
    def _parse_trojan(self, raw: str) -> dict:
        return {
            'name': 'test-proxy',
            'type': 'trojan',
            'server': 'example.com',
            'port': 443,
            'password': 'password'
        }
    
    def _parse_hysteria(self, raw: str) -> dict:
        return {
            'name': 'test-proxy',
            'type': 'hysteria',
            'server': 'example.com',
            'port': 443,
            'auth_str': 'password'
        }
    
    def _parse_hysteria2(self, raw: str) -> dict:
        return {
            'name': 'test-proxy',
            'type': 'hysteria2',
            'server': 'example.com',
            'port': 443,
            'password': 'password'
        }
    
    async def _get_next_port(self) -> int:
        port = self.current_port
        self.current_port += 1
        if self.current_port > self.http_port_end:
            self.current_port = self.http_port_start
        return port
    
    async def _test_through_mihomo(self, local_port: int, test_url: str, timeout: int) -> tuple[bool, Optional[str], Optional[float]]:
        proxy_url = f'http://127.0.0.1:{local_port}'
        
        try:
            client_timeout = aiohttp.ClientTimeout(total=timeout)
            connector = aiohttp.TCPConnector(ssl=False)
            
            async with aiohttp.ClientSession(connector=connector, timeout=client_timeout) as session:
                start_time = asyncio.get_event_loop().time()
                
                async with session.get(test_url, proxy=proxy_url) as response:
                    await response.read()
                    
                    end_time = asyncio.get_event_loop().time()
                    latency = (end_time - start_time) * 1000
                    
                    if response.status in [200, 201, 204, 301, 302, 307, 308]:
                        logger.debug(f"Mihomo proxy test successful, latency: {latency:.2f}ms")
                        return True, None, latency
                    else:
                        return False, f"HTTP {response.status}", None
        
        except asyncio.TimeoutError:
            return False, "Timeout", None
        except Exception as e:
            logger.debug(f"Mihomo proxy test failed: {e}")
            return False, str(e), None
