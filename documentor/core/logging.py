"""Simple logging system for the entire project."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Setup global logging for the project.
    
    Args:
        level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
        log_file: Path to log file (optional)
        format_string: Custom log format
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Basic configuration
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[]
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(format_string))
    
    # File handler (if specified)
    handlers = [console_handler]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(format_string))
        handlers.append(file_handler)
    
    # Setup root logger
    root_logger = logging.getLogger()
    for handler in handlers:
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get logger for module.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger
    """
    return logging.getLogger(name)


# Setup default logging on import
setup_logging()
