import os

class AppSettings:
    def __init__(self, logging):
        self.logger = logging.getLogger(__name__)
        self.is_debug = os.getenv("log_level", "WARNING").upper() == "DEBUG"
