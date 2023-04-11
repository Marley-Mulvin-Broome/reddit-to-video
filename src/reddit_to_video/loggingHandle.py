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
        except:
            self.handleError(record)


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
