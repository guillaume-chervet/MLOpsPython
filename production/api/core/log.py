import os
import logging.config
import logging
import time

log_level = os.getenv("log_level", "WARNING").upper()


class Logging:
    def getLogger(self, name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.propagate = 0
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s.%(module)s.%(funcName)s:" "%(lineno)d - %(levelname)s - %(message)s"
            )
            formatter.converter = time.gmtime
            console_handler = logging.StreamHandler()
            logger.setLevel(log_level)
            logger.addHandler(console_handler)
            console_handler.setFormatter(formatter)

        return logger

    def configure_module(self):
        logging.getLogger('uvicorn:').setLevel(logging.ERROR)
        logging.getLogger('gunicorn').setLevel(logging.ERROR)
