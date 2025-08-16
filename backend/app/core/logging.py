import logging
import logging.handlers
import sys
import os
from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime

from app.core.config import settings

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)

class CustomFormatter(logging.Formatter):
    """Custom formatter with colors for development"""
    
    # Color codes
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logging() -> None:
    """Setup application logging with proper configuration"""
    
    # Clear any existing handlers
    logging.getLogger().handlers.clear()
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Create formatters
    if settings.ENVIRONMENT == "production":
        formatter = JSONFormatter()
        console_formatter = JSONFormatter()
    else:
        formatter = CustomFormatter(settings.LOG_FORMAT)
        console_formatter = CustomFormatter(settings.LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Error file handler (for errors only)
    error_handler = logging.handlers.RotatingFileHandler(
        "logs/error.log",
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    
    # Suppress noisy loggers in production
    if settings.ENVIRONMENT == "production":
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(name)

def log_request(request_id: str, method: str, path: str, status_code: int, duration: float) -> None:
    """Log HTTP request details"""
    logger = get_logger("http")
    extra_fields = {
        "request_id": request_id,
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration * 1000, 2)
    }
    
    if status_code >= 400:
        logger.warning("HTTP Request", extra={"extra_fields": extra_fields})
    else:
        logger.info("HTTP Request", extra={"extra_fields": extra_fields})

def log_database_operation(operation: str, table: str, duration: float, success: bool) -> None:
    """Log database operation details"""
    logger = get_logger("database")
    extra_fields = {
        "operation": operation,
        "table": table,
        "duration_ms": round(duration * 1000, 2),
        "success": success
    }
    
    if success:
        logger.debug("Database Operation", extra={"extra_fields": extra_fields})
    else:
        logger.error("Database Operation Failed", extra={"extra_fields": extra_fields})

def log_external_api_call(api_name: str, endpoint: str, duration: float, status_code: int, success: bool) -> None:
    """Log external API call details"""
    logger = get_logger("external_api")
    extra_fields = {
        "api_name": api_name,
        "endpoint": endpoint,
        "duration_ms": round(duration * 1000, 2),
        "status_code": status_code,
        "success": success
    }
    
    if success:
        logger.info("External API Call", extra={"extra_fields": extra_fields})
    else:
        logger.error("External API Call Failed", extra={"extra_fields": extra_fields})

# Initialize logging
setup_logging()

# Create main logger
logger = get_logger(__name__)
