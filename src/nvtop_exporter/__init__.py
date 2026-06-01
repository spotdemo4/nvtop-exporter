import os
import logging
from .exporter import init, start

LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "WARN": logging.WARN,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def get_log_level() -> int:
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    return LOG_LEVELS[log_level_name]


def main() -> None:
    logging.basicConfig(
        level=get_log_level(),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    init()
    start()
