from typing import List

import logging
from . import init_log

logger = logging.getLogger(__name__)

def readlines(fn: str, encoding="utf-8") -> List[str]:
    try:
        with open(fn, "r", encoding=encoding) as fp:
            lines = fp.readlines()
        return lines
    except FileNotFoundError as e:
        logger.error(f"Failed to read file {fn}", e)
    return []

