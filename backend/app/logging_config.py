"""
Logging configuration for crane lifting capacity app.
"""

import json
import logging
import logging.config
from pathlib import Path

from app import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter using built-in json module."""

    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        return json.dumps(log_entry, indent=2)


# Logging configuration dictionary for uvicorn server
# This follows Python's dictConfig format:
# https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
LOG_CONFIG = {
    # Version of the logging configuration schema (always 1)
    "version": 1,
    # Don't disable existing loggers from other parts of the application
    "disable_existing_loggers": False,
    # FORMATTERS: Define how log messages should look like
    "formatters": {
        # Default formatter for general server messages (startup, shutdown, etc)
        "default": {
            # Use uvicorn's built-in formatter class
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        # Formatter specifically for HTTP access logs (requests/responses)
        "access": {
            # Use uvicorn's built-in access formatter
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": (
                '%(levelprefix)s %(client_addr)s - '
                '"%(request_line)s" %(status_code)s'
            ),
        },
        # Custom JSON formatter for file logging
        "json": {
            "()": JSONFormatter,
        },
    },
    # HANDLERS: Define WHERE logs should go (console, file, etc.)
    "handlers": {
        # Handler for general server messages to console
        "console": {
            # StreamHandler = output to a stream (stdout/stderr)
            "class": "logging.StreamHandler",
            # Send output to standard output (your terminal)
            "stream": "ext://sys.stdout",
            # Use the "default" formatter defined above
            "formatter": "default",
        },
        # Handler for HTTP access logs to console
        "console_access": {
            # Also a stream handler
            "class": "logging.StreamHandler",
            # Also to standard output
            "stream": "ext://sys.stdout",
            # Use the "access" formatter for HTTP request format
            "formatter": "access",
        },
        # Handler for ALL logs to file (both server and access logs)
        "file": {
            # RotatingFileHandler = creates new files when size limit reached
            "class": "logging.handlers.RotatingFileHandler",
            # File path where logs will be written
            "filename": "../logs/crane_lifting_capacity.log",
            # Maximum file size before rotation (10MB)
            "maxBytes": 10485760,
            # Keep 5 backup files
            # (crane_lifting_capacity.log.1, crane_lifting_capacity.log.2, etc.)
            "backupCount": 5,
            # Use JSON format for structured logging in files
            "formatter": "json",
        },
    },
    # LOGGERS: Configure specific loggers and connect them to handlers
    "loggers": {
        # Main uvicorn logger - handles general server messages
        "uvicorn": {
            # Send logs to both console (with colors) and file (as JSON)
            "handlers": ["console", "file"],
            # Only log INFO level and above (INFO, WARNING, ERROR, CRITICAL)
            "level": "INFO",
            # Don't pass logs up to parent loggers (prevents duplication)
            "propagate": False,
        },
        # Uvicorn access logger - handles HTTP request/response logs
        "uvicorn.access": {
            # Send to special access console format AND to file as JSON
            "handlers": ["console_access", "file"],
            # Also INFO level and above
            "level": "INFO",
            # Don't propagate to prevent duplicate logs
            "propagate": False,
        },
    },
}


def ensure_logs_directory():
    """Create logs directory if it doesn't exist."""
    Path("../logs").mkdir(exist_ok=True)


def get_safe_settings_for_logging():
    """Get settings that are safe to log (excluding sensitive information)."""
    return {
        "APP_TITLE": settings.APP_TITLE,
        "APP_DESCRIPTION": settings.APP_DESCRIPTION,
        "APP_VERSION": settings.APP_VERSION,
        "PORT": settings.PORT,
        "DEVELOPMENT": settings.DEVELOPMENT,
        "SUPPORTED_IMAGE_CONTENT_TYPES": settings.SUPPORTED_IMAGE_CONTENT_TYPES,
        "PAGINATION_SIZE": settings.PAGINATION_SIZE,
    }


def log_startup_settings():
    """Log application settings after startup."""
    logger = logging.getLogger("uvicorn")

    logger.info("=== Application Settings ===")
    safe_settings = get_safe_settings_for_logging()

    for key, value in safe_settings.items():
        logger.info(f"{key}: {value}")
    logger.info("=== End Settings ===")


def setup_logging():
    """Setup logging configuration based on development mode."""
    if not settings.DEVELOPMENT:
        # Production mode: setup file logging + console logging
        ensure_logs_directory()
        logging.config.dictConfig(LOG_CONFIG)
        log_startup_settings()
    else:
        # Development mode: only show settings, no file logging
        log_startup_settings()
