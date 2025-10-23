import logging
from pathlib import Path
from datetime import datetime
from app.config import LOGS_DIR


def get_daily_log_file(site_id: str) -> Path:
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"{site_id}_{date_str}.log"
    return log_file


def setup_logger(site_id: str) -> logging.Logger:
    logger = logging.getLogger(f"checkhub.{site_id}")
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        logger.handlers.clear()
    
    log_file = get_daily_log_file(site_id)
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger


def get_main_logger() -> logging.Logger:
    logger = logging.getLogger("checkhub.main")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
        file_handler = logging.FileHandler(
            LOGS_DIR / "main.log",
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
