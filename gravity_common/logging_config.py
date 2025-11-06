"""
Logging configuration for consistent logging across all microservices.

Each service can use these utilities while maintaining independence.
"""

import logging
import sys
from typing import Optional
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter for structured logging.
    
    Adds service name and standardized fields to all log records.
    """
    
    def __init__(self, *args, service_name: str = "gravity-service", **kwargs):
        self.service_name = service_name
        super().__init__(*args, **kwargs)
    
    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to log record."""
        super().add_fields(log_record, record, message_dict)
        log_record['service'] = self.service_name
        log_record['level'] = record.levelname
        log_record['logger'] = record.name


def setup_logging(
    service_name: str,
    log_level: str = "INFO",
    json_logs: bool = True,
) -> logging.Logger:
    """
    Setup logging configuration for a microservice.
    
    Args:
        service_name: Name of the microservice
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Whether to use JSON format (True) or text format (False)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    if json_logs:
        # Use JSON formatter for production
        formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s',
            service_name=service_name,
        )
    else:
        # Use text formatter for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
