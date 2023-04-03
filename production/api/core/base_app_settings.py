import os

from pathlib import Path

from .model.name import NAME


class BaseAppSettings:
    def __init__(self, logging):
        self.logger = logging.getLogger(__name__)
        self.is_debug = os.getenv("log_level", "WARNING").upper() == "DEBUG"
