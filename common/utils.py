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
        msg = f"Not Found: {fn}"
        logger.error(msg)
        raise FileNotFoundError(msg)
    return []

