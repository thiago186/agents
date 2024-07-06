import logging
import json
from pathlib import Path
from datetime import datetime

from app.config import settings


class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "module_name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage(),
            "function": record.funcName,
            "filename": record.filename,
            "lineno": record.lineno,
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


currpath = Path(__name__).resolve().parent
if currpath.name != "app":
    currpath = currpath / "app"
    

if (currpath / "logs").exists() is False:
    (currpath / "logs").mkdir()

log_files = ["controllers.log", "models.log", "api.log"]
for log_file in log_files:
    if (currpath / "logs" / log_file).exists() is False:
        (currpath / "logs" / log_file).touch()


# Setting up loggers for different modules
controller_logger = setup_logger("controllers", (currpath / "logs" / "controllers.log"))
models_logger = setup_logger("models", (currpath / "logs" / "models.log"))
api_logger = setup_logger("api", (currpath / "logs" / "api.log"))

if __name__ == "__main__":
    controller_logger.debug("This is a debug message")
    controller_logger.info("This is an info message")
    controller_logger.warning("This is a warning message")
    controller_logger.error("This is an error message")
    controller_logger.critical("This is a critical message")

    models_logger.debug("This is a debug message")
    models_logger.info("This is an info message")
    models_logger.warning("This is a warning message")
    models_logger.error("This is an error message")
    models_logger.critical("This is a critical message")

    api_logger.debug("This is a debug message")
    api_logger.info("This is an info message")
    api_logger.warning("This is a warning message")
    api_logger.error("This is an error message")

