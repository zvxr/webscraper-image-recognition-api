import logging
from logging.config import dictConfig

from app.models.log import LogConfig


def setup_logging():
    dictConfig(LogConfig().dict())


def get_logger(name):
    return logging.getLogger(f"wira.{name}")
