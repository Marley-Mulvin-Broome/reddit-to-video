import logging
import tqdm

tqdm_handler = None


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def setup_logging(level=logging.INFO):
    global tqdm_handler
    tqdm_handler = TqdmLoggingHandler()

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level,
        handlers=[tqdm_handler],
    )


def remove_logger():
    global tqdm_handler

    if tqdm_handler is not None:
        logging.getLogger().removeHandler(tqdm_handler)
