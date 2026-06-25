from __future__ import annotations

import logging


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    return logging.getLogger("zhizhe")
