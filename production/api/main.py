import io
import json
import sys
from typing import Dict, Optional, Union, List

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.base_app_settings import BaseAppSettings
from core.log import Logging
from core.model.app_settings import AppSettings
from core.process import Process
from core.version import VERSION
from core.model.inference import Inference

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

app_settings = AppSettings(logging)
inference = Inference(logging, app_settings)
base_app_settings = BaseAppSettings(logging)
process = Process(logging, inference)


@app.on_event("startup")
def startup_event():
    if hasattr(inference, "startup"):
        inference.startup()


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


async def upload_internal_async(
    file: UploadFile = File(...),
        settings_list: List[UploadFile] = File([]),
        type: Optional[str] = Form(None)
):
    filename = file.filename
    file_readed = await file.read()
    file_bytes = io.BytesIO(file_readed)

    settings = None
    if settings_list:
        for file in settings_list:
            file_settings = await file.read()
            settings = json.loads(file_settings.decode("utf8"))

    if settings is None:
        settings = {"version": VERSION}
    else:
        settings["version"]: VERSION

    if type is not None:
        settings["type"] = type

    result = await process.process_document_async(file_bytes, filename, settings)
    return result


@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    settings: List[UploadFile] = File([]),
    type: Optional[str] = Form(None),
):
    result = await upload_internal_async(file, settings, type)
    return result


class Item(BaseModel):
    id: str
    settings: Optional[Dict[str, Union[None, str, float, Dict[str, float]]]] = None


logger.info("application starting using version: %s", VERSION)

if __name__ == "__main__":
    args = sys.argv
    port = 5000
    if len(args) > 1:
        port_string = args[1]
        port = int(port_string)

    uvicorn.run(app, host="0.0.0.0", port=port)
