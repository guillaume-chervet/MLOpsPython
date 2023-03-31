import asyncio

from .pre_processing_app_settings import PreProcessingAppSettings
from ..redis import Redis


class PreProcessing:
    def __init__(self, logging, app_settings: PreProcessingAppSettings, redis: Redis):
        self.logger = logging.getLogger(__name__)
        self.app_settings = app_settings
        self.redis = redis

    async def execute_async(self, file, settings=None):
        self.logger.debug("PreProcessing")
        self.logger.debug(settings)
        await asyncio.sleep(0.001)
        is_skip_process = False
        return is_skip_process
