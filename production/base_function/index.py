import io
import json
from typing import Dict, Optional, Union, List

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.tracing import init_tracing
from core.async_middleware import RequestContextLogMiddleware
from core.base_app_settings import BaseAppSettings
from core.http_service_factory import HttpServiceFactory
from core.http_singleton import SingletonAiohttp
from core.log import Logging
from core.model.app_settings import AppSettings
from core.model.model_factory import ModelFactory
from core.post_processing.post_processing import PostProcessing
from core.post_processing.post_processing_app_settings import PostProcessingAppSettings
from core.pre_processing.pre_processing import PreProcessing
from core.pre_processing.pre_processing_app_settings import PreProcessingAppSettings
from core.process import Process
from core.redis import Redis
from core.scrub import scrub, add_url
from core.version import VERSION
from core.async_middleware import get_is_debug

logging = Logging()
logger = logging.getLogger(__name__)
logging.configure_module()

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:4000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestContextLogMiddleware)

app_settings = AppSettings(logging)
model = ModelFactory(logging, app_settings).create()
http_service_factory = HttpServiceFactory(logging)
redis = Redis()
post_processing = PostProcessing(logging, PostProcessingAppSettings(logging), redis, http_service_factory)
pre_processing = PreProcessing(logging, PreProcessingAppSettings(logging), redis)
base_app_settings = BaseAppSettings(logging)
process = Process(logging, redis, model, pre_processing, post_processing, base_app_settings, get_is_debug)

init_tracing(base_app_settings, app)


async def on_shutdown():
    await SingletonAiohttp.close()


@app.on_event("startup")
def startup_event():
    if hasattr(model, "startup"):
        model.startup()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    logger.exception(f"An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.warning(f"The client sent invalid data!: {exc}: {request}")
    return await request_validation_exception_handler(request, exc)


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/version")
def version():
    return {"version": VERSION}


# @trace("process_document")
async def upload_internal_async(file: UploadFile = File(...), settings_list: List[UploadFile] = File([])):
    filename = file.filename
    file_readed = await file.read()
    file_bytes = io.BytesIO(file_readed)

    settings = None
    if settings_list:
        for file in settings_list:
            file_settings = await file.read()
            settings = json.loads(file_settings.decode('utf8'))

    if settings is None:
        settings = {"version": VERSION}
    else:
        settings["version"]: VERSION

    result = await process.process_document_async(file_bytes, filename, settings)
    return result


@app.post("/upload-integration")
async def upload_integration(file: UploadFile = File(...), settings: List[UploadFile] = File([])):
    result = await upload_internal_async(file, settings)
    return scrub(result)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    result = await upload_internal_async(file, [])
    return add_url(result, base_app_settings.client_url_file)


class Item(BaseModel):
    id: str
    settings: Optional[Dict[str, Union[None, str, float, Dict[str, float]]]] = None


@app.post("/{path:path}")
async def process_data(item: Item):
    file, filename = process.get_file_byid(item.id)
    if item.settings is None:
        settings = {"file_id": item.id, "version": VERSION}
    else:
        settings = item.settings.copy()
        settings["file_id"] = item.id
        settings["version"] = VERSION
    return await process.process_document_async(file, filename, settings)


logger.info('application starting using version: %s', VERSION)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
