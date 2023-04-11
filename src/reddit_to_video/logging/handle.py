"""Logging handler that outputs to tqdm

This module contains a logging handler that outputs to tqdm. 
This is useful for logging text to the console while using tqdm for progress bars.

Classes:
    TqdmLoggingHandler(logging.Handler): Logging handler that outputs to tqdm

Functions:
    setup_logging(level=logging.INFO): Sets up logging
    remove_logger(): Removes the tqgm logger

Example:
    >>> import logging
    >>> from reddit_to_video.loggingHandle import setup_logging
    >>> setup_logging()
    >>> logging.info("Hello world!")
    2020-05-01 12:00:00,000 - root - INFO - Hello world!
    >>> remove_logger()
"""

import logging
import tqdm

tqdm_handler = None


class TqdmLoggingHandler(logging.Handler):
    """Logging handler that outputs to tqdm"""

    def __init__(self, level=logging.NOTSET):
        """Initialises the logging handler"""
        super().__init__(level)

    def emit(self, record):
        """Emits a log message"""
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise


def setup_logging(level=logging.INFO):
    """Sets up logging"""
    tqdm_handler = TqdmLoggingHandler()

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level,
        handlers=[tqdm_handler],
    )


def remove_logger():
    """Removes the tqgm logger"""
    if tqdm_handler is not None:
        logging.getLogger().removeHandler(tqdm_handler)
