# utils.py
import logging
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.INFO
    )

def timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
