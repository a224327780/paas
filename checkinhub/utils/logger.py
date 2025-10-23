import logging
import os
from datetime import datetime
from pathlib import Path


class SiteLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        account = kwargs.pop('account', None)
        if account:
            return f"[{account}] {msg}", kwargs
        return msg, kwargs


def setup_logger(name: str = "checkinhub", level: str = "INFO", log_format: str = None) -> logging.Logger:
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper()))
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_site_logger(site_name: str, log_dir: str = "logs", level: str = "INFO") -> logging.Logger:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    logger_name = f"checkinhub.{site_name}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if logger.handlers:
        return SiteLoggerAdapter(logger, {})
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"{site_name}_{today}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(getattr(logging, level.upper()))
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return SiteLoggerAdapter(logger, {})
