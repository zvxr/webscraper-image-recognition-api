from logging.config import dictConfig

from app.models.log import LogConfig

import logging


def setup_logging():
    dictConfig(LogConfig().dict())


def get_logger(name):
    a = 1
    return logging.getLogger(f"redflag.{name}")
