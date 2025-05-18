#!/usr/bin/env python3
from logging import getLogger

from logger_config import setup_logging

setup_logging()

log = getLogger(__name__)


def main() -> None:
    log.info('start python project')


if __name__ == '__main__':
    main()
