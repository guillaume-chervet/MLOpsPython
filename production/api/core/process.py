from starlette.concurrency import run_in_threadpool
from functools import partial
from .model.inference import Inference
import asyncio

lock = asyncio.Lock()

class Process:
    def __init__(self, logging, inference: Inference):
        self.logger = logging.getLogger(__name__)
        self.inference = inference
        self.name = "execute_model"

    async def process_document_async(self, file, filename, settings=None):
        logger = self.logger
        logger.debug('before execute model %s', filename)

        if settings is not None:
            logger.debug('settings found')
            logger.debug(settings)
        else:
            logger.debug('no settings')

        def execute_with_lock(file_in, filename_in, settings_in):
            execute_compute = partial(run_in_threadpool, self.inference.execute)(file_in, filename_in, settings_in)
            return execute_compute

        data_without_redis = await execute_with_lock(file, filename, settings)

        return data_without_redis
