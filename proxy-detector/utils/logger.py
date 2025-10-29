import sys
from pathlib import Path
from loguru import logger


class Logger:
    def __init__(self, config: dict):
        self.config = config
        self._setup_logger()
    
    def _setup_logger(self):
        logger.remove()
        
        log_format = self.config.get('format', 
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}")
        level = self.config.get('level', 'INFO')
        
        logger.add(
            sys.stderr,
            format=log_format,
            level=level,
            colorize=True
        )
        
        log_file = self.config.get('file')
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.add(
                log_file,
                format=log_format,
                level=level,
                rotation=self.config.get('rotation', '10 MB'),
                retention=self.config.get('retention', '7 days'),
                compression='zip'
            )
    
    @staticmethod
    def get_logger():
        return logger


def setup_logger(config: dict):
    Logger(config)
    return logger
