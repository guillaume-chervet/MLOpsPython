from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from .log import Logging
from starlette.responses import Response
from http import HTTPStatus

logging = Logging()
logger = logging.getLogger(__name__)

SYNC = "sync"
IS_SYNC_CTX_KEY = 'is_sync'
_is_sync_ctx_var: ContextVar[bool] = ContextVar(IS_SYNC_CTX_KEY, default=True)
def get_is_sync() -> bool:
    return _is_sync_ctx_var.get()

DEBUG = "debug"
IS_DEBUG_CTX_KEY = 'is_debug'
_is_debug_ctx_var: ContextVar[bool] = ContextVar(IS_DEBUG_CTX_KEY, default=True)
def get_is_debug() -> bool:
    return _is_debug_ctx_var.get()

def extract_query_param(request, name):
    is_sync = None
    if name in request.query_params:
        is_sync_params = request.query_params[name]
        if is_sync_params is None or is_sync_params == "":
            is_sync = None
        elif is_sync_params == "false":
            is_sync = False
        else:
            is_sync = True
    return is_sync


class RequestContextLogMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):

        is_sync = _is_sync_ctx_var.set(extract_query_param(request, SYNC))
        is_debug = _is_debug_ctx_var.set(extract_query_param(request, DEBUG))

        try:
            response = await call_next(request)
            return response
        # starlette issue https://github.com/encode/starlette/discussions/1527?msclkid=bf5e446ad04711ec9aa56a00ca155b1e
        except RuntimeError as e:
            if await request.is_disconnected() and str(e) == "No response returned.":
                logger.warning(
                    "Error `No response returned` detected. "
                    "At the same time we know that the client is disconnected "
                    "and not waiting for a response."
                )

                return Response(status_code=HTTPStatus.NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            _is_sync_ctx_var.reset(is_sync)
            _is_debug_ctx_var.reset(is_debug)

