import yaml
from pathlib import Path
from typing import Any, Dict
from loguru import logger


class ConfigLoader:
    def __init__(self, config_path: str = "./config/config.yaml"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
            return self.config
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_data_sources(self) -> list:
        return self.config.get('data_sources', [])
    
    def get_detection_config(self) -> dict:
        return self.config.get('detection', {})
    
    def get_mihomo_config(self) -> dict:
        return self.config.get('mihomo', {})
    
    def get_logging_config(self) -> dict:
        return self.config.get('logging', {})
    
    def get_output_config(self) -> dict:
        return self.config.get('output', {})
