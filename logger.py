from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os
import logging

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name: str = "default"):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        log_filename = os.path.join(LOG_DIR, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
        handler = TimedRotatingFileHandler(
            log_filename, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger