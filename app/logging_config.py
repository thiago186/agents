import logging
import json
from pathlib import Path
from datetime import datetime

from .config import settings

class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "module_name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage(),
            "function": record.funcName,
        }
        return json.dumps(log_record)

def setup_logger(name, log_file, level=settings.log_level):
    """Function to set up as many loggers as you want"""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    # Create a logging format
    formatter = CustomJsonFormatter()
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger


if Path("logs").exists() is False:
    Path("logs").mkdir()

log_files = ["logs/controllers.log", "logs/models.log", "logs/api.log"]
for log_file in log_files:
    if Path(log_file).exists() is False:
        Path(log_file).touch()


# Setting up loggers for different modules
controller_logger = setup_logger("controllers", "logs/controllers.log")
models_logger = setup_logger("models", "logs/models.log")
api_logger = setup_logger("api", "logs/api.log")
