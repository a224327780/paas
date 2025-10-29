import asyncio
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from loguru import logger

from data_sources.base import ProxyInfo
from data_sources.file_source import FileDataSource
from data_sources.url_source import UrlDataSource
from data_sources.api_source import ApiDataSource
from protocols.http_handler import HttpProtocolHandler
from protocols.mihomo_handler import MihomoProtocolHandler


class ProxyDetector:
    def __init__(self, config: dict):
        self.config = config
        self.data_sources = []
        self.http_handler = None
        self.mihomo_handler = None
        
        self.detection_config = config.get('detection', {})
        self.timeout = self.detection_config.get('timeout', 10)
        self.concurrent_tasks = self.detection_config.get('concurrent_tasks', 50)
        self.retry_attempts = self.detection_config.get('retry_attempts', 2)
        self.test_urls = self.detection_config.get('test_urls', ['https://www.google.com'])
        
        self.output_config = config.get('output', {})
        
        self.statistics = {
            'total': 0,
            'working': 0,
            'failed': 0,
            'by_protocol': {},
            'start_time': None,
            'end_time': None
        }
    
    async def initialize(self):
        logger.info("Initializing Proxy Detector...")
        
        self._init_data_sources()
        
        self.http_handler = HttpProtocolHandler(timeout=self.timeout)
        
        mihomo_config = self.config.get('mihomo', {})
        self.mihomo_handler = MihomoProtocolHandler(mihomo_config)
        await self.mihomo_handler.start()
        
        logger.info("Proxy Detector initialized successfully")
    
    def _init_data_sources(self):
        data_source_configs = self.config.get('data_sources', [])
        
        for ds_config in data_source_configs:
            ds_type = ds_config.get('type')
            
            if ds_type == 'file':
                self.data_sources.append(FileDataSource(ds_config))
            elif ds_type == 'url':
                self.data_sources.append(UrlDataSource(ds_config))
            elif ds_type == 'api':
                self.data_sources.append(ApiDataSource(ds_config))
            else:
                logger.warning(f"Unknown data source type: {ds_type}")
        
        logger.info(f"Initialized {len(self.data_sources)} data sources")
    
    async def fetch_all_proxies(self) -> List[ProxyInfo]:
        all_proxies = []
        
        tasks = [source.fetch_proxies() for source in self.data_sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch proxies: {result}")
            elif isinstance(result, list):
                all_proxies.extend(result)
        
        logger.info(f"Fetched total of {len(all_proxies)} proxies from all sources")
        return all_proxies
    
    async def detect_proxy(self, proxy: ProxyInfo) -> Dict:
        protocol = proxy.protocol.lower()
        
        for attempt in range(self.retry_attempts + 1):
            try:
                if protocol in ['http', 'https', 'socks5']:
                    test_url = self.test_urls[0]
                    success, error, latency = await self.http_handler.test_proxy(proxy, test_url)
                
                elif self.mihomo_handler.supports_protocol(protocol):
                    test_url = self.test_urls[0]
                    success, error, latency = await self.mihomo_handler.test_proxy(
                        proxy, test_url, self.timeout
                    )
                
                else:
                    success = False
                    error = f"Unsupported protocol: {protocol}"
                    latency = None
                
                if success or attempt == self.retry_attempts:
                    return {
                        'proxy': proxy,
                        'success': success,
                        'error': error,
                        'latency': latency,
                        'attempts': attempt + 1,
                        'timestamp': datetime.now().isoformat()
                    }
                
                await asyncio.sleep(1)
            
            except Exception as e:
                logger.error(f"Unexpected error testing proxy {proxy}: {e}")
                if attempt == self.retry_attempts:
                    return {
                        'proxy': proxy,
                        'success': False,
                        'error': str(e),
                        'latency': None,
                        'attempts': attempt + 1,
                        'timestamp': datetime.now().isoformat()
                    }
        
        return {
            'proxy': proxy,
            'success': False,
            'error': 'Max retries exceeded',
            'latency': None,
            'attempts': self.retry_attempts + 1,
            'timestamp': datetime.now().isoformat()
        }
    
    async def run_detection(self):
        logger.info("Starting proxy detection...")
        self.statistics['start_time'] = datetime.now().isoformat()
        
        proxies = await self.fetch_all_proxies()
        
        if not proxies:
            logger.warning("No proxies to test")
            return
        
        self.statistics['total'] = len(proxies)
        
        semaphore = asyncio.Semaphore(self.concurrent_tasks)
        
        async def bounded_detect(proxy):
            async with semaphore:
                return await self.detect_proxy(proxy)
        
        tasks = [bounded_detect(proxy) for proxy in proxies]
        results = await asyncio.gather(*tasks)
        
        working_proxies = []
        failed_proxies = []
        
        for result in results:
            protocol = result['proxy'].protocol
            if protocol not in self.statistics['by_protocol']:
                self.statistics['by_protocol'][protocol] = {'total': 0, 'working': 0, 'failed': 0}
            
            self.statistics['by_protocol'][protocol]['total'] += 1
            
            if result['success']:
                working_proxies.append(result)
                self.statistics['working'] += 1
                self.statistics['by_protocol'][protocol]['working'] += 1
                logger.info(f"✓ {result['proxy']} - Latency: {result['latency']:.2f}ms")
            else:
                failed_proxies.append(result)
                self.statistics['failed'] += 1
                self.statistics['by_protocol'][protocol]['failed'] += 1
                logger.debug(f"✗ {result['proxy']} - Error: {result['error']}")
        
        self.statistics['end_time'] = datetime.now().isoformat()
        
        await self._save_results(working_proxies, failed_proxies)
        self._print_statistics()
    
    async def _save_results(self, working_proxies: List[Dict], failed_proxies: List[Dict]):
        if self.output_config.get('save_working', True):
            working_file = Path(self.output_config.get('working_proxies_file', './output/working_proxies.txt'))
            working_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(working_file, 'w', encoding='utf-8') as f:
                for result in working_proxies:
                    proxy = result['proxy']
                    latency = result['latency']
                    f.write(f"{proxy.to_url()} # Latency: {latency:.2f}ms\n")
            
            logger.info(f"Saved {len(working_proxies)} working proxies to {working_file}")
        
        if self.output_config.get('save_failed', True):
            failed_file = Path(self.output_config.get('failed_proxies_file', './output/failed_proxies.txt'))
            failed_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(failed_file, 'w', encoding='utf-8') as f:
                for result in failed_proxies:
                    proxy = result['proxy']
                    error = result['error']
                    f.write(f"{proxy.to_url()} # Error: {error}\n")
            
            logger.info(f"Saved {len(failed_proxies)} failed proxies to {failed_file}")
        
        if self.output_config.get('save_statistics', True):
            stats_file = Path(self.output_config.get('statistics_file', './output/statistics.json'))
            stats_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.statistics, f, indent=2)
            
            logger.info(f"Saved statistics to {stats_file}")
    
    def _print_statistics(self):
        logger.info("=" * 60)
        logger.info("Detection Statistics:")
        logger.info(f"Total Proxies: {self.statistics['total']}")
        logger.info(f"Working: {self.statistics['working']}")
        logger.info(f"Failed: {self.statistics['failed']}")
        logger.info(f"Success Rate: {self.statistics['working']/self.statistics['total']*100:.2f}%")
        
        logger.info("\nBy Protocol:")
        for protocol, stats in self.statistics['by_protocol'].items():
            logger.info(f"  {protocol.upper()}: {stats['working']}/{stats['total']} working")
        
        logger.info("=" * 60)
    
    async def cleanup(self):
        logger.info("Cleaning up...")
        
        for source in self.data_sources:
            await source.close()
        
        await self.mihomo_handler.stop()
        
        logger.info("Cleanup completed")
