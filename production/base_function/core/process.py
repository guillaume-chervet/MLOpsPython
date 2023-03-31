import copy
import io
import uuid

from starlette.concurrency import run_in_threadpool
from functools import partial

from .base_app_settings import BaseAppSettings
from .model.model import Model
from .redis import Redis
from .post_processing.post_processing import PostProcessing
from .pre_processing.pre_processing import PreProcessing
from .async_middleware import get_is_debug

from .scrub import scrub_internal
from datetime import datetime, timedelta
import asyncio

from .tracing import trace


redis_key_global_state = "global-state"


def extract_property_name(mail_json_id):
    state_property_name = mail_json_id
    to_replace = [["-", ""], ["0", "a"], ["1", "b"], ["2", "c"], ["3", "d"], ["4", "e"], ["5", "f"], ["6", "g"],
                  ["7", "h"], ["8", "i"], ["9", "j"]]
    for key in to_replace:
        state_property_name = state_property_name.replace(key[0], key[1])

    return state_property_name


def check_timeout(settings, redis: Redis, logger, orchestrator_timeout_second: int):
    if settings is not None:
        if settings.get("file_id") is None:
            return False
    else:
        return False
    mail_json_id = settings['mail_json_id']
    redis_connection, path = redis.redis_connection()
    # Si on a dépassé un certain temps on ne répond plus car la réponse sera prise en compte par le pod Orchestrator
    state_property_name = extract_property_name(mail_json_id)
    full_state = redis_connection.jsonget(redis_key_global_state, path.rootPath(), no_escape=True)
    state = None
    if state_property_name in full_state:
        state = full_state[state_property_name]

    if state is None:
        logger.warn(f"timeout global state not found {mail_json_id}")
        return True

    if state["end"] is not None:
        logger.warn(f"timeout response already sent {mail_json_id}")
        return True

    datetime_receive = datetime.fromtimestamp(state["start"])
    datetime_now = datetime.now()
    is_time_to_respond_elapsed = (datetime_now - timedelta(
        seconds=orchestrator_timeout_second)) > datetime_receive
    if is_time_to_respond_elapsed:
        logger.warn(f"timeout time elapsed {mail_json_id}")
        return True
    return False


lock = asyncio.Lock()


class Process:
    def __init__(self, logging, redis: Redis, model: Model,
                 pre_processing: PreProcessing, post_processing: PostProcessing, base_app_settings: BaseAppSettings, local_get_is_debug:get_is_debug):
        self.logger = logging.getLogger(__name__)
        self.redis = redis
        self.model = model
        self.pre_processing = pre_processing
        self.post_processing = post_processing
        self.name = "execute_model"
        self.orchestrator_timeout_second = base_app_settings.orchestrator_timeout_second
        self.local_get_is_debug = local_get_is_debug

    @trace("name")
    async def process_document_async(self, file, filename, settings=None):
        logger = self.logger
        redis = self.redis
        data = None
        try:
            logger.debug('before execute model %s', filename)
            if settings is not None:
                logger.debug('settings found')
                logger.debug(settings)
            else:
                logger.debug('no settings')

            is_skip_process = check_timeout(settings, self.redis, logger, self.orchestrator_timeout_second)

            if is_skip_process:
                return {
                    "process_skipped": True,
                    "reason": "timeout"
                    }

            is_skip_process = await self.pre_processing.execute_async(file, settings)

            if is_skip_process:
                return {
                    "process_skipped": True,
                    "reason": "pre_processing"
                    }

            def execute_with_lock(file_in, filename_in, settings_in):
                execute_compute = partial(run_in_threadpool, self.model.execute)(file_in, filename_in, settings_in)
                return execute_compute

            data_without_redis = await execute_with_lock(file, filename, settings)

            self.remove_file_from_redis(settings)
            logger.debug('after execute model')
            data = scrub(redis, data_without_redis)
            post_processed_data = await self.post_processing.execute_async(data, settings)
        except Exception as e:
            logger.exception("some exception occured", exc_info=e)
            await self.post_processing.on_exception_async(e, data, settings)
            return {}
        return post_processed_data

    def remove_file_from_redis(self, settings):
        if settings is not None:
            file_id = settings.get("file_id")
            if self.local_get_is_debug():
                self.logger.debug("is debug=true so file is not removed : " + file_id)
                return
            if file_id is not None:
                self.redis.redis_delete(file_id)

    def get_file_byid(self, id: str):
        if id.startswith("json:"):
            redis_id = id.replace('json:', '', 1)
            splits = redis_id.split(":")
            redis_connection, path = self.redis.redis_connection()
            query_path = path.rootPath()
            if len(splits) == 2:
                redis_id = splits[1]
                if splits[0] != "":
                    query_path = path(splits[0])
            json_data = redis_connection.jsonget(redis_id, query_path, no_escape=True)
            return json_data, "none.txt"
        try:
            image_info = self.redis.redis_hgetall(id)
            filename = image_info[b"filename"].decode("utf-8")
            image_bytes = image_info[b"bytes"]
            return io.BytesIO(image_bytes), filename
        except Exception as e:
            self.logger.error("Error get_file_byid : ", e)
            raise e


def scrub(redis, data):
    def add_redis_mutate(obj, key, index):

        if obj[key] is None:
            del obj[key]
            return

        file_bytes = obj[key].read()
        del obj[key]
        filename = "no_name.unknown"
        if "filename" in obj:
            filename = obj["filename"]

        redis_key = str(uuid.uuid4())
        image_info_redis = {"filename": filename, "bytes": file_bytes}
        redis.redis_hmset(redis_key, image_info_redis)

        part_of_key = key.replace('file_bytes', '')
        if part_of_key != "":
            new_key = "file_id" + part_of_key
        else:
            new_key = "file_id"

        obj[new_key] = redis_key

    return scrub_internal(copy.deepcopy(data), add_redis_mutate, "file_bytes")
