import asyncio
import argparse
from pathlib import Path

from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from core.detector import ProxyDetector


async def main():
    parser = argparse.ArgumentParser(description='Proxy Detector - Multi-protocol proxy detection tool')
    parser.add_argument(
        '-c', '--config',
        default='./config/config.yaml',
        help='Path to configuration file (default: ./config/config.yaml)'
    )
    parser.add_argument(
        '-o', '--once',
        action='store_true',
        help='Run detection once and exit (default: continuous mode)'
    )
    parser.add_argument(
        '-i', '--interval',
        type=int,
        help='Override detection interval in seconds'
    )
    
    args = parser.parse_args()
    
    config_loader = ConfigLoader(args.config)
    config = config_loader.config
    
    logger = setup_logger(config_loader.get_logging_config())
    
    logger.info("=" * 60)
    logger.info("Proxy Detector - Multi-protocol proxy detection")
    logger.info("Supported protocols: HTTP, HTTPS, SOCKS5, SS, SSR, VMESS, VLESS, TROJAN, Hysteria, Hysteria2")
    logger.info("=" * 60)
    
    detector = ProxyDetector(config)
    await detector.initialize()
    
    try:
        if args.once:
            await detector.run_detection()
        else:
            detection_config = config_loader.get_detection_config()
            interval = args.interval or detection_config.get('check_interval', 300)
            
            logger.info(f"Running in continuous mode with {interval}s interval")
            logger.info("Press Ctrl+C to stop")
            
            while True:
                try:
                    await detector.run_detection()
                    logger.info(f"Waiting {interval} seconds until next detection cycle...")
                    await asyncio.sleep(interval)
                except KeyboardInterrupt:
                    logger.info("Received interrupt signal, shutting down...")
                    break
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        await detector.cleanup()
        logger.info("Proxy Detector stopped")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete")
