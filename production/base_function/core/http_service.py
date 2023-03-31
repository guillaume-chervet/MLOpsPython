import asyncio

from .async_middleware import get_is_sync, get_is_debug
from .http_singleton import SingletonAiohttp
from .i_http_service import IHttpService
import os

from .tracing import trace

APPLICATION_JSON = 'application/json'
HEADERS = {'Content-type': APPLICATION_JSON, 'Accept': APPLICATION_JSON}

@trace("name")
async def post_async(logger, data, url, number_retry=0, current_retry_number=0, http_timeout=30):
    session = SingletonAiohttp.get_aiohttp_client(http_timeout)
    logger.debug(f"begin request: {url}")
    logger.debug(f"begin request retry: {str(number_retry)}")
    async with session.post(url, json=data, headers=HEADERS) as response:
        logger.debug(f"end request: {url}")
        status = str(response.status)
        logger.debug(f"status: {status}")
        int_status = int(status)
        if int_status == 202:
            return int_status, {}
        if int_status == 200:
            result = await response.json(content_type=None)
            return int_status, result
        else:
            error = await response.text()
            logger.debug(f"response = {error}")
    if int_status >= 500 and number_retry > 0:
        logger.error(error)
        if current_retry_number > 1:
            await asyncio.sleep(1500 * (current_retry_number + 1))
        return await post_async(logger, data, url, number_retry - 1, current_retry_number + 1, http_timeout)

    return int_status, error


class HttpService(IHttpService):

    def __init__(self, logging, name="empty", local_get_is_sync=get_is_sync, local_get_is_debug=get_is_debug):
        super().__init__(logging, name)
        self.url_gateway = os.getenv("url_gateway", "http://gateway")
        self.http_timeout = int(os.getenv("http_timeout", "30"))
        self.is_debug = os.getenv("log_level", "WARNING").upper() == "DEBUG"
        self.url_template = os.getenv(f"url_{self.name_with_underscore}",
                                      f"{self.url_gateway}/{{function}}/{{function_name}}")
        self.number_retry = int(os.getenv("number_retry_" + self.name_with_underscore, 3))
        self.local_get_is_sync = local_get_is_sync
        self.local_get_is_debug = local_get_is_debug

    @trace("name")
    async def post_async(self, file_id, settings=None):
        if self.url_template == "" or self.url_template is None:
            self.logger.debug(f"Service url is empty for : {self.name}")
            return None
        data = {'id': file_id}

        name_with_underscore = self.name_with_underscore
        if settings is None:
            settings = {'action': name_with_underscore}
        else:
            settings['action'] = name_with_underscore

        if settings is not None:
            data['settings'] = settings
            self.logger.debug(f"settings: {settings}")

        is_sync = self.local_get_is_sync()
        url = self.url_template.format(url_gateway=self.url_gateway, function_name=self.name.replace("_", "-"),
                                       function="async-function")
        if is_sync is True:
            url = self.url_template.format(url_gateway=self.url_gateway, function_name=self.name.replace("_", "-"),
                                           function="function")
            url = f"{url}?sync=true"
        elif is_sync is False:
            url = f"{url}?sync=false"

        is_debug = self.local_get_is_debug()
        if is_debug:
            url = f"{url}&debug=true"

        self.logger.debug(f"begin request: {url}")
        self.logger.debug(data)
        result = await post_async(self.logger, data, url, self.number_retry, 0, self.http_timeout)
        self.logger.debug(f"post_async response: {result}")
        return result

    @trace("name")
    async def post_with_data(self, body_data):
        url = self.url_template
        if url == "" or url is None:
            self.logger.debug(f"Service url is empty for : {self.name}")
            return None
        self.logger.debug(f"begin request: {url}")
        self.logger.debug(f"post_with_data: {body_data}")
        result = await post_async(self.logger, body_data, url, self.number_retry, 0, self.http_timeout)
        self.logger.debug(f"post_with_data response: {result}")
        return result
