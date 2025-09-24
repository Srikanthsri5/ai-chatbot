"""
Custom logging configuration for the application.
(Logging without storing logs in database)
"""
from loguru import logger
import sys, json
# Load configuration

# Remove default logger to customize
logger.remove()
rotation_limit = "50 MB"
retention_limit = "30 days"
login_formatter = "{time:DD-MMMM-YYYY HH:mm:ss} - {message}"
# Formatter for all loggers
formatter = "{time:DD-MMMM-YYYY HH:mm:ss} - {level} - {message}"
login_formatter = login_formatter
logger.level("Execute", no=27, color="<yellow>", icon="⚙️")
logger.level("API", no=25, color="<cyan>", icon="📦")
logger.level("LOGIN", no=24, color="<green>", icon="📥")

# Console handler (for all log levels)
# logger.add(sys.stdout, format=formatter, level="DEBUG")
logger.add(
    sys.stdout,
    format=formatter,
    level="DEBUG",
    filter=lambda record: record["level"].name not in ["INFO", "SUCCESS", "API"]
)

# File handler for DEBUG level logs
logger.add(
    "app_logs/debug.log",
    format=formatter,
    level="DEBUG",
    filter=lambda record: record["level"].name == "DEBUG",
    rotation=rotation_limit,  # Rotate after 100 MB
    retention=retention_limit,  # Retain logs for 30 days
)

# File handler for INFO level logs
logger.add(
    "app_logs/info.log",
    format=formatter,
    level="INFO",
    filter=lambda record: record["level"].name == "INFO",
    rotation=rotation_limit,  # Rotate after 100 MB
    retention=retention_limit,  # Retain logs for 30 days
)

# File handler for ERROR level logs
logger.add(
    "app_logs/error.log",
    format=formatter,
    level="ERROR",
    filter=lambda record: record["level"].name == "ERROR",
    rotation=rotation_limit,  # Rotate after 100 MB
    retention=retention_limit,  # Retain logs for 30 days
)

# File handler for SUCCESS level logs
logger.add(
    "app_logs/login.log",
    format=login_formatter,
    level="LOGIN",
    filter=lambda record: record["level"].name == "LOGIN",
    rotation=rotation_limit,  # Rotate after 50 MB
    retention=retention_limit,  # Retain logs for 30 days
)

# File handler for API response logs
logger.add(
    "app_logs/api_responses.log",
    format="{time:DD-MMMM-YYYY HH:mm:ss} - {message}",
    level="API",
    filter=lambda record: record["level"].name == "API",
    rotation=rotation_limit,
    retention=retention_limit,
)

