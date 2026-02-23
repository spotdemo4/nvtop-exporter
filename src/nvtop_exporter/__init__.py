import os
import logging
from .exporter import init, start


def main() -> None:
    logging.basicConfig(
        level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO").upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    init()
    start()
