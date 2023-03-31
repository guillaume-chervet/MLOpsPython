import asyncio

from .post_processing_app_settings import PostProcessingAppSettings
from ..http_service_factory import HttpServiceFactory
from ..redis import Redis


class PostProcessing:
    def __init__(self, logging, app_settings: PostProcessingAppSettings, redis: Redis, http_factory: HttpServiceFactory):
        self.logger = logging.getLogger(__name__)
        self.app_settings = app_settings
        self.redis = redis
        self.http_factory = http_factory

    async def execute_async(self, data=None, settings=None):
        self.logger.debug("PostProcessing")
        self.logger.debug(data)
        await asyncio.sleep(0.001)
        return data

    async def on_exception_async(self, exception: Exception, data=None, settings=None):
        self.logger.debug("PostProcessingException")
        self.logger.debug(exception)
        await asyncio.sleep(0.001)
        return data
