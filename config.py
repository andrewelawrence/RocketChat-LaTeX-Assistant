import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Log directory
_LOG_DIR = os.environ.get("logDir")
_DEFAULT_PATH = os.path.join(_LOG_DIR, "app.log")

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s -- %(message)s",
    handlers=[
        TimedRotatingFileHandler(_DEFAULT_PATH, when="midnight", interval=1, backupCount=7),
        logging.StreamHandler()
    ]
)

def get_logger(name: str, user_id: str = None) -> logging.Logger:
    logger = logging.getLogger(name)

    if user_id:
        user_log_path = os.path.join(_LOG_DIR, f"user_{user_id}.log")
        user_handler = TimedRotatingFileHandler(user_log_path, when="midnight", interval=1, backupCount=7)
        user_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
        logger.addHandler(user_handler)
        
    return logger
